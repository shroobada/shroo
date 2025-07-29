import threading
from concurrent.futures import ThreadPoolExecutor

from django.apps import AppConfig
from decouple import config
import pynetbox
import asyncio
import json
import time

from typing import Dict, Tuple, List, Optional, Generator, Any, AsyncGenerator

from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class CacheEntry:
    data: List[Dict]
    timestamp: float
    ttl: int
    endpoint_name: str
    filters: Optional[Dict]

    @property
    def is_expired(self) -> bool:
        return time.time() - self.timestamp > self.ttl

    @property
    def age_seconds(self) -> float:
        return time.time() - self.timestamp

    @property
    def remaining_ttl(self) -> float:
        return max(0.0, self.ttl - self.age_seconds)



class OptimizedNetBoxClient:
    def __init__(self, netbox_url: str, token: str, default_ttl: int = 300):
        self.nb = pynetbox.api(netbox_url, token=token)
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = {}
        self.fetch_locks: Dict[str, threading.Lock] = {}
        self.async_fetch_locks: Dict[str, asyncio.Lock] = {}
        self.cleanup_thread = None
        self.is_running = False
        self._cache_lock = threading.RLock()  # Protects cache dictionary

        # Thread pool for async operations
        self.thread_pool = ThreadPoolExecutor(max_workers=4)

    def start_cache_manager(self, cleanup_interval: int = 60):
        """Start the cache manager with automatic cleanup (thread-based)"""
        if self.is_running:
            return

        self.is_running = True

        # Start cleanup thread (works in any context)
        self.cleanup_thread = threading.Thread(
            target=self._cleanup_expired_entries_thread,
            args=(cleanup_interval,),
            daemon=True
        )
        self.cleanup_thread.start()

    def stop_cache_manager(self):
        """Stop the cache manager"""
        self.is_running = False

        if self.cleanup_thread and self.cleanup_thread.is_alive():
            # Give cleanup thread time to finish
            self.cleanup_thread.join(timeout=2)

        # Shutdown thread pool
        self.thread_pool.shutdown(wait=False)

    def _cleanup_expired_entries_thread(self, interval: int):
        """Background thread to clean up expired cache entries"""
        while self.is_running:
            try:
                time.sleep(interval)

                if not self.is_running:
                    break

                with self._cache_lock:
                    expired_keys = []
                    for cache_key, entry in self.cache.items():
                        if entry.is_expired:
                            expired_keys.append(cache_key)

                    for key in expired_keys:
                        del self.cache[key]
                        # Also clean up the locks
                        if key in self.fetch_locks:
                            del self.fetch_locks[key]
                        if key in self.async_fetch_locks:
                            del self.async_fetch_locks[key]

            except Exception as e:
                print(e)

    # Synchronous version (for use in Django, Flask, etc.)
    def get_data_sync(self, endpoint_name: str,
                      filters: Optional[Dict] = None,
                      ttl: Optional[int] = None,
                      force_refresh: bool = False) -> List[Dict]:
        """
        Synchronous version - get data from cache or fetch from NetBox
        Use this in Django views, Flask routes, etc.
        """
        cache_key = self._get_cache_key(endpoint_name, filters)
        ttl = ttl or self.default_ttl

        # Check cache first (unless force refresh)
        if not force_refresh:
            with self._cache_lock:
                if cache_key in self.cache:
                    entry = self.cache[cache_key]
                    if not entry.is_expired:
                        return entry.data
                    else:
                        # Remove expired entry
                        del self.cache[cache_key]

        # Ensure we have a lock for this cache key
        if cache_key not in self.fetch_locks:
            self.fetch_locks[cache_key] = threading.Lock()

        # Fetch data (with lock to prevent concurrent fetches)
        with self.fetch_locks[cache_key]:
            # Double-check cache in case another thread fetched while we waited
            if not force_refresh:
                with self._cache_lock:
                    if cache_key in self.cache and not self.cache[cache_key].is_expired:
                        return self.cache[cache_key].data

            # Fetch fresh data
            start_time = time.time()

            data = self._fetch_netbox_data_sync(endpoint_name, filters)

            fetch_time = time.time() - start_time

            # Cache the result
            entry = CacheEntry(
                data=data,
                timestamp=time.time(),
                ttl=ttl,
                endpoint_name=endpoint_name,
                filters=filters
            )

            with self._cache_lock:
                self.cache[cache_key] = entry

            return data

    # Async version (for use in async frameworks like FastAPI)
    async def get_data_async(self, endpoint_name: str,
                             filters: Optional[Dict] = None,
                             ttl: Optional[int] = None,
                             force_refresh: bool = False) -> List[Dict]:
        """
        Async version - get data from cache or fetch from NetBox
        Use this in FastAPI, aiohttp, etc.
        """
        cache_key = self._get_cache_key(endpoint_name, filters)
        ttl = ttl or self.default_ttl

        # Check cache first (unless force refresh)
        if not force_refresh:
            with self._cache_lock:
                if cache_key in self.cache:
                    entry = self.cache[cache_key]
                    if not entry.is_expired:
                        return entry.data
                    else:
                        # Remove expired entry
                        del self.cache[cache_key]

        # Ensure we have an async lock for this cache key
        if cache_key not in self.async_fetch_locks:
            self.async_fetch_locks[cache_key] = asyncio.Lock()

        # Fetch data (with lock to prevent concurrent fetches)
        async with self.async_fetch_locks[cache_key]:
            # Double-check cache in case another coroutine fetched while we waited
            if not force_refresh:
                with self._cache_lock:
                    if cache_key in self.cache and not self.cache[cache_key].is_expired:
                        self.logger.info(f"Cache populated by another request for {endpoint_name}")
                        return self.cache[cache_key].data

            # Fetch fresh data in thread pool
            start_time = time.time()

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                self.thread_pool,
                self._fetch_netbox_data_sync,
                endpoint_name,
                filters
            )

            fetch_time = time.time() - start_time

            # Cache the result
            entry = CacheEntry(
                data=data,
                timestamp=time.time(),
                ttl=ttl,
                endpoint_name=endpoint_name,
                filters=filters
            )

            with self._cache_lock:
                self.cache[cache_key] = entry

            return data

    def get_data_streaming_sync(self, endpoint_name: str,
                                filters: Optional[Dict] = None,
                                ttl: Optional[int] = None,
                                force_refresh: bool = False,
                                chunk_size: int = 100) -> Generator[Dict, None, None]:
        """
        Synchronous streaming version
        """
        try:
            data = self.get_data_sync(endpoint_name, filters, ttl, force_refresh)

            # Yield metadata first
            yield {
                "status": "start",
                "endpoint": endpoint_name,
                "total_items": len(data),
                "chunk_size": chunk_size,
                "total_chunks": (len(data) + chunk_size - 1) // chunk_size,
                "from_cache": not force_refresh
            }

            # Stream data in chunks
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                chunk_number = (i // chunk_size) + 1

                yield {
                    "status": "chunk",
                    "chunk_number": chunk_number,
                    "items_in_chunk": len(chunk),
                    "data": chunk
                }

            # Yield completion
            yield {
                "status": "complete",
                "total_items_sent": len(data)
            }

        except Exception as e:
            yield {
                "status": "error",
                "error": str(e),
                "endpoint": endpoint_name
            }

    async def get_data_streaming_async(self, endpoint_name: str,
                                       filters: Optional[Dict] = None,
                                       ttl: Optional[int] = None,
                                       force_refresh: bool = False,
                                       chunk_size: int = 100) -> AsyncGenerator[
        dict[str, str | int | bool] | dict[str, str | int | list[dict]] | dict[str, str | int] | dict[str, str], None]:
        """
        Async streaming version
        """
        try:
            data = await self.get_data_async(endpoint_name, filters, ttl, force_refresh)

            # Yield metadata first
            yield {
                "status": "start",
                "endpoint": endpoint_name,
                "total_items": len(data),
                "chunk_size": chunk_size,
                "total_chunks": (len(data) + chunk_size - 1) // chunk_size,
                "from_cache": not force_refresh
            }

            # Stream data in chunks
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                chunk_number = (i // chunk_size) + 1

                yield {
                    "status": "chunk",
                    "chunk_number": chunk_number,
                    "items_in_chunk": len(chunk),
                    "data": chunk
                }

                # Yield control to allow other coroutines to run
                await asyncio.sleep(0)

            # Yield completion
            yield {
                "status": "complete",
                "total_items_sent": len(data)
            }

        except Exception as e:
            yield {
                "status": "error",
                "error": str(e),
                "endpoint": endpoint_name
            }

    def _fetch_netbox_data_sync(self, endpoint_name: str,
                                filters: Optional[Dict]) -> List[Dict]:
        """Synchronous NetBox data fetch"""
        endpoint= eval(f'self.nb.{endpoint_name}')

        if 'count' in endpoint_name:

            if filters:
                query = eval(f'{endpoint_name}(**filters)')
            else:
                query = eval(f'self.nb.{endpoint_name}()')
        elif filters:
            query = endpoint.filter(**filters)
        else:
            query = endpoint.all()

        # Convert all items to dictionaries
        data = []
        if 'count' in endpoint_name:
            data=[query]
        else:
            for item in query:
                data.append(dict(item))

        return data

    def force_refresh(self, endpoint_name: str, filters: Optional[Dict] = None) -> bool:
        """
        Force refresh of specific endpoint data
        Returns True if cache entry existed, False if not cached
        """
        cache_key = self._get_cache_key(endpoint_name, filters)

        with self._cache_lock:
            if cache_key in self.cache:
                del self.cache[cache_key]
                return True
            else:
                return False

    def clear_cache(self, endpoint_name: Optional[str] = None,
                    filters: Optional[Dict] = None):
        """Clear cache entries"""
        with self._cache_lock:
            if endpoint_name is None:
                # Clear entire cache
                cleared_count = len(self.cache)
                self.cache.clear()
                self.fetch_locks.clear()
                self.async_fetch_locks.clear()
            else:
                if filters is not None:
                    # Clear specific endpoint+filters combination
                    cache_key = self._get_cache_key(endpoint_name, filters)
                    if cache_key in self.cache:
                        del self.cache[cache_key]
                        if cache_key in self.fetch_locks:
                            del self.fetch_locks[cache_key]
                        if cache_key in self.async_fetch_locks:
                            del self.async_fetch_locks[cache_key]
                else:
                    # Clear all entries for this endpoint (any filters)
                    keys_to_remove = [
                        key for key in self.cache.keys()
                        if key.startswith(f"{endpoint_name}:") or key == endpoint_name
                    ]

                    for key in keys_to_remove:
                        del self.cache[key]
                        if key in self.fetch_locks:
                            del self.fetch_locks[key]
                        if key in self.async_fetch_locks:
                            del self.async_fetch_locks[key]



    def get_cache_status(self) -> Dict:
        """Get detailed cache status"""
        with self._cache_lock:
            status = {
                "is_running": self.is_running,
                "default_ttl_seconds": self.default_ttl,
                "total_entries": len(self.cache),
                "entries": {}
            }

            for cache_key, entry in self.cache.items():
                status["entries"][cache_key] = {
                    "endpoint": entry.endpoint_name,
                    "filters": entry.filters,
                    "item_count": len(entry.data),
                    "cached_at": datetime.fromtimestamp(entry.timestamp).isoformat(),
                    "age_seconds": round(entry.age_seconds, 2),
                    "ttl_seconds": entry.ttl,
                    "remaining_ttl_seconds": round(entry.remaining_ttl, 2),
                    "is_expired": entry.is_expired
                }

        return status

    def is_cached(self, endpoint_name: str, filters: Optional[Dict] = None) -> Tuple[bool, Optional[float]]:
        """Check if data is cached and fresh"""
        cache_key = self._get_cache_key(endpoint_name, filters)

        with self._cache_lock:
            if cache_key not in self.cache:
                return False, None

            entry = self.cache[cache_key]
            if entry.is_expired:
                return False, None

            return True, entry.remaining_ttl

    @staticmethod
    def _get_cache_key( endpoint_name: str, filters: Optional[Dict]) -> str:
        """Generate cache key from endpoint and filters"""
        if filters:
            filter_str = json.dumps(filters, sort_keys=True)
            return f"{endpoint_name}:{hash(filter_str)}"
        return endpoint_name


nb:OptimizedNetBoxClient|None=None

class InfrasotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infrasot'
    verbose_name = 'InfraSoT'
    icon='i-lucide-server'

    def ready(self):
        global nb
        nb=OptimizedNetBoxClient(netbox_url=config('INFRASOT_API_URL'),token=config('INFRASOT_API_TOKEN'),default_ttl=300)
        nb.start_cache_manager(cleanup_interval=60)

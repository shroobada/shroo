// app/composables/useApi.ts
import type { UseFetchOptions } from 'nuxt/app'

export const useApi = <T>(
  url: string,
  options: UseFetchOptions<T> = {}
) => {
  return useFetch(url, {
    baseURL: '/api',
    ...options
  })
}

export const useApiPost = <T>(
  url: string,
  body: any,
  options: UseFetchOptions<T> = {}
) => {
  return useFetch(url, {
    baseURL: '/api',
    method: 'POST',
    body,
    ...options
  })
}
// composables/useApi.ts

export const useApi = () => {
  // Endpoint mappings for different resource types
  const endpoints = {
    devices: 'dcim',
    vlans: 'ipam',
    prefixes: 'ipam',
    ip_addresses: 'ipam'
  } as const

  // Health check endpoints
  const healthEndpoints = {
    infrasot: '/back/health',
    orchestrator: '/back/health/orchestrator'
  } as const

  // Fetch count for a specific resource
  async function fetchCount(resource: keyof typeof endpoints): Promise<number> {
    try {
      const endpoint = endpoints[resource]
      const { data } = await useFetch<{ result: number[] }>(`/back/${endpoint}/${resource}/count`, {
        lazy: true
      })
      return data.value?.result?.[0] || 0
    } catch (error) {
      console.error(`Failed to fetch ${resource} count:`, error)
      return 0
    }
  }

  // Fetch all counts for specified resources
  async function fetchAllCounts(resources: (keyof typeof endpoints)[] = Object.keys(endpoints) as (keyof typeof endpoints)[]): Promise<Record<string, number>> {
    const results = await Promise.all(
      resources.map(async resource => ({
        [resource]: await fetchCount(resource)
      }))
    )

    return results.reduce((acc, curr) => ({ ...acc, ...curr }), {})
  }

  // Check health status for a specific service
  async function checkHealthStatus(service: keyof typeof healthEndpoints): Promise<boolean> {
    try {
      const endpoint = healthEndpoints[service]
      const { data } = await useFetch<boolean>(endpoint, {
        lazy: true
      })
      return data.value || false
    } catch (error) {
      console.error(`Failed to check ${service} status:`, error)
      return false
    }
  }

  // Check all health statuses
  async function checkAllHealthStatuses(): Promise<Record<string, boolean>> {
    const results = await Promise.all(
      Object.keys(healthEndpoints).map(async service => ({
        [`${service}Status`]: await checkHealthStatus(service as keyof typeof healthEndpoints)
      }))
    )

    return results.reduce((acc, curr) => ({ ...acc, ...curr }), {})
  }

  // Generic API fetch wrapper
  async function apiFetch<T>(endpoint: string, options?: any): Promise<T | null> {
    try {
      const { data } = await useFetch<T>(endpoint, {
        lazy: true,
        ...options
      })
      return data.value
    } catch (error) {
      console.error(`API fetch failed for ${endpoint}:`, error)
      return null
    }
  }

  return {
    // Endpoints
    endpoints,
    healthEndpoints,

    // Count functions
    fetchCount,
    fetchAllCounts,

    // Health functions
    checkHealthStatus,
    checkAllHealthStatuses,

    // Generic fetch
    apiFetch
  }
}

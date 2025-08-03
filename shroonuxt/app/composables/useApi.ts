// composables/useApi.ts

const ENDPOINTS = {
  devices: 'dcim',
  vlans: 'ipam',
  prefixes: 'ipam',
  ip_addresses: 'ipam',
  object_changes: 'core'
}

function isEndpointKey(value: string): value is keyof typeof ENDPOINTS {
  return value in ENDPOINTS
}

const HEALTHENDPOINTS = {
  infrasot: '/back/health',
  orchestrator: '/back/health/orchestrator'
}

export const useApi = () => {
  // Generic fetch with error handling
  const safeApiFetch = async <T>(resource: keyof typeof ENDPOINTS | string, defaultValue: T, detail = '', options = {}) => {
    try {
      let url = '/back'

      // eslint-disable-next-line @stylistic/max-statements-per-line
      if (isEndpointKey(resource)) { url = `${url}/${ENDPOINTS[resource]}` }

      url = `${url}/${resource}/${detail}`

      const data = await $fetch<T>(url, options)
      return data ?? defaultValue
    } catch (error) {
      console.error(`API fetch failed for ${resource}:`, error)
      return defaultValue
    }
  }
  return {
    ENDPOINTS,
    HEALTHENDPOINTS,
    safeApiFetch
  }
}

import type { Device } from '~/types/infrasot'

interface DeviceFilters {
  nameChunk?: string
  deviceType?: string
  manufacturer?: string
  role?: string
  status?: string
  site?: string
  vlan?: string // From custom_fields.vlan_id
  tag?: string
}

// Individual filter functions
export const filterByNameChunk = (devices: Device[], nameChunk: string): Device[] => {
  if (!nameChunk.trim()) return devices
  return devices.filter(device =>
    device.name.toLowerCase().includes(nameChunk.toLowerCase()) ||
    device.display.toLowerCase().includes(nameChunk.toLowerCase())
  )
}

export const filterByDeviceType = (devices: Device[], deviceType: string): Device[] => {
  if (!deviceType.trim()) return devices
  return devices.filter(device =>
    device.device_type.model.toLowerCase().includes(deviceType.toLowerCase()) ||
    device.device_type.display.toLowerCase().includes(deviceType.toLowerCase())
  )
}

export const filterByManufacturer = (devices: Device[], manufacturer: string): Device[] => {
  if (!manufacturer.trim()) return devices
  return devices.filter(device =>
    device.device_type.manufacturer.name.toLowerCase().includes(manufacturer.toLowerCase())
  )
}

export const filterByRole = (devices: Device[], role: string): Device[] => {
  if (!role.trim()) return devices
  return devices.filter(device =>
    device.role.name.toLowerCase().includes(role.toLowerCase())
  )
}

export const filterByStatus = (devices: Device[], status: string): Device[] => {
  if (!status.trim()) return devices
  return devices.filter(device =>
    device.status.value === status.toLowerCase() ||
    device.status.label.toLowerCase().includes(status.toLowerCase())
  )
}

export const filterBySite = (devices: Device[], site: string): Device[] => {
  if (!site.trim()) return devices
  return devices.filter(device =>
    device.site.name.toLowerCase().includes(site.toLowerCase())
  )
}

export const filterByVlan = (devices: Device[], vlan: string): Device[] => {
  if (!vlan.trim()) return devices
  return devices.filter(device =>
    device.custom_fields.vlan_id === vlan
  )
}

export const filterByTag = (devices: Device[], tag: string): Device[] => {
  if (!tag.trim()) return devices
  return devices.filter(device =>
    device.tags.some(deviceTag =>
      deviceTag.name.toLowerCase().includes(tag.toLowerCase())
    )
  )
}

// Combined filter function
export const filterDevices = (devices: Device[], filters: DeviceFilters): Device[] => {
  let filteredDevices = [...devices]

  if (filters.nameChunk) {
    filteredDevices = filterByNameChunk(filteredDevices, filters.nameChunk)
  }

  if (filters.deviceType) {
    filteredDevices = filterByDeviceType(filteredDevices, filters.deviceType)
  }

  if (filters.manufacturer) {
    filteredDevices = filterByManufacturer(filteredDevices, filters.manufacturer)
  }

  if (filters.role) {
    filteredDevices = filterByRole(filteredDevices, filters.role)
  }

  if (filters.status) {
    filteredDevices = filterByStatus(filteredDevices, filters.status)
  }

  if (filters.site) {
    filteredDevices = filterBySite(filteredDevices, filters.site)
  }

  if (filters.vlan) {
    filteredDevices = filterByVlan(filteredDevices, filters.vlan)
  }

  if (filters.tag) {
    filteredDevices = filterByTag(filteredDevices, filters.tag)
  }

  return filteredDevices
}

// Nuxt composable example for reactive filtering
export const useDeviceFilters = () => {
  const devices = ref<Device[]>([])
  const filters = ref<DeviceFilters>({})

  // Computed filtered devices
  const filteredDevices = computed(() =>
    filterDevices(devices.value, filters.value)
  )

  // Helper functions to update filters
  const setNameFilter = (name: string) => {
    filters.value.nameChunk = name
  }

  const setTypeFilter = (type: string) => {
    filters.value.deviceType = type
  }

  const setManufacturerFilter = (manufacturer: string) => {
    filters.value.manufacturer = manufacturer
  }

  const setRoleFilter = (role: string) => {
    filters.value.role = role
  }

  const setStatusFilter = (status: string) => {
    filters.value.status = status
  }

  const setSiteFilter = (site: string) => {
    filters.value.site = site
  }

  const setVlanFilter = (vlan: string) => {
    filters.value.vlan = vlan
  }

  const setTagFilter = (tag: string) => {
    filters.value.tag = tag
  }

  const clearFilters = () => {
    filters.value = {}
  }
  return {
    devices: readonly(devices),
    filteredDevices: readonly(filteredDevices),
    filters: readonly(filters),
    setNameFilter,
    setTypeFilter,
    setManufacturerFilter,
    setRoleFilter,
    setStatusFilter,
    setSiteFilter,
    setVlanFilter,
    setTagFilter,
    clearFilters
  }
}

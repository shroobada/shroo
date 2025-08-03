<script setup lang="ts">
import { format, isToday } from 'date-fns'
import type { Device } from '~/types/infrasot'

const props = defineProps<{
  devices: Device[]
}>()

const devicesRefs = ref<Element[]>([])
const searchTerm = ref('')

const selectedDevice = defineModel<Device | null>()

// Filter devices based on search term
const filteredDevices = computed(() => {
  if (!searchTerm.value.trim()) {
    return props.devices
  }

  const search = searchTerm.value.toLowerCase()
  return props.devices.filter((device) => {
    // Search in device name and display
    if (device.name?.toLowerCase().includes(search)
      || device.display?.toLowerCase().includes(search)) {
      return true
    }

    // Search in manufacturer and model
    if (device.device_type?.manufacturer?.name?.toLowerCase().includes(search)
      || device.device_type?.model?.toLowerCase().includes(search)) {
      return true
    }

    // Search in role
    if (device.role?.name?.toLowerCase().includes(search)) {
      return true
    }

    // Search in site and location
    if (device.site?.name?.toLowerCase().includes(search)
      || device.location?.name?.toLowerCase().includes(search)) {
      return true
    }

    // Search in IP addresses
    if (device.primary_ip4?.address?.toLowerCase().includes(search)
      || device.primary_ip6?.address?.toLowerCase().includes(search)) {
      return true
    }

    // Search in serial and asset tag
    if (device.serial?.toLowerCase().includes(search)
      || device.asset_tag?.toLowerCase().includes(search)) {
      return true
    }

    // Search in description
    if (device.description?.toLowerCase().includes(search)) {
      return true
    }

    // Search in tags
    if (device.tags?.some(tag => tag.name?.toLowerCase().includes(search))) {
      return true
    }

    return false
  })
})

watch(selectedDevice, () => {
  if (!selectedDevice.value) {
    return
  }
  const ref = devicesRefs.value[selectedDevice.value.id]
  if (ref) {
    ref.scrollIntoView({ block: 'nearest' })
  }
})

defineShortcuts({
  arrowdown: () => {
    const index = filteredDevices.value.findIndex(device => device.id === selectedDevice.value?.id)

    if (index === -1) {
      selectedDevice.value = filteredDevices.value[0]
    } else if (index < filteredDevices.value.length - 1) {
      selectedDevice.value = filteredDevices.value[index + 1]
    }
  },
  arrowup: () => {
    const index = filteredDevices.value.findIndex(device => device.id === selectedDevice.value?.id)

    if (index === -1) {
      selectedDevice.value = filteredDevices.value[filteredDevices.value.length - 1]
    } else if (index > 0) {
      selectedDevice.value = filteredDevices.value[index - 1]
    }
  }
})

// Status color mapping
const getStatusColor = (status: string) => {
  switch (status) {
    case 'active': return 'text-green-500'
    case 'offline': return 'text-red-500'
    case 'planned': return 'text-blue-500'
    case 'staged': return 'text-yellow-500'
    case 'failed': return 'text-orange-500'
    case 'inventory': return 'text-gray-500'
    case 'decommissioning': return 'text-purple-500'
    default: return 'text-gray-400'
  }
}

// Get critical tag indicator
const isCritical = (device: Device) => {
  return device.tags?.some(tag => tag.name?.toLowerCase() === 'critical') || false
}

// Clear search
const clearSearch = () => {
  searchTerm.value = ''
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Search Bar -->
    <div class="p-4 sm:px-6 border-b border-default bg-background/50 backdrop-blur supports-[backdrop-filter]:bg-background/50">
      <div class="relative">
        <UInput
          v-model="searchTerm"
          name="search"
          placeholder="Search devices, IPs, locations..."
          icon="i-lucide-search"
          size="sm"
          color="neutral"
          variant="outline"
          :ui="{ icon: { trailing: { pointer: '' } } }"
        >
          <template #trailing>
            <UButton
              v-show="searchTerm"
              color="neutral"
              variant="link"
              icon="i-lucide-x"
              :padded="false"
              @click="clearSearch"
            />
          </template>
        </UInput>
      </div>

      <!-- Search Results Count -->
      <div v-if="searchTerm.trim()" class="mt-2 text-sm text-muted">
        {{ filteredDevices.length }} of {{ devices.length }} devices
      </div>
    </div>

    <!-- Device List -->
    <div class="flex-1 overflow-y-auto divide-y divide-default">
      <!-- No Results -->
      <div v-if="filteredDevices.length === 0" class="p-8 text-center">
        <UIcon name="i-lucide-search-x" class="size-12 text-dimmed mx-auto mb-4" />
        <p class="text-muted mb-2">
          No devices found
        </p>
        <p class="text-dimmed text-sm">
          {{ searchTerm.trim() ? 'Try adjusting your search terms' : 'No devices available' }}
        </p>
      </div>

      <!-- Device Items -->
      <div
        v-for="(device, index) in filteredDevices"
        :key="device.id"
        :ref="el => { devicesRefs[device.id] = el as Element }"
      >
        <div
          class="p-4 sm:px-6 text-sm cursor-pointer border-l-2 transition-colors"
          :class="[
            selectedDevice && selectedDevice.id === device.id ? 'border-primary bg-primary/10' : 'border-(--ui-bg) hover:border-primary hover:bg-primary/5'
          ]"
          @click="selectedDevice = device"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-3">
              <span class="font-semibold text-highlighted">{{ device.name || device.display || 'Unnamed Device' }}</span>

              <UChip
                v-if="isCritical(device)"
                color="red"
                variant="soft"
                size="sm"
              />

              <UChip
                :color="device.status?.value === 'active' ? 'green' : device.status?.value === 'offline' ? 'red' : 'gray'"
                variant="soft"
                size="sm"
              >
                {{ device.status?.label || 'Unknown' }}
              </UChip>
            </div>

            <span class="text-dimmed">
              {{ isToday(new Date(device.last_updated))
                ? format(new Date(device.last_updated), 'HH:mm')
                : format(new Date(device.last_updated), 'dd MMM')
              }}
            </span>
          </div>

          <div class="flex items-center gap-2 mb-1">
            <span class="text-toned">{{ device.device_type?.manufacturer?.name || 'Unknown' }}</span>
            <span class="text-dimmed">•</span>
            <span class="text-toned">{{ device.device_type?.model || 'Unknown Model' }}</span>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3 text-dimmed">
              <div v-if="device.site?.name" class="flex items-center gap-1">
                <UIcon name="i-lucide-map-pin" class="size-3" />
                <span>{{ device.site.name }}</span>
              </div>

              <div v-if="device.location?.name" class="flex items-center gap-1">
                <UIcon name="i-lucide-building" class="size-3" />
                <span>{{ device.location.name }}</span>
              </div>

              <div v-if="device.primary_ip4?.address" class="flex items-center gap-1">
                <UIcon name="i-lucide-network" class="size-3" />
                <span>{{ device.primary_ip4.address.split('/')[0] }}</span>
              </div>
            </div>

            <div v-if="device.tags && device.tags.length > 0" class="flex items-center gap-1">
              <UIcon
                v-for="tag in device.tags.slice(0, 3)"
                :key="tag.id"
                name="i-lucide-tag"
                class="size-3"
                :style="{ color: `#${tag.color}` }"
              />
              <span v-if="device.tags.length > 3" class="text-dimmed text-xs">
                +{{ device.tags.length - 3 }}
              </span>
            </div>
          </div>

          <p v-if="device.description?.trim()" class="text-dimmed line-clamp-1 mt-1">
            {{ device.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { breakpointsTailwind } from '@vueuse/core'
import type { Device } from '~/types/infrasot'
import DeviceDetail from '~/components/infrasot/deviceDetail.vue'
import DevicesList from '~/components/infrasot/devicesList.vue'

const { safeApiFetch } = useApi()

const tabItems = [{
  label: 'All',
  value: 'all'
}, {
  label: 'Active',
  value: 'active'
}, {
  label: 'Offline',
  value: 'offline'
}, {
  label: 'Critical',
  value: 'critical'
}]
const selectedTab = ref('all')

const devices = await safeApiFetch<Device[]>('devices', [])
// Filter devices based on the selected tab
const filteredDevices = computed(() => {
  switch (selectedTab.value) {
    case 'active':
      return devices.filter(device => device.status?.value === 'active')
    case 'offline':
      return devices.filter(device => device.status?.value === 'offline')
    case 'critical':
      return devices.filter(device =>
        device.tags?.some(tag => tag.name?.toLowerCase() === 'critical') || false
      )
    default:
      return devices
  }
})

const selectedDevice = ref<Device | null>()

const isDevicePanelOpen = computed({
  get() {
    return !!selectedDevice.value
  },
  set(value: boolean) {
    if (!value) {
      selectedDevice.value = null
    }
  }
})

// Reset selected device if it's not in the filtered devices
watch(filteredDevices, () => {
  if (!filteredDevices.value.find(device => device.id === selectedDevice.value?.id)) {
    selectedDevice.value = null
  }
})

const breakpoints = useBreakpoints(breakpointsTailwind)
const isMobile = breakpoints.smaller('lg')
</script>

<template>
  <UDashboardPanel
    id="devices-1"
    :default-size="25"
    :min-size="20"
    :max-size="30"
    resizable
  >
    <UDashboardNavbar title="Devices">
      <template #leading>
        <UDashboardSidebarCollapse />
      </template>
      <template #trailing>
        <UBadge :label="filteredDevices.length" variant="subtle" />
      </template>

      <template #right>
        <UTabs
          v-model="selectedTab"
          :items="tabItems"
          :content="false"
          size="xs"
        />
      </template>
    </UDashboardNavbar>
    <DevicesList v-model="selectedDevice" :devices="filteredDevices" />
  </UDashboardPanel>

  <DeviceDetail v-if="selectedDevice" :device="selectedDevice" @close="selectedDevice = null" />
  <div v-else class="hidden lg:flex flex-1 items-center justify-center">
    <UIcon name="i-lucide-server" class="size-32 text-dimmed" />
  </div>

  <ClientOnly>
    <USlideover v-if="isMobile" v-model:open="isDevicePanelOpen">
      <template #content>
        <DeviceDetail v-if="selectedDevice" :device="selectedDevice" @close="selectedDevice = null" />
      </template>
    </USlideover>
  </ClientOnly>
</template>

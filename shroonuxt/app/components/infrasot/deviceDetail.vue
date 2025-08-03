<script setup lang="ts">
import { format } from 'date-fns'
import type { Device } from '~/types'

defineProps<{
  device: Device
}>()

const emits = defineEmits(['close'])

const dropdownItems = [[{
  label: 'Edit device',
  icon: 'i-lucide-edit'
}, {
  label: 'Clone device',
  icon: 'i-lucide-copy'
}], [{
  label: 'Power on',
  icon: 'i-lucide-power'
}, {
  label: 'Power off',
  icon: 'i-lucide-power-off'
}], [{
  label: 'Delete device',
  icon: 'i-lucide-trash-2'
}]]

const toast = useToast()

const notes = ref('')
const loading = ref(false)

function onSubmit() {
  loading.value = true

  setTimeout(() => {
    notes.value = ''

    toast.add({
      title: 'Notes saved',
      description: 'Device notes have been updated successfully',
      icon: 'i-lucide-check-circle',
      color: 'success'
    })

    loading.value = false
  }, 1000)
}

// Get status color
const getStatusColor = (status: string) => {
  switch (status) {
    case 'active': return 'green'
    case 'offline': return 'red'
    case 'planned': return 'blue'
    case 'staged': return 'yellow'
    case 'failed': return 'orange'
    case 'inventory': return 'gray'
    case 'decommissioning': return 'purple'
    default: return 'gray'
  }
}
</script>

<template>
  <UDashboardPanel id="device-detail">
    <UDashboardNavbar :title="device.name" :toggle="false">
      <template #leading>
        <UButton
          icon="i-lucide-x"
          color="neutral"
          variant="ghost"
          class="-ms-1.5"
          @click="emits('close')"
        />
      </template>

      <template #right>
        <UTooltip text="Console">
          <UButton
            icon="i-lucide-terminal"
            color="neutral"
            variant="ghost"
          />
        </UTooltip>

        <UTooltip text="Edit">
          <UButton icon="i-lucide-edit" color="neutral" variant="ghost" />
        </UTooltip>

        <UDropdownMenu :items="dropdownItems">
          <UButton
            icon="i-lucide-ellipsis-vertical"
            color="neutral"
            variant="ghost"
          />
        </UDropdownMenu>
      </template>
    </UDashboardNavbar>

    <!-- Device Header -->
    <div class="flex flex-col sm:flex-row justify-between gap-4 p-4 sm:px-6 border-b border-default">
      <div class="flex items-start gap-4 sm:my-1.5">
        <div class="flex-shrink-0">
          <div class="size-12 rounded-lg bg-primary/10 flex items-center justify-center">
            <UIcon name="i-lucide-server" class="size-6 text-primary" />
          </div>
        </div>

        <div class="min-w-0 flex-1">
          <div class="flex items-center gap-3 mb-2">
            <h3 class="font-semibold text-highlighted text-lg">
              {{ device.display }}
            </h3>
            <UChip
              :color="getStatusColor(device.status.value)"
              variant="soft"
            >
              {{ device.status.label }}
            </UChip>
          </div>

          <div class="space-y-1">
            <p class="text-muted">
              {{ device.device_type?.manufacturer?.name || 'Unknown' }} {{ device.device_type?.model || 'Unknown Model' }}
            </p>
            <p class="text-muted text-sm">
              Serial: {{ device.serial || 'N/A' }} • Asset: {{ device.asset_tag || 'N/A' }}
            </p>
          </div>
        </div>
      </div>

      <div class="text-right">
        <p class="text-muted text-sm">
          Last updated
        </p>
        <p class="text-sm font-medium">
          {{ format(new Date(device.last_updated), 'dd MMM yyyy HH:mm') }}
        </p>
      </div>
    </div>

    <!-- Device Details -->
    <div class="flex-1 overflow-y-auto">
      <div class="p-4 sm:p-6 space-y-6">

        <!-- Location Information -->
        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-map-pin" class="size-5" />
              <h4 class="font-semibold">Location</h4>
            </div>
          </template>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-if="device.site?.name">
              <p class="text-sm text-muted">Site</p>
              <p class="font-medium">{{ device.site.name }}</p>
            </div>
            <div v-if="device.location?.name">
              <p class="text-sm text-muted">Location</p>
              <p class="font-medium">{{ device.location.name }}</p>
            </div>
            <div v-if="device.rack?.name">
              <p class="text-sm text-muted">Rack</p>
              <p class="font-medium">{{ device.rack.name }}</p>
            </div>
            <div v-if="device.position">
              <p class="text-sm text-muted">Position</p>
              <p class="font-medium">{{ device.position }}</p>
            </div>
          </div>
        </UCard>

        <!-- Network Information -->
        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-network" class="size-5" />
              <h4 class="font-semibold">Network</h4>
            </div>
          </template>

          <div class="space-y-4">
            <div v-if="device.primary_ip4?.address">
              <p class="text-sm text-muted">Primary IPv4</p>
              <p class="font-mono">{{ device.primary_ip4.address }}</p>
            </div>
            <div v-if="device.primary_ip6?.address">
              <p class="text-sm text-muted">Primary IPv6</p>
              <p class="font-mono">{{ device.primary_ip6.address }}</p>
            </div>
            <div v-if="device.oob_ip?.address">
              <p class="text-sm text-muted">Out-of-band IP</p>
              <p class="font-mono">{{ device.oob_ip.address }}</p>
            </div>
          </div>
        </UCard>

        <!-- Technical Specifications -->
        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-cpu" class="size-5" />
              <h4 class="font-semibold">Technical Specifications</h4>
            </div>
          </template>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p class="text-sm text-muted">Interfaces</p>
              <p class="font-medium">{{ device.interface_count }}</p>
            </div>
            <div>
              <p class="text-sm text-muted">Power Ports</p>
              <p class="font-medium">{{ device.power_port_count }}</p>
            </div>
            <div>
              <p class="text-sm text-muted">Console Ports</p>
              <p class="font-medium">{{ device.console_port_count }}</p>
            </div>
            <div>
              <p class="text-sm text-muted">Module Bays</p>
              <p class="font-medium">{{ device.module_bay_count }}</p>
            </div>
          </div>
        </UCard>

        <!-- Role and Platform -->
        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-settings" class="size-5" />
              <h4 class="font-semibold">Configuration</h4>
            </div>
          </template>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-if="device.role?.name">
              <p class="text-sm text-muted">Role</p>
              <p class="font-medium">{{ device.role.name }}</p>
            </div>
            <div v-if="device.platform?.name">
              <p class="text-sm text-muted">Platform</p>
              <p class="font-medium">{{ device.platform.name }}</p>
            </div>
            <div v-if="device.tenant?.name">
              <p class="text-sm text-muted">Tenant</p>
              <p class="font-medium">{{ device.tenant.name }}</p>
            </div>
            <div v-if="device.config_template?.name">
              <p class="text-sm text-muted">Config Template</p>
              <p class="font-medium">{{ device.config_template.name }}</p>
            </div>
          </div>
        </UCard>

        <!-- Tags -->
        <UCard v-if="device.tags && device.tags.length > 0">
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-tags" class="size-5" />
              <h4 class="font-semibold">Tags</h4>
            </div>
          </template>

          <div class="flex flex-wrap gap-2">
            <UChip
              v-for="tag in device.tags"
              :key="tag.id"
              variant="soft"
              :style="{ backgroundColor: `#${tag.color}20`, color: `#${tag.color}` }"
            >
              {{ tag.name }}
            </UChip>
          </div>
        </UCard>

        <!-- Custom Fields -->
        <UCard v-if="device.custom_fields && Object.keys(device.custom_fields).length > 0">
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-list" class="size-5" />
              <h4 class="font-semibold">Custom Fields</h4>
            </div>
          </template>

          <div class="space-y-3">
            <div v-for="(value, key) in device.custom_fields" :key="key">
              <p class="text-sm text-muted capitalize">{{ key.replace(/_/g, ' ') }}</p>
              <p class="font-medium">{{ value }}</p>
            </div>
          </div>
        </UCard>

        <!-- Description -->
        <UCard v-if="device.description?.trim()">
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-file-text" class="size-5" />
              <h4 class="font-semibold">Description</h4>
            </div>
          </template>

          <p class="whitespace-pre-wrap">{{ device.description }}</p>
        </UCard>
      </div>
    </div>

    <!-- Notes Section -->
    <div class="pb-4 px-4 sm:px-6 shrink-0">
      <UCard variant="subtle" class="mt-auto" :ui="{ header: 'flex items-center gap-1.5 text-dimmed' }">
        <template #header>
          <UIcon name="i-lucide-sticky-note" class="size-5" />
          <span class="text-sm truncate">Add notes for {{ device.name }}</span>
        </template>

        <form @submit.prevent="onSubmit">
          <UTextarea
            v-model="notes"
            color="neutral"
            variant="none"
            autoresize
            placeholder="Add maintenance notes, observations, or updates..."
            :rows="3"
            :disabled="loading"
            class="w-full"
            :ui="{ base: 'p-0 resize-none' }"
          />

          <div class="flex items-center justify-between">
            <UTooltip text="Attach file">
              <UButton
                color="neutral"
                variant="ghost"
                icon="i-lucide-paperclip"
              />
            </UTooltip>

            <div class="flex items-center justify-end gap-2">
              <UButton
                color="neutral"
                variant="ghost"
                label="Save draft"
              />
              <UButton
                type="submit"
                color="neutral"
                :loading="loading"
                label="Save notes"
                icon="i-lucide-save"
              />
            </div>
          </div>
        </form>
      </UCard>
    </div>
  </UDashboardPanel>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted} from 'vue'

const { fetchAllCounts, checkHealthStatus } = useApi()

// Labels for display
const labels = {
  society: 'Nom de Societe',
  user: 'Utilisateur',
  version: 'Version',
  devices: 'Devices',
  prefixes: 'Prefix',
  vlans: 'Vlans',
  ip_addresses: 'IP Adresses',
  infrasoTStatus: 'Statut InfraSoT',
  orchStatus: 'Statut Orchestrateur',
  scanResult: 'Resultat du Scan',
  lastScan: 'Dernier Scan'
}

// Static data
const info = {
  society: 'Codefect',
  user: 'Bobby',
  version: '1.0'
}

// Dynamic counts
const counts = reactive({
  devices: 0,
  prefixes: 0,
  vlans: 0,
  ip_addresses: 0
})

// Status data
const status = reactive({
  infrasoTStatus: false,
  orchStatus: false
})

// Scan data
const scan = {
  scanResult: true,
  lastScan: new Date().toLocaleString('fr-FR')
}

// Loading states
const loading = reactive({
  infrasoTStatus: true,
  orchStatus: true
})

// Check InfraSoT status
async function checkInfraSoTStatus() {
  loading.infrasoTStatus = true
  try {
    return await checkHealthStatus('infrasot')
  } finally {
    loading.infrasoTStatus = false
  }
}

// Check orchestrator status
async function checkOrchStatus() {
  loading.orchStatus = true
  try {
    return await checkHealthStatus('orchestrator')
  } finally {
    loading.orchStatus = false
  }
}

// Refresh status function
async function refreshStatus() {
  await Promise.all([
    checkInfraSoTStatus().then(result => status.infrasoTStatus = result),
    checkOrchStatus().then(result => status.orchStatus = result)
  ])
}

// Fetch counts using the composable
async function loadCounts() {
  const results = await fetchAllCounts()
  Object.assign(counts, results)
}

// Export refresh function for parent components
defineExpose({ refreshStatus })

// Status check and auto-refresh (client-side only)
let statusInterval: NodeJS.Timeout | null = null

onMounted(async () => {
  // Load initial counts and status
  await Promise.all([
    loadCounts(),
    checkInfraSoTStatus().then(result => status.infrasoTStatus = result),
    checkOrchStatus().then(result => status.orchStatus = result)
  ])

  // Auto-refresh status every 5 seconds
  statusInterval = setInterval(async () => {
    await refreshStatus()
  }, 5000)
})

// Cleanup interval on component unmount
onUnmounted(() => {
  if (statusInterval) {
    clearInterval(statusInterval)
  }
})

// Stats cards
const stats = [
  { icon: 'i-lucide-users', data: info },
  { icon: 'i-lucide-server', data: counts },
  { icon: 'i-lucide-square-radical', data: status },
  { icon: 'i-lucide-scan-eye', data: scan }
]
</script>

<template>
  <UPageGrid class="lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-px">
    <UPageCard
      v-for="(stat, index) in stats"
      :key="index"
      :icon="stat.icon"
      orientation="vertical"
      to="/customers"
      variant="subtle"
      :ui="{
        container: 'gap-y-1.5',
        wrapper: 'items-start',
        leading: 'p-2.5 rounded-full bg-primary/10 ring ring-inset ring-primary/25 flex-col'
      }"
      class="lg:rounded-none first:rounded-l-lg last:rounded-r-lg hover:z-1"
    >
      <div v-for="([key, value]) in Object.entries(stat.data)" :key="key" class="flex justify-between">
        <span class="font-medium">{{ labels[key as keyof typeof labels] }} :</span>
        <span class="w-20">
          <template v-if="typeof value === 'boolean'">
            <UIcon
              v-if="loading[key as keyof typeof loading]"
              name="i-lucide-refresh-ccw"
              class="h-6 w-6 text-blue-500 animate-spin"
            />
            <UIcon
              v-else
              :name="value ? 'i-lucide-check-check' : 'i-lucide-x'"
              :class="value ? 'text-green-500' : 'text-red-500'"
              class="h-6 w-6"
            />
          </template>
          <template v-else>
            {{ value }}
          </template>
        </span>
      </div>
    </UPageCard>
  </UPageGrid>
</template>

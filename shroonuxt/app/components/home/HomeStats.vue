<script setup lang="ts">
import type { Period, Range, Stat } from '~/types'

const props = defineProps<{
  period: Period
  range: Range
}>()

function excludeTitleAndIcon(obj: InputObject): InputObject {
  const { title, icon, ...rest } = obj
  return rest
}

function formatDate(date) {
  const pad = (n) => n.toString().padStart(2, '0')

  const year = date.getFullYear()
  const month = pad(date.getMonth() + 1) // zero-based months
  const day = pad(date.getDate())

  const hours = pad(date.getHours())
  const minutes = pad(date.getMinutes())
  const seconds = pad(date.getSeconds())

  return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`
}

const keyVerbose: Record<string, string> = {
  society: 'Nom de Societe',
  user: 'Utilisateur',
  version: 'Version',
  devices: 'Devices',
  prefixes: 'Prefix',
  vlans: 'Vlans',
  ips: 'IP Adresses',
  dbStatus: 'Statut BD',
  orchStatus: 'Statut Orchestrateur',
  scanResult: 'Resultat du Scan',
  lastScan: 'Dernier Scan'
}

const baseStats = [{
  icon: 'i-lucide-users',
  society: 'Codefect',
  user: 'Bobby',
  version: '1.0'
}, {
  icon: 'i-lucide-server',
  devices: 0,
  prefixes: 0,
  vlans: 0,
  ips: 0
}, {
  icon: 'i-lucide-square-radical',
  dbStatus: true,
  orchStatus: true
}, {
  icon: 'i-lucide-scan-eye',
  scanResult: true,
  lastScan: formatDate(new Date())
}]
</script>

<template>
  <UPageGrid class="lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-px">
    <UPageCard
      v-for="(stat, index) in baseStats"
      :key="index"
      :icon="stat.icon"
      orientation="vertical"
      to="/customers"
      variant="subtle"
      :ui="{
        container: 'gap-y-1.5',
        wrapper: 'items-start',
        leading: 'p-2.5 rounded-full bg-primary/10 ring ring-inset ring-primary/25 flex-col',
        title: 'font-normal text-muted text-xs uppercase'
      }"
      class="lg:rounded-none first:rounded-l-lg last:rounded-r-lg hover:z-1"
    >
      <div v-for="([key, value]) in Object.entries(excludeTitleAndIcon(stat))" :key="key" class="flex justify-between">
        <span class="font-medium">{{ keyVerbose[key] }} :</span>
        <span class="w-20">{{ value }}</span>
      </div>
    </UPageCard>
  </UPageGrid>
</template>

<script setup lang="ts">
import { eachDayOfInterval, eachWeekOfInterval, eachMonthOfInterval, format, startOfDay, startOfWeek, startOfMonth, subDays, endOfDay } from 'date-fns'
import { VisXYContainer, VisLine, VisAxis, VisArea, VisCrosshair, VisTooltip } from '@unovis/vue'
import type { Period, Range } from '~/types'
import { onMounted } from 'vue'

const { safeApiFetch } = useApi()

const cardRef = useTemplateRef<HTMLElement | null>('cardRef')

const period = ref<Period>('daily')
const range = ref<Range>({
  start: startOfDay(subDays(new Date(), 6)), // 7 days ago at 00:00
  end: endOfDay(new Date()) // today at 23:59
})

type DataRecord = {
  id: number
  date: Date
  user: string
  action: string
  changed_object: string
  changed_object_type: string
}

type ChartDataRecord = {
  date: Date
  count: number
}

const { width } = useElementSize(cardRef)

const data = ref<ChartDataRecord[]>([])
const rawData = ref<DataRecord[]>([])

// Function to get period start date
const getPeriodStart = (date: Date, period: Period): Date => {
  switch (period) {
    case 'daily':
      return startOfDay(date)
    case 'weekly':
      return startOfWeek(date)
    case 'monthly':
      return startOfMonth(date)
    default:
      return startOfDay(date)
  }
}

const loading = ref(true)

const loadData = async () => {
  loading.value = true
  try {
    const objectChanges = await safeApiFetch<any[]>('object_changes', [])

    rawData.value = objectChanges.filter((item) => {
      const itemDate = new Date(item.time)
      return itemDate >= range.value.start && itemDate <= range.value.end
    }).map(item => ({
      id: item.id,
      date: new Date(item.time),
      user: item.user.display,
      action: item.action.label,
      changed_object: item.changed_object?.display ?? item.prechange_data.address,
      changed_object_type: item.changed_object_type
    }))
  } finally {
    loading.value = false
  }
}

watch([period, range], async () => {
  await nextTick()
  await loadData()

  // Get all dates in the period
  const dates = ({
    daily: eachDayOfInterval,
    weekly: eachWeekOfInterval,
    monthly: eachMonthOfInterval
  } as Record<Period, typeof eachDayOfInterval>)[period.value](range.value)

  // Create a map to count activities per period
  const activityCounts = new Map<string, number>()

  // Initialize all periods with 0
  dates.forEach((date) => {
    const key = getPeriodStart(date, period.value).toISOString()
    activityCounts.set(key, 0)
  })

  // Count activities for each period
  rawData.value.forEach((activity) => {
    const periodStart = getPeriodStart(activity.date, period.value)
    const key = periodStart.toISOString()
    const currentCount = activityCounts.get(key) || 0
    activityCounts.set(key, currentCount + 1)
  })

  // Convert to chart data
  data.value = dates.map((date) => {
    const periodStart = getPeriodStart(date, period.value)
    const key = periodStart.toISOString()
    return {
      date: periodStart,
      count: activityCounts.get(key) || 0
    }
  })
}, { immediate: true })

const x = (_: ChartDataRecord, i: number) => i
const y = (d: ChartDataRecord) => d.count

const total = computed(() => rawData.value.length)

const formatNumber = new Intl.NumberFormat('en', { maximumFractionDigits: 0 }).format

const formatDate = (date: Date): string => {
  return ({
    daily: format(date, 'd MMM'),
    weekly: format(date, 'd MMM'),
    monthly: format(date, 'MMM yyy')
  })[period.value]
}

const xTicks = (i: number) => {
  if (i === 0 || i === data.value.length - 1 || !data.value[i]) {
    return ''
  }

  return formatDate(data.value[i].date)
}

const template = (d: ChartDataRecord) => {
  const activityText = d.count === 1 ? 'activity' : 'activities'
  return `${formatDate(d.date)}: ${formatNumber(d.count)} ${activityText}`
}

// Initialize data on mount
onMounted( () => {
  loadData()
})
</script>

<template>
  <UCard ref="cardRef" :ui="{ root: 'overflow-visible', body: '!px-0 !pt-0 !pb-3' }">
    <template #header>
      <div>
        <p class="text-xs text-muted uppercase mb-1.5">
          Total Activities
        </p>
        <p class="text-3xl text-highlighted font-semibold">
          <USkeleton v-if="loading" class="h-9 w-24" />
          <span v-else>{{ formatNumber(total) }}</span>
        </p>
        <HomeDateRangePicker v-model="range" class="-ms-1" />

        <HomePeriodSelect v-model="period" :range="range" />
      </div>
    </template>

    <!-- Loading skeleton for chart -->
    <div v-if="loading" class="h-96 flex items-end justify-between px-6 pb-6 space-x-2">
      <USkeleton class="h-68 w-8" />
      <USkeleton class="h-60 w-8" />
      <USkeleton class="h-76 w-8" />
      <USkeleton class="h-52 w-8" />
      <USkeleton class="h-72 w-8" />
      <USkeleton class="h-64 w-8" />
      <USkeleton class="h-80 w-8" />
      <USkeleton class="h-56 w-8" />
    </div>

    <!-- Chart content -->
    <VisXYContainer
      v-else
      :data="data"
      :padding="{ top: 40 }"
      class="h-96"
      :width="width"
    >
      <VisLine
        :x="x"
        :y="y"
        color="var(--ui-primary)"
      />
      <VisArea
        :x="x"
        :y="y"
        color="var(--ui-primary)"
        :opacity="0.1"
      />

      <VisAxis
        type="x"
        :x="x"
        :tick-format="xTicks"
      />

      <VisCrosshair
        color="var(--ui-primary)"
        :template="template"
      />

      <VisTooltip />
    </VisXYContainer>
  </UCard>

  <HomeActivityTable :data="rawData" :loading="loading"/>
</template>

<style scoped>
.unovis-xy-container {
  --vis-crosshair-line-stroke-color: var(--ui-primary);
  --vis-crosshair-circle-stroke-color: var(--ui-bg);

  --vis-axis-grid-color: var(--ui-border);
  --vis-axis-tick-color: var(--ui-border);
  --vis-axis-tick-label-color: var(--ui-text-dimmed);

  --vis-tooltip-background-color: var(--ui-bg);
  --vis-tooltip-border-color: var(--ui-border);
  --vis-tooltip-text-color: var(--ui-text-highlighted);
}
</style>

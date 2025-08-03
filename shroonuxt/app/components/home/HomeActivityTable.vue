<script setup lang="ts">
import { h, resolveComponent } from 'vue'
import type { TableColumn } from '@nuxt/ui'
import { getPaginationRowModel } from '@tanstack/vue-table'

const table = useTemplateRef('table')

type DataRecord = {
  id: number
  date: Date
  user: string
  action: string
  changed_object: string
  changed_object_type: string
}

const props = defineProps<{
  data: DataRecord[]
  loading?: boolean
}>()

const UBadge = resolveComponent('UBadge')

const tableData = computed(() => {
  // Sort by date descending (most recent first) and limit results
  return [...props.data].sort((a, b) => b.date.getTime() - a.date.getTime())
})

const columns: TableColumn<DataRecord>[] = [
  {
    accessorKey: 'id',
    header: 'ID',
    cell: ({ row }) => `#${row.getValue('id')}`
  },
  {
    accessorKey: 'date',
    header: 'Date',
    cell: ({ row }) => {
      return (row.getValue('date') as Date).toLocaleString('en-US', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      })
    }
  },
  {
    accessorKey: 'user',
    header: 'User'
  },
  {
    accessorKey: 'action',
    header: 'Action',
    cell: ({ row }) => {
      const actionColors = {
        created: 'success' as const,
        updated: 'warning' as const,
        deleted: 'error' as const
      }

      const action = row.getValue('action') as string
      const color = actionColors[action.toLowerCase()] || 'neutral' as const

      return h(UBadge, { class: 'capitalize', variant: 'subtle', color }, () => action)
    }
  },
  {
    accessorKey: 'changed_object',
    header: 'Object',
    cell: ({ row }) => {
      const object = row.getValue('changed_object') as string
      return h('div', { class: 'truncate max-w-32', title: object }, object)
    }
  },
  {
    accessorKey: 'changed_object_type',
    header: () => h('div', { class: 'text-right' }, 'Type'),
    cell: ({ row }) => {
      return h('div', { class: 'text-right font-medium capitalize' }, row.getValue('changed_object_type'))
    }
  }
]

const pagination = ref({
  pageIndex: 0,
  pageSize: 10
})
</script>

<template>
  <div class="w-full space-y-4 pb-4">
  <UTable
    ref="table"
    v-model:pagination="pagination"
    :data="tableData"
    :columns="columns"
      class="shrink-0"
    :ui="{
        base: 'table-fixed border-separate border-spacing-0',
      thead: '[&>tr]:bg-elevated/50 [&>tr]:after:content-none',
      tbody: '[&>tr]:last:[&>td]:border-b-0',
      th: 'first:rounded-l-lg last:rounded-r-lg border-y border-default first:border-l last:border-r',
      td: 'border-b border-default'
    }"
    :pagination-options="{ getPaginationRowModel: getPaginationRowModel() }"
  />
    <div class="flex justify-center border-t border-default pt-4">
      <UPagination
        :default-page="(table?.tableApi?.getState().pagination.pageIndex || 0) + 1"
        :items-per-page="table?.tableApi?.getState().pagination.pageSize"
        :total="table?.tableApi?.getFilteredRowModel().rows.length"
        @update:page="(p) => table?.tableApi?.setPageIndex(p - 1)"
      />
    </div>
  </div>
</template>

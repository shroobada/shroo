<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const { safeApiFetch } = useApi()

const toast = useToast()

const open = ref(false)

const menuData = ref<NavigationMenuItem[]>([])

// Function to fetch and process menu data
const fetchMenuData = async () => {
  try {
    const data = await safeApiFetch<NavigationMenuItem[]>('menu', [])

    // Process the data
    data.map(item =>
      item.children?.map((child) => {
        child.label = labels[child.label] ?? child.label
        return child
      })
    )

    menuData.value = data
  } catch (error) {
    console.error('Failed to fetch menu data:', error)
    menuData.value = []
  }
}

const links = computed(() => {
  if (menuData.value && Array.isArray(menuData.value)) {
    return [menuData.value] // Wrap in array for NavigationMenuItem[][]
  }
  return []
})

const groups = computed(() => [{
  id: 'links',
  label: 'Go to',
  items: links.value.flat()
}])

onMounted(async () => {
  await nextTick()
  await fetchMenuData()

  const cookie = useCookie('cookie-consent')
  if (cookie.value === 'accepted') {
    return
  }

  toast.add({
    title: 'We use first-party cookies to enhance your experience on our website.',
    duration: 0,
    close: false,
    actions: [{
      label: 'Accept',
      color: 'neutral',
      variant: 'outline',
      onClick: () => {
        cookie.value = 'accepted'
      }
    }, {
      label: 'Opt out',
      color: 'neutral',
      variant: 'ghost'
    }]
  })
})
</script>

<template>
  <UDashboardGroup unit="rem">
    <UDashboardSidebar
      id="default"
      v-model:open="open"
      collapsible
      resizable
      class="bg-elevated/25"
      :ui="{ footer: 'lg:border-t lg:border-default' }"
    >
      <template #header="{ collapsed }">
        <TeamsMenu :collapsed="collapsed" />
      </template>

      <template #default="{ collapsed }">
        <UDashboardSearchButton :collapsed="collapsed" class="bg-transparent ring-default" />
        <UNavigationMenu
          v-for="(linkGroup, index) in links"
          :key="index"
          :collapsed="collapsed"
          :items="linkGroup"
          orientation="vertical"
          tooltip
          popover
        />
      </template>

      <template #footer="{ collapsed }">
        <UserMenu :collapsed="collapsed" />
      </template>
    </UDashboardSidebar>

    <UDashboardSearch :groups="groups" />

    <slot />

    <NotificationsSlideover />
  </UDashboardGroup>
</template>

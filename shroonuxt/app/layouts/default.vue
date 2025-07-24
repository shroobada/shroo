<template>
  <UApp>
    <UHeader :links="appConfig.ui_data.header_links">
      <template #logo>
        <UIcon :name="appConfig.ui_data.logo.icon" class="w-6 h-6" />
        <span class="font-bold">{{ appConfig.ui_data.logo.text }}</span>
      </template>
    </UHeader>

    <main>
      <!-- Nuxt automatically handles routing based on pages/ directory -->
      <slot />
    </main>

    <UFooter>
      <template #links>
        <ULink
          v-for="link in appConfig.ui_data.footer.social_links"
          :key="link.to"
          :to="link.to"
          class="text-gray-500 hover:text-gray-900 dark:hover:text-white"
        >
          {{ link.label }}
        </ULink>
      </template>

      <template #center>
        <p class="text-sm text-gray-500">
          {{ appConfig.ui_data.footer.copyright }}
        </p>
      </template>
    </UFooter>
  </UApp>
</template>

<script setup lang="ts">
// Get app configuration (just data for UI components)
const appConfig = useAppConfig()
</script>
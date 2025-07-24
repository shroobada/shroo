<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage/>
    </NuxtLayout>
  </UApp>
</template>

<script setup lang="ts">
// Global head configuration
useHead({
  titleTemplate: '%s - My Nuxt App',
  meta: [
    {name: 'viewport', content: 'width=device-width, initial-scale=1'},
    {name: 'description', content: 'Built with Nuxt 4 and UI Pro'}
  ],
  link: [
    {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'}
  ]
})
</script>
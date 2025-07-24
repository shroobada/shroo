<template>
  <UPage>
    <UPageHeader
      title="Features"
      description="Discover what makes Nuxt 4 + UI Pro special"
    />

    <UPageBody>
      <div class="grid gap-6 md:grid-cols-2">
        <UCard>
          <template #header>
            <h3 class="text-lg font-semibold">Nuxt 4 Improvements</h3>
          </template>

          <UList>
            <UListItem>New app/ directory structure</UListItem>
            <UListItem>Improved data fetching with useAsyncData</UListItem>
            <UListItem>Better TypeScript support</UListItem>
            <UListItem>Faster CLI and development server</UListItem>
          </UList>
        </UCard>

        <UCard>
          <template #header>
            <h3 class="text-lg font-semibold">UI Pro Components</h3>
          </template>

          <UList>
            <UListItem>50+ premium components</UListItem>
            <UListItem>Built-in dark mode support</UListItem>
            <UListItem>Fully accessible design</UListItem>
            <UListItem>Customizable with SCSS</UListItem>
          </UList>
        </UCard>
      </div>
    </UPageBody>
  </UPage>
</template>

<script setup lang="ts">
// SEO meta tags
useSeoMeta({
  title: 'Features',
  description: 'Discover the powerful features of Nuxt 4 and UI Pro'
})
</script>
<template>
  <!-- Hero section with custom SCSS class -->
  <UPageHero
    class="hero-section"
    title="Welcome to Nuxt 4 + UI Pro"
    description="Build beautiful applications with the latest Nuxt and premium UI components"
  >
    <template #headline>
      <UBadge variant="solid" size="lg" class="animate-fade-in-up">
        New in Nuxt 4
      </UBadge>
    </template>

    <template #actions>
      <UButton size="xl" to="/docs">
        Get Started
      </UButton>
      <UButton size="xl" variant="ghost" to="/features">
        Learn More
      </UButton>
    </template>
  </UPageHero>

  <!-- Features section -->
  <UPageSection class="container-custom">
    <UPageGrid>
      <UPageCard
        title="⚡ Fast Development"
        description="New app/ directory structure and improved TypeScript support"
        class="animate-fade-in-up"
      />
      <UPageCard
        title="🎨 Beautiful UI"
        description="50+ premium components ready to use in development mode"
        class="animate-fade-in-up"
      />
      <UPageCard
        title="📱 Responsive"
        description="Mobile-first design with dark mode support"
        class="animate-fade-in-up"
      />
    </UPageGrid>
  </UPageSection>
</template>

<script setup lang="ts">
// Get app configuration
const appConfig = useAppConfig()

// SEO meta tags
useSeoMeta({
  title: 'Home',
  description: appConfig.app.description
})
</script>

<style lang="scss" scoped>
// Component-specific SCSS styles
.hero-section {
  :deep(.hero-section__title) {
    color: white;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
}
</style>
<template>
  <UApp>
    <UPage>
      <UPageHeader>
        <template #headline>
          <UBadge variant="soft" color="red">
            Error {{ error?.statusCode }}
          </UBadge>
        </template>

        <template #title>
          {{ errorMessage }}
        </template>

        <template #description>
          Something went wrong. Please try again or go back to the homepage.
        </template>

        <template #actions>
          <UButton @click="handleError" variant="solid">
            Try Again
          </UButton>
          <UButton to="/" variant="ghost">
            Go Home
          </UButton>
        </template>
      </UPageHeader>
    </UPage>
  </UApp>
</template>

<script setup lang="ts">
import type { NuxtError } from '#app'

// Define props
const props = defineProps<{
  error: NuxtError
}>()

// Error message computation
const errorMessage = computed(() => {
  switch (props.error?.statusCode) {
    case 404:
      return 'Page Not Found'
    case 500:
      return 'Internal Server Error'
    default:
      return 'An Error Occurred'
  }
})

// Error handling
const handleError = () => {
  clearError({ redirect: '/' })
}

// Set page meta
useSeoMeta({
  title: `Error ${props.error?.statusCode}`,
  description: 'An error occurred while loading this page'
})
</script>
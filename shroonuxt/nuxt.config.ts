// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: {enabled: true},
    ssr: true,

    modules: [
        '@nuxt/ui-pro',
    ],

    // Create main sCSS file for customizations
    css: ['~/assets/scss/main.scss'],
      // SCSS configuration
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/scss/variables.scss" as *;'
        }
      }
    }
  },

    // Optional: Customize UI Pro
    uiPro: {
        // Free in development mode - no license needed for dev
        // license: 'your-license-key-for-production'
    },
})

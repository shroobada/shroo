// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui-pro',
    '@vueuse/nuxt'
  ],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/api/**': {
      cors: true,
      // proxy: {
      //   to: process.env.NUXT_PROXY_TARGET || 'http://localhost:8000',
      //   pathRewrite:
      //     {
      //       '^/api/':
      //         ''
      //     },
      //   changeOrigin: true,
      //   secure: (process.env.NUXT_PROXY_SECURE || 'false') === 'true'
      // }
    }
  },

  compatibilityDate: '2024-07-11',

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }

})

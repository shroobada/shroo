// shared/constants.ts
export const APP_CONSTANTS = {
  API_BASE_URL: process.env.NUXT_API_BASE_URL || '/api',
  DEFAULT_LOCALE: 'en',
  SUPPORTED_LOCALES: ['en', 'es', 'fr'],
  CACHE_TTL: 1000 * 60 * 5, // 5 minutes
} as const

export const UI_COLORS = {
  primary: 'emerald',
  secondary: 'blue',
  success: 'green',
  warning: 'yellow',
  error: 'red',
  info: 'blue'
} as const
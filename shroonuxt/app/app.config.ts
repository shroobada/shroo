// app/app.config.ts
export default defineAppConfig({
  // UI Pro theme configuration
  ui: {
    primary: 'emerald',
    gray: 'slate',
    colors: ['emerald', 'blue', 'violet', 'rose'],
    strategy: 'merge'
  },

  // App metadata (not routing - just data for components)
  app: {
    name: 'My Nuxt App',
    description: 'Built with Nuxt 4 and UI Pro',
    version: '1.0.0'
  },

  // UI component data (header/footer links for display only)
  // Note: Nuxt handles actual routing via file-based routing in pages/
  ui_data: {
    logo: {
      text: 'My App',
      icon: 'i-heroicons-cube'
    },
    // These are just for header/footer components, not routing
    header_links: [
      { to: '/', label: 'Home' },
      { to: '/features', label: 'Features' },
      { to: '/docs', label: 'Documentation' },
      { to: '/contact', label: 'Contact' }
    ],
    footer: {
      copyright: '© 2025 My Nuxt App. All rights reserved.',
      social_links: [
        { to: '/privacy', label: 'Privacy Policy' },
        { to: '/terms', label: 'Terms of Service' }
      ]
    }
  }
})
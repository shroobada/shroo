<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'

defineProps<{
  collapsed?: boolean
}>()

const colorMode = useColorMode()
const appConfig = useAppConfig()

const code_colors = ['code-blue', 'code-light-blue', 'code-digoulass-blue', 'code-neutral', 'code-digoulass-neutral', 'code-digoulass-gold', 'code-gold']
const base_colors = ['red', 'orange', 'amber', 'yellow', 'lime', 'green', 'emerald', 'teal', 'cyan', 'sky', 'blue', 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose']
const base_neutrals = ['slate', 'gray', 'zinc', 'neutral', 'stone']
const code_neutrals = ['code-neutral', 'code-digoulass-neutral']

const themeConfig = [
  {
    type: 'primary',
    colors: [base_colors, code_colors],
    content: { align: 'center', collisionPadding: 16 }
  },
  {
    type: 'neutral',
    colors: [base_neutrals, code_neutrals],
    content: { align: 'end', collisionPadding: 16 }
  }
]

const user = ref({
  name: 'Benjamin Canac',
  avatar: {
    src: 'https://github.com/benjamincanac.png',
    alt: 'Benjamin Canac'
  }
})

const items = computed<DropdownMenuItem[][]>(() => ([[{
  type: 'label',
  label: user.value.name,
  avatar: user.value.avatar
}], [{
  label: 'Profile',
  icon: 'i-lucide-user'
}, {
  label: 'Billing',
  icon: 'i-lucide-credit-card'
}, {
  label: 'Settings',
  icon: 'i-lucide-settings',
  to: '/settings'
}], [{
  label: 'Theme',
  icon: 'i-lucide-palette',
  children: themeConfig.map(({ type, colors, content }) => ({
    label: type.charAt(0).toUpperCase() + type.slice(1),
    slot: 'chip',
    chip: type === 'neutral' && appConfig.ui.colors.neutral === 'neutral'
      ? 'old-neutral'
      : appConfig.ui.colors[type],
    content,
    children: colors.flatMap(colorGroup =>
      colorGroup.map(color => ({
        label: color,
        chip: color === 'neutral' && type === 'neutral' ? 'old-neutral' : color,
        slot: 'chip',
        type: 'checkbox',
        checked: appConfig.ui.colors[type] === color,
        onSelect(e) {
          e.preventDefault()
          appConfig.ui.colors[type] = color
        }
      }))
    )
  }))
}, {
  label: 'Appearance',
  icon: 'i-lucide-sun-moon',
  children: [
    { mode: 'light', icon: 'i-lucide-sun' },
    { mode: 'dark', icon: 'i-lucide-moon' },
    { mode: 'system', icon: 'i-lucide-monitor' }
  ].map(({ mode, icon }) => ({
    label: mode.charAt(0).toUpperCase() + mode.slice(1),
    icon,
    type: 'checkbox',
    checked: colorMode.value === mode,
    onSelect(e) {
      e.preventDefault()
      colorMode.preference = mode
    }
  }))
}], [{
  label: 'Log out',
  icon: 'i-lucide-log-out'
}]]))
</script>

<template>
  <UDropdownMenu
    :items="items"
    :content="{ align: 'center', collisionPadding: 12 }"
    :ui="{ content: collapsed ? 'w-48' : 'w-(--reka-dropdown-menu-trigger-width)' }"
  >
    <UButton
      v-bind="{
        ...user,
        label: collapsed ? undefined : user?.name,
        trailingIcon: collapsed ? undefined : 'i-lucide-chevrons-up-down'
      }"
      color="neutral"
      variant="ghost"
      block
      :square="collapsed"
      class="data-[state=open]:bg-elevated"
      :ui="{
        trailingIcon: 'text-dimmed'
      }"
    />

    <template #chip-leading="{ item }">
      <span
        :style="{
          '--chip-light': `var(--color-${(item as any).chip}-500)`,
          '--chip-dark': `var(--color-${(item as any).chip}-400)`
        }"
        class="ms-0.5 size-2 rounded-full bg-(--chip-light) dark:bg-(--chip-dark)"
      />
    </template>
  </UDropdownMenu>
</template>

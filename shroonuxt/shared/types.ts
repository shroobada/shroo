// shared/types.ts
export interface NavigationLink {
  to: string
  label: string
  icon?: string
  children?: NavigationLink[]
}

export interface AppConfig {
  name: string
  description: string
  version: string
}

export interface User {
  id: string
  name: string
  email: string
  avatar?: string
}
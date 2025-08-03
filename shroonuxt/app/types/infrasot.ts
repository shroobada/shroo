// Base interfaces for common structures
interface BaseEntity {
  id: number
  url: string
  display: string
  name: string
}

interface BaseEntityWithDisplayUrl extends BaseEntity {
  display_url: string
}

// Manufacturer interface
interface Manufacturer {
  id: number
  url: string
  display: string
  name: string
  slug: string
  description: string
  devicetype_count: number
}

// Device Type interface
interface DeviceType {
  id: number
  url: string
  display: string
  manufacturer: Manufacturer
  model: string
  slug: string
  description: string
  device_count: number
}

// Role interface
interface Role {
  id: number
  url: string
  display: string
  name: string
  slug: string
  description: string
  device_count: number
  virtualmachine_count: number
  _depth: number
}

// Tenant interface
interface Tenant {
  id: number
  url: string
  display: string
  name: string
  slug: string
  description: string
}

// Platform interface
interface Platform {
  id: number
  url: string
  display: string
  name: string
  slug: string
  description: string
  device_count: number
  virtualmachine_count: number
}

// Site interface
interface Site {
  id: number
  url: string
  display: string
  name: string
  slug: string
  description: string
}

// Location interface
interface Location {
  id: number
  url: string
  display: string
  name: string
  slug: string
  description: string
  rack_count: number
  _depth: number
}

// Rack interface
interface Rack {
  id: number
  url: string
  display: string
  name: string
  description: string
  device_count: number
}

// Face interface
interface Face {
  value: 'front' | 'rear'
  label: 'Front' | 'Rear'
}

// Parent Device interface
interface ParentDevice extends BaseEntityWithDisplayUrl {}

// Status interface
interface Status {
  value: 'offline' | 'active' | 'planned' | 'staged' | 'failed' | 'inventory' | 'decommissioning'
  label: string
}

// Airflow interface
interface Airflow {
  value: 'front-to-rear' | 'rear-to-front' | 'left-to-right' | 'right-to-left' | 'side-to-rear' | 'passive' | 'mixed'
  label: string
}

// IP Family interface
interface IPFamily {
  value: 4 | 6
  label: 'IPv4' | 'IPv6'
}

// IP Address interface
interface IPAddress {
  id: number
  url: string
  display: string
  family: IPFamily
  address: string
  description: string
}

// Cluster interface
interface Cluster {
  id: number
  url: string
  display: string
  name: string
  description: string
  virtualmachine_count: number
}

// Virtual Chassis Master interface
interface VirtualChassisMaster extends BaseEntityWithDisplayUrl {}

// Virtual Chassis interface
interface VirtualChassis {
  id: number
  url: string
  display: string
  name: string
  master: VirtualChassisMaster
  description: string
  member_count: number
}

// Config Template interface
interface ConfigTemplate {
  id: number
  url: string
  display: string
  name: string
  description: string
}

// Tag interface
interface Tag {
  id: number
  url: string
  display_url: string
  display: string
  name: string
  slug: string
  color: string
}

// Custom Fields interface (dynamic object)
interface CustomFields {
  [key: string]: string
}

// Main Device interface
interface Device {
  id: number
  url: string
  display_url: string
  display: string
  name: string
  device_type: DeviceType
  role: Role
  tenant: Tenant
  platform: Platform
  serial: string
  asset_tag: string
  site: Site
  location: Location
  rack: Rack
  position: number
  face: Face
  latitude: number
  longitude: number
  parent_device: ParentDevice
  status: Status
  airflow: Airflow
  primary_ip: IPAddress
  primary_ip4: IPAddress
  primary_ip6: IPAddress
  oob_ip: IPAddress
  cluster: Cluster
  virtual_chassis: VirtualChassis
  vc_position: number
  vc_priority: number
  description: string
  comments: string
  config_template: ConfigTemplate
  config_context: string
  local_context_data: string
  tags: Tag[]
  custom_fields: CustomFields
  created: string // ISO 8601 date string
  last_updated: string // ISO 8601 date string
  console_port_count: number
  console_server_port_count: number
  power_port_count: number
  power_outlet_count: number
  interface_count: number
  front_port_count: number
  rear_port_count: number
  device_bay_count: number
  module_bay_count: number
  inventory_item_count: number
}

// API Response type (array of devices)
type DevicesResponse = Device[]

// Export all types
export type {
  Device,
  DevicesResponse,
  DeviceType,
  Manufacturer,
  Role,
  Tenant,
  Platform,
  Site,
  Location,
  Rack,
  Face,
  ParentDevice,
  Status,
  Airflow,
  IPAddress,
  IPFamily,
  Cluster,
  VirtualChassis,
  VirtualChassisMaster,
  ConfigTemplate,
  Tag,
  CustomFields
}

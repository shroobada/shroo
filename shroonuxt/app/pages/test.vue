<template>
  <div class="w-full h-full">
    <UCard class="h-full">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Network Diagram
          </h3>
          <div class="flex gap-2">
            <UButton
              size="sm"
              variant="soft"
              @click="resetView"
              icon="i-heroicons-arrow-path"
            >
              Reset View
            </UButton>
            <UButton
              size="sm"
              variant="soft"
              @click="togglePhysics"
              :icon="physicsEnabled ? 'i-heroicons-pause' : 'i-heroicons-play'"
            >
              {{ physicsEnabled ? 'Stop' : 'Start' }} Physics
            </UButton>
          </div>
        </div>
      </template>

      <div class="relative">
        <div
          v-if="loading"
          class="absolute inset-0 flex items-center justify-center bg-white/80 dark:bg-gray-900/80 z-10"
        >
          <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin" />
        </div>

        <div
          v-if="error"
          class="p-4 text-center"
        >
          <UAlert
            icon="i-heroicons-exclamation-triangle"
            color="red"
            variant="soft"
            :title="error"
          />
        </div>

        <div
          ref="networkContainer"
          class="w-full h-96 border border-gray-200 dark:border-gray-700 rounded-lg"
          :class="{ 'opacity-50': loading }"
        />
      </div>

      <template #footer v-if="stats">
        <div class="flex justify-between text-sm text-gray-500 dark:text-gray-400">
          <span>Nodes: {{ stats.nodes }}</span>
          <span>Edges: {{ stats.edges }}</span>
        </div>
      </template>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'

interface Props {
  mxfileContent?: string
  mxfileUrl?: string
  height?: string
  physicsConfig?: object
}

const props = withDefaults(defineProps<Props>(), {
  height: '400px',
  physicsConfig: () => ({
    enabled: true,
    stabilization: {
      enabled: true,
      iterations: 100,
      updateInterval: 100,
      onlyDynamicEdges: false,
      fit: true
    },
    barnesHut: {
      gravitationalConstant: -2000,
      centralGravity: 0.3,
      springLength: 95,
      springConstant: 0.04,
      damping: 0.09,
      avoidOverlap: 0.1
    }
  })
})

const networkContainer = ref<HTMLElement>()
const loading = ref(false)
const error = ref<string>('')
const physicsEnabled = ref(true)
const stats = ref<{ nodes: number; edges: number } | null>(null)

let network: any = null
let vis: any = null

// Load vis-network
onMounted(async () => {
  try {
    // Dynamically import vis-network
    const visModule = await import('vis-network/standalone')
    vis = visModule

    if (props.mxfileContent) {
      await parseAndRenderMxFile(props.mxfileContent)
    } else if (props.mxfileUrl) {
      await loadAndParseMxFile(props.mxfileUrl)
    }
  } catch (err) {
    error.value = 'Failed to load vis-network library'
    console.error(err)
  }
})

onUnmounted(() => {
  if (network) {
    network.destroy()
  }
})

// Watch for prop changes
watch(() => props.mxfileContent, (newContent) => {
  if (newContent && vis) {
    parseAndRenderMxFile(newContent)
  }
})

watch(() => props.mxfileUrl, (newUrl) => {
  if (newUrl && vis) {
    loadAndParseMxFile(newUrl)
  }
})

async function loadAndParseMxFile(url: string) {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const content = await response.text()
    await parseAndRenderMxFile(content)
  } catch (err) {
    error.value = `Failed to load mxfile: ${err instanceof Error ? err.message : 'Unknown error'}`
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function parseAndRenderMxFile(content: string) {
  loading.value = true
  error.value = ''

  try {
    const { nodes, edges } = parseMxFile(content)
    renderNetwork(nodes, edges)
    stats.value = { nodes: nodes.length, edges: edges.length }
  } catch (err) {
    error.value = `Failed to parse mxfile: ${err instanceof Error ? err.message : 'Unknown error'}`
    console.error(err)
  } finally {
    loading.value = false
  }
}

function parseMxFile(content: string) {
  const parser = new DOMParser()
  const xmlDoc = parser.parseFromString(content, 'text/xml')

  // Check for parsing errors
  const parseError = xmlDoc.querySelector('parsererror')
  if (parseError) {
    throw new Error('Invalid XML format')
  }

  const nodes: any[] = []
  const edges: any[] = []
  const nodeMap = new Map()

  // Find all mxCell elements
  const cells = xmlDoc.querySelectorAll('mxCell')

  cells.forEach((cell) => {
    const id = cell.getAttribute('id')
    const value = cell.getAttribute('value') || ''
    const style = cell.getAttribute('style') || ''
    const vertex = cell.getAttribute('vertex') === '1'
    const edge = cell.getAttribute('edge') === '1'
    const source = cell.getAttribute('source')
    const target = cell.getAttribute('target')
    const parent = cell.getAttribute('parent')

    if (vertex && id && parent !== '0') {
      // Extract geometry if available
      const geometry = cell.querySelector('mxGeometry')
      let x, y, width, height

      if (geometry) {
        x = parseFloat(geometry.getAttribute('x') || '0')
        y = parseFloat(geometry.getAttribute('y') || '0')
        width = parseFloat(geometry.getAttribute('width') || '30')
        height = parseFloat(geometry.getAttribute('height') || '30')
      }

      // Parse style for color and shape information
      const styleObj = parseStyle(style)

      const node = {
        id: id,
        label: decodeValue(value),
        x: x,
        y: y ? -y : undefined, // Flip Y coordinate as vis-network uses different coordinate system
        size: Math.max(width || 30, height || 30) / 2,
        color: {
          background: styleObj.fillColor || '#e1f5fe',
          border: styleObj.strokeColor || '#01579b',
          highlight: {
            background: styleObj.fillColor || '#b3e5fc',
            border: styleObj.strokeColor || '#0277bd'
          }
        },
        font: {
          color: styleObj.fontColor || '#000000',
          size: parseInt(styleObj.fontSize || '12')
        },
        shape: mapShape(styleObj.shape)
      }

      nodes.push(node)
      nodeMap.set(id, node)
    } else if (edge && source && target) {
      const edgeStyle = parseStyle(style)

      const edgeData = {
        id: id,
        from: source,
        to: target,
        label: decodeValue(value),
        color: {
          color: edgeStyle.strokeColor || '#848484'
        },
        width: parseInt(edgeStyle.strokeWidth || '1'),
        arrows: {
          to: {
            enabled: !edgeStyle.endArrow || edgeStyle.endArrow !== 'none',
            scaleFactor: 1
          }
        },
        smooth: {
          enabled: true,
          type: 'dynamic'
        }
      }

      edges.push(edgeData)
    }
  })

  return { nodes, edges }
}

function parseStyle(styleString: string): Record<string, string> {
  const style: Record<string, string> = {}
  if (!styleString) return style

  const pairs = styleString.split(';')
  pairs.forEach(pair => {
    const [key, value] = pair.split('=')
    if (key && value) {
      style[key.trim()] = value.trim()
    }
  })

  return style
}

function decodeValue(value: string): string {
  if (!value) return ''

  // Basic HTML entity decoding
  const decoded = value
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")

  // Remove basic HTML tags for label display
  return decoded.replace(/<[^>]*>/g, '')
}

function mapShape(shape: string): string {
  const shapeMap: Record<string, string> = {
    'ellipse': 'ellipse',
    'circle': 'circle',
    'rectangle': 'box',
    'rhombus': 'diamond',
    'triangle': 'triangle',
    'hexagon': 'hexagon'
  }

  return shapeMap[shape] || 'box'
}

function renderNetwork(nodes: any[], edges: any[]) {
  if (!networkContainer.value || !vis) return

  const data = {
    nodes: new vis.DataSet(nodes),
    edges: new vis.DataSet(edges)
  }

  const options = {
    physics: {
      ...props.physicsConfig,
      enabled: physicsEnabled.value
    },
    layout: {
      improvedLayout: true,
      clusterThreshold: 150
    },
    interaction: {
      hover: true,
      hoverConnectedEdges: true,
      selectConnectedEdges: false,
      zoomView: true,
      dragView: true
    },
    nodes: {
      borderWidth: 2,
      shadow: {
        enabled: true,
        color: 'rgba(0,0,0,0.2)',
        size: 10,
        x: 2,
        y: 2
      },
      font: {
        size: 12,
        face: 'arial'
      }
    },
    edges: {
      smooth: {
        enabled: true,
        type: 'dynamic',
        roundness: 0.5
      },
      shadow: {
        enabled: true,
        color: 'rgba(0,0,0,0.1)',
        size: 5,
        x: 1,
        y: 1
      }
    }
  }

  // Destroy existing network
  if (network) {
    network.destroy()
  }

  // Create new network
  network = new vis.Network(networkContainer.value, data, options)

  // Add event listeners
  network.on('stabilizationIterationsDone', () => {
    network.setOptions({ physics: { enabled: false } })
    physicsEnabled.value = false
  })

  network.on('click', (params: any) => {
    if (params.nodes.length > 0) {
      console.log('Node clicked:', params.nodes[0])
    }
  })
}

function resetView() {
  if (network) {
    network.fit({
      animation: {
        duration: 1000,
        easingFunction: 'easeInOutQuad'
      }
    })
  }
}

function togglePhysics() {
  physicsEnabled.value = !physicsEnabled.value
  if (network) {
    network.setOptions({
      physics: { enabled: physicsEnabled.value }
    })
  }
}
</script>

<style scoped>
/* Additional styling if needed */
.vis-network {
  outline: none;
}
</style>

<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">MxFile Network Viewer Demo</h1>

    <!-- File upload section -->
    <UCard class="mb-6">
      <template #header>
        <h2 class="text-xl font-semibold">Upload MxFile</h2>
      </template>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">
            Upload .drawio/.mxfile
          </label>
          <input
            type="file"
            accept=".drawio,.mxfile,.xml"
            @change="handleFileUpload"
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>

        <div class="flex gap-4">
          <UButton
            @click="loadSampleDiagram"
            variant="outline"
            icon="i-heroicons-document-text"
          >
            Load Sample Diagram
          </UButton>

          <UButton
            @click="clearDiagram"
            variant="outline"
            color="red"
            icon="i-heroicons-trash"
          >
            Clear
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Network viewer -->
    <div v-if="mxfileContent" class="h-[600px]">
      <MxFileNetworkViewer
        :mxfile-content="mxfileContent"
        :physics-config="physicsConfig"
      />
    </div>

    <UCard v-else class="h-[400px] flex items-center justify-center">
      <div class="text-center text-gray-500">
        <UIcon name="i-heroicons-document-plus" class="w-12 h-12 mx-auto mb-4" />
        <p>No diagram loaded. Upload an mxfile or load a sample to get started.</p>
      </div>
    </UCard>

    <!-- Configuration panel -->
    <UCard class="mt-6">
      <template #header>
        <h3 class="text-lg font-semibold">Physics Configuration</h3>
      </template>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1">Central Gravity</label>
          <URange
            v-model="physicsConfig.barnesHut.centralGravity"
            :min="0"
            :max="1"
            :step="0.1"
          />
          <span class="text-xs text-gray-500">{{ physicsConfig.barnesHut.centralGravity }}</span>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Spring Length</label>
          <URange
            v-model="physicsConfig.barnesHut.springLength"
            :min="50"
            :max="200"
            :step="5"
          />
          <span class="text-xs text-gray-500">{{ physicsConfig.barnesHut.springLength }}</span>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Damping</label>
          <URange
            v-model="physicsConfig.barnesHut.damping"
            :min="0"
            :max="1"
            :step="0.01"
          />
          <span class="text-xs text-gray-500">{{ physicsConfig.barnesHut.damping }}</span>
        </div>
      </div>
    </UCard>
  </div>
</template>

<script setup>
const mxfileContent = ref('')

const physicsConfig = ref({
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

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    mxfileContent.value = e.target.result
  }
  reader.readAsText(file)
}

function loadSampleDiagram() {
  // Sample mxfile content - a simple flowchart
  const sampleMxFile = `<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram>
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="2" value="Start" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="374" y="40" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="3" value="Process Data" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="354" y="120" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="4" value="Decision?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="374" y="220" width="80" height="80" as="geometry" />
        </mxCell>
        <mxCell id="5" value="Action A" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="250" y="340" width="100" height="50" as="geometry" />
        </mxCell>
        <mxCell id="6" value="Action B" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="470" y="340" width="100" height="50" as="geometry" />
        </mxCell>
        <mxCell id="7" value="End" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="374" y="440" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="8" value="" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="2" target="3">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="390" y="250" as="sourcePoint" />
            <mxPoint x="440" y="200" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="9" value="" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="3" target="4">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="390" y="250" as="sourcePoint" />
            <mxPoint x="440" y="200" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="10" value="" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="4" target="5">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="390" y="250" as="sourcePoint" />
            <mxPoint x="440" y="200" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="11" value="" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="4" target="6">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="390" y="250" as="sourcePoint" />
            <mxPoint x="440" y="200" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="12" value="" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="5" target="7">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="390" y="250" as="sourcePoint" />
            <mxPoint x="440" y="200" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="13" value="" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="6" target="7">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="390" y="250" as="sourcePoint" />
            <mxPoint x="440" y="200" as="targetPoint" />
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>`

  mxfileContent.value = sampleMxFile
}

function clearDiagram() {
  mxfileContent.value = ''
}
</script>

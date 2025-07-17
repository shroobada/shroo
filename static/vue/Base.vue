<script setup>
import {reactive} from 'vue'

export const currentScope = reactive({
  scope: null,
})

</script>
<template>
    <component :is="currentScope"/>
</template>

<style scoped></style>

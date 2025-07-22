<script setup>
import { ref, onMounted } from 'vue';
import AppMenuItem from './AppMenuItem.vue';

const model = ref([{ label: 'skeleton' }]);
const loading = ref(true);
const apiBaseUrl = import.meta.env.SHROO_API_BASE_URL || 'http://localhost:80';

const fetchMenuItems = async () => {
    try {
        const response = await fetch(`${apiBaseUrl}/api/menu/`);
        const data = await response.json();
        if (data.length === 0) throw new Error('No menu items found');
        model.value = data;
    } catch (error) {
        console.error('Failed to fetch menu items:', error);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchMenuItems();
});
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>

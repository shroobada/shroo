<script setup>
import BestSellingWidget from '@BestSellingWidget.vue';
import NotificationsWidget from '@4.3.6NotificationsWidget.vue';
import RecentSalesWidget from '@4.3.6RecentSalesWidget.vue';
import RevenueStreamWidget from '@4.3.6RevenueStreamWidget.vue';
import StatsWidget from '@4.3.6StatsWidget.vue';

import currentScope from './Base.vue';
currentScope.scope = 'home';
</script>

<template>
    <div class="grid grid-cols-12 gap-8">
        <StatsWidget />

        <div class="col-span-12 xl:col-span-6">
            <RecentSalesWidget />
            <BestSellingWidget />
        </div>
        <div class="col-span-12 xl:col-span-6">
            <RevenueStreamWidget />
            <NotificationsWidget />
        </div>
    </div>
</template>
<script setup>
import { initializeMessaging } from '@/service/Messaging';
import { onBeforeMount, onMounted } from 'vue';

onBeforeMount(async () => {});

onMounted(() => {
    initializeMessaging();
});
</script>

<template>
    <router-view />
</template>

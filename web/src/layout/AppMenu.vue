<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Chat',
        items: [
            { label: 'Novo Chat', icon: 'pi pi-file-edit', to: '/' },
            { label: 'Pesquisar chats', icon: 'pi pi-search', to: '/' },

        ]
    },   
    {
        label:'Chats',
        items: [
            { label: 'Exemplo',  to: '/' },
        ]
    },   
    ]);


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

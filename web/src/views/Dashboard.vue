<template>
    <div class="flex flex-col space-y-5 items-center justify-center">
        <!-- <div class="w-10/12 h-auto flex flex-col item-center justify-center p-2 bg-[#444444] rounded-md">
             <h1 class="text-white text-2xl">Titulo</h1>
             <p class="text-white">Resposta</p>
        </div> -->


        <Panel class="mx-12">
            <template #header>
                <div class="flex items-center gap-2">
                    <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle" />
                    <span class="font-bold">AI ICware</span>
                </div>
            </template>
            <template #footer>
                <div class="flex flex-wrap items-center justify-between gap-4">
                    <span class="text-surface-500 dark:text-surface-400">Updated 2 hours ago</span>
                    <div class="flex item-center p-4">
                        <Button label="Copiar" />
                    </div>
                </div>
            </template>
            <p class="m-0">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                dolore magna
                aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                Excepteur
                sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>

        </Panel>

        <Panel class="mx-12">
            <template #header>
                <div class="flex items-center gap-2">
                    <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle" />
                    <span class="font-bold">Usuário</span>
                </div>
            </template>
            <template #footer>
                <div class="flex flex-wrap items-center justify-between gap-4">
                    <span class="text-surface-500 dark:text-surface-400">Updated 2 hours ago</span>
                </div>
            </template>
            <p class="m-0">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                dolore magna
                aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                Excepteur
                sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>

        </Panel>


       <div class="w-10/12 min-h-32 flex flex-col justify-center rounded-2xl shadow-md fixed bottom-20 p-5 bg-[#e6ebf3]">
    <FloatLabel variant="on" class="mt-5">
        <Textarea id="on_label" v-model="CheckText" class="w-full resize-none max-h-40" autoResize rows="1" />
        <label for="on_label">Pergunte-me alguma coisa.</label>
    </FloatLabel>

    <div class="w-full flex items-center justify-between p-4">
        <div class="flex items-center justify-center px-2 gap-4">
            <span class="pi pi-plus text-4xl hover:cursor-pointer"></span>
            <span class="pi pi-sliders-h text-4xl hover:cursor-pointer"></span>
            <p>Ferramentas</p>
        </div>
        <div v-if="(Status = true)" class="flex item-center p-2 gap-4">
            <span class="pi pi-microphone flex items-center justify-center w-10 h-10 hover:cursor-pointer text-4xl bg-[#bcbcca] rounded-full"></span>
            <span :class="isTextPresent ? 'pi pi-send' : 'pi pi-microchip-ai' " class="flex items-center justify-center w-10 h-10 hover:cursor-pointer text-4xl bg-[#bcbcca] rounded-full"></span>
        </div>
    </div>
</div>

    </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const CheckText = ref(''); 

const isTextPresent = computed(() => CheckText.value.trim().length >0);

</script>


<style lang="scss" scoped></style>
<template>
    <div class="flex flex-col space-y-5 items-center justify-center mb-60 overflow-x-hidden">

        <!-- Painel IA -->
        <Panel class="w-full max-w-4xl mx-4">
            <template #header>
                <div class="flex items-center gap-2">
                    <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle" />
                    <span class="font-bold">AI ICware</span>
                </div>
            </template>
            <template #footer>
                <div class="flex flex-wrap items-center justify-between gap-4">
                    <span class="text-surface-500 dark:text-surface-400">Resposta: 06/07/2024 às 04:03</span>
                    <div class="flex items-center p-4">
                        <Button label="Copiar" />
                    </div>
                </div>
            </template>
            <p class="m-0">
                Lorem ipsum dolor sit amet...
            </p>
        </Panel>

        <!-- Painel Usuário -->
        <Panel class="w-full max-w-4xl mx-4">
            <template #header>
                <div class="w-full flex flex-row-reverse items-center gap-2">
                    <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle" />
                    <span class="font-bold">Usuário</span>
                </div>
            </template>
            <template #footer>
                <div class="flex flex-wrap items-center justify-between gap-4">
                    <span class="text-surface-500 dark:text-surface-400">Pergunta: 06/07/2024 às 04:03</span>
                </div>
            </template>
            <p class="m-0">
                Lorem ipsum dolor sit amet...
            </p>
        </Panel>

        <!-- Input fixo -->
        <div
            class="w-full max-w-4xl min-h-32 flex flex-col justify-center rounded-2xl shadow-md fixed bottom-20 p-5 bg-[#e6ebf3] mx-4">
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
                <div class="flex items-center p-2 gap-4">
                    <span
                        class="pi pi-microphone flex items-center justify-center w-10 h-10 hover:cursor-pointer text-4xl bg-[#bcbcca] rounded-full"></span>
                    <span :class="isTextPresent ? 'pi pi-send' : 'pi pi-microchip-ai'"
                        class="flex items-center justify-center w-10 h-10 hover:cursor-pointer text-4xl bg-[#bcbcca] rounded-full"></span>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { computed, ref } from 'vue';

const CheckText = ref('');

const isTextPresent = computed(() => CheckText.value.trim().length > 0);

</script>


<style lang="scss" scoped></style>
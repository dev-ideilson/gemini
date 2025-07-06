<script setup>
defineProps({
    message: Object
});
</script>

<template>
    <div
        :class="[
            'flex items-start gap-3 p-3 rounded-xl shadow-sm max-w-[80%] whitespace-pre-wrap',
            message.sender === 'user'
                ? 'bg-green-100 dark:bg-green-800 text-green-900 dark:text-green-100 self-end'
                : message.isError
                  ? 'bg-red-100 dark:bg-red-800 text-red-900 dark:text-red-100 self-start'
                  : 'bg-blue-100 dark:bg-blue-800 text-blue-900 dark:text-blue-100 self-start'
        ]"
    >
        <Avatar
            v-if="message.sender !== 'system'"
            :image="message.sender === 'user' ? 'https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png' : 'https://primefaces.org/cdn/primevue/images/avatar/onyamalimba.png'"
            shape="circle"
            class="flex-shrink-0 w-8 h-8"
        />

        <div>
            <div class="font-semibold text-xs mb-1 opacity-70">
                {{ message.sender === 'user' ? 'Você' : message.sender === 'ai' ? 'IA ICware' : 'Sistema' }}
            </div>

            <!-- Destaca blocos de código -->
            <div v-if="message.text.includes('```')" class="text-sm font-mono bg-black/5 dark:bg-white/10 p-2 rounded overflow-x-auto">
                <pre v-html="formatCode(message.text)" />
            </div>
            <p v-else class="text-sm leading-relaxed whitespace-pre-line">{{ message.text }}</p>

            <div class="text-[10px] text-gray-500 dark:text-gray-400 mt-1 text-right">
                {{ new Date(message.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) }}
            </div>
        </div>
    </div>
</template>

<script>
function formatCode(text) {
    const codeBlock = text.match(/```(.*?)```/s);
    if (codeBlock) {
        const code = codeBlock[1].trim();
        return `<code>${code.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code>`;
    }
    return text;
}
</script>

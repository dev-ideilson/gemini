<script setup>
import { MessageError } from '@/service/Messaging';
import { httpAuth } from '@/service/requests/auth';
import { on, send } from '@/socket';
import { useAuthStore } from '@/stores/AuthStore';
import { computed, nextTick, onMounted, ref } from 'vue'; // Importe nextTick

const auth = useAuthStore();
const prompt = ref('');
// 1. Array para armazenar as mensagens
const messages = ref([]);
const chatContainer = ref(null); // Ref para o container do chat para scroll

const isTextPresent = computed(() => prompt.value.trim().length > 0);

// Função para rolar para o final do chat
const scrollToBottom = () => {
    nextTick(() => {
        if (chatContainer.value) {
            chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
        }
    });
};

const sessionId = ref(localStorage.getItem('chat_session_id') || '');

if (!sessionId.value) {
    sessionId.value = crypto.randomUUID();
    localStorage.setItem('chat_session_id', sessionId.value);
}

async function on_generation() {
    if (!isTextPresent.value) return;

    const userMessage = prompt.value; // Captura a mensagem do usuário antes de limpar o input
    prompt.value = ''; // Limpa o input imediatamente

    // 2. Adiciona a mensagem do usuário ao histórico instantaneamente
    messages.value.push({
        sender: 'user',
        text: userMessage,
        timestamp: new Date()
    });
    scrollToBottom(); // Rola para a nova mensagem do usuário

    try {
        const namespace = 'core/';

        on(namespace, 'error', (data) => {
            MessageError(data);
        });

        on(namespace, 'chat.ai.response', (data) => {
            if (data.session_id && data.session_id !== sessionId.value) {
                sessionId.value = data.session_id;
                localStorage.setItem('chat_session_id', data.session_id);
            }

            messages.value.push({
                sender: 'ai',
                text: data.message,
                timestamp: new Date()
            });
            scrollToBottom();
        });

        await send(namespace, 'chat.ai.generate', {
            prompt: userMessage,
            session_id: sessionId.value
        });
    } catch (error) {
        MessageError(error);
        // Opcional: Adicionar uma mensagem de erro ao chat se a chamada falhar
        messages.value.push({
            sender: 'system', // ou 'error'
            text: 'Erro ao enviar a mensagem. Tente novamente.',
            timestamp: new Date(),
            isError: true
        });
        scrollToBottom();
    }
}

onMounted(async () => {
    try {
        const { data } = await httpAuth.auth_get_session(sessionId.value);

        messages.value = data.map((msg) => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
        }));
        scrollToBottom();
    } catch (error) {
        console.error('Erro ao carregar histórico:', error);
    }
});
</script>

<template>
    <div class="flex flex-col h-full overflow-hidden relative">
        <div ref="chatContainer" class="flex flex-col space-y-4 w-full max-w-4xl px-4 pt-6 pb-36 mx-auto overflow-y-hidden flex-grow">
            <div v-for="(message, index) in messages" :key="index" :class="{ 'flex justify-end': message.sender === 'user', 'flex justify-start': message.sender === 'ai' }">
                <div
                    :class="[
                        'flex items-start gap-3 p-3 rounded-lg shadow max-w-[75%]',
                        {
                            'bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100': message.sender === 'ai',
                            'bg-green-100 dark:bg-green-900 text-green-900 dark:text-green-100': message.sender === 'user',
                            'bg-red-100 dark:bg-red-900 text-red-900 dark:text-red-100': message.isError
                        }
                    ]"
                >
                    <Avatar v-if="message.sender === 'ai'" image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle" class="flex-shrink-0 w-8 h-8" />

                    <div>
                        <div :class="['font-bold text-sm', { 'text-right': message.sender === 'user' }]">
                            {{ message.sender === 'ai' ? 'AI ICware' : `${auth.user.first_name}` }}
                        </div>
                        <p class="mt-1 text-base m-0 whitespace-pre-wrap">{{ message.text }}</p>
                        <div class="text-xs mt-1" :class="{ 'text-right': message.sender === 'user', 'text-gray-500 dark:text-gray-400': !message.isError, 'text-red-700 dark:text-red-300': message.isError }">
                            {{ new Date(message.timestamp).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' }) }} às {{ new Date(message.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) }}
                        </div>
                    </div>

                    <Avatar v-if="message.sender === 'user'" image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle" class="flex-shrink-0 w-8 h-8" />
                </div>
            </div>
            <div class="h-24"></div>
        </div>

        <div class="fixed bottom-0 left-0 right-0 w-full flex justify-center p-4 bg-white dark:bg-gray-800 shadow-lg border-t border-gray-200 dark:border-gray-700 z-10">
            <div class="w-full max-w-4xl flex flex-col rounded-xl overflow-hidden">
                <div class="relative flex items-center gap-4 w-full">
                    <Textarea
                        id="chat_input"
                        v-model="prompt"
                        class="w-full resize-none pr-12 rounded-xl border-gray-300 dark:border-gray-600 focus:ring focus:ring-blue-200 focus:border-blue-300 dark:focus:ring-blue-700 dark:focus:border-blue-600 p-3"
                        autoResize
                        rows="1"
                        placeholder="Pergunte-me alguma coisa..."
                        @keyup.enter.prevent="on_generation()"
                    />
                    <Button
                        :icon="isTextPresent ? 'pi pi-send' : 'pi pi-microphone'"
                        :class="[
                            'absolute p-0 w-9 h-9 flex items-center justify-center rounded-full',
                            isTextPresent ? 'bg-blue-500 hover:bg-blue-600 text-white' : 'bg-gray-300 hover:bg-gray-400 text-gray-700 dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-gray-200'
                        ]"
                        @click="on_generation()"
                        aria-label="Send message"
                        :disabled="!isTextPresent"
                    />
                </div>

                <div class="flex items-center justify-between p-2 mt-2">
                    <div class="flex items-center gap-4 text-gray-600 dark:text-gray-300">
                        <span class="pi pi-plus text-xl hover:text-blue-500 dark:hover:text-blue-400 cursor-pointer" title="Adicionar Anexo"></span>
                        <span class="pi pi-sliders-h text-xl hover:text-blue-500 dark:hover:text-blue-400 cursor-pointer" title="Configurações"></span>
                        <span class="text-sm">Ferramentas</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped></style>

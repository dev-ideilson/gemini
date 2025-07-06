# api/core/handlers/ai.py
from api.core.sockets.registry import register_handler
from api.core.tasks.tasks_core import run_gemini_generate_task

@register_handler("chat.ai.generate")
async def handle_chat_gemini_send(consumer, payload):
    prompt = payload.get("prompt", "")
    user_group = consumer.channel_group_name  # já existe no seu WsConsumer

    # Chama Celery com o prompt e group name do usuário
    run_gemini_generate_task.delay(prompt, user_group)

    await consumer.send_json({
        "type": "chat.ai.status",
        "message": "Geração iniciada, aguarde...",
        "payload": {}
    })
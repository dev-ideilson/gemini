# api/core/tasks/task_core.py
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from api.core.classes.google_genai import GoogleGenAI
from api.core.models.models_app import ChatSession, ChatMessage
import logging
import traceback

logger = logging.getLogger(__name__)

@shared_task(name='tasks_gemini_genereate.run_task', queue='default')
def run_gemini_generate_task(prompt_text, user_group, session_id=None):
    try:
        # Obter camada de canal
        channel_layer = get_channel_layer()

        # Inicializar IA e sessão
        genai = GoogleGenAI()
        session = genai.get_or_create_session(session_id)

        # Salvar mensagem do usuário no histórico
        ChatMessage.objects.create(session=session, sender='user', text=prompt_text)

        # Gerar resposta com histórico (o próprio método já salva a resposta da IA)
        result = genai.generate(prompt_text=prompt_text, session_id=session.session_id)

        if result:
            async_to_sync(channel_layer.group_send)(
                user_group,
                {
                    "type": "chat.gemini.response",
                    "message": result["message"],
                    "session_id": result["session_id"]
                }
            )
        else:
            async_to_sync(channel_layer.group_send)(
                user_group,
                {
                    "type": "chat.gemini.response",
                    "message": "Não foi possível gerar uma resposta.",
                    "session_id": session.session_id
                }
            )

    except Exception as e:
        async_to_sync(channel_layer.group_send)(
            user_group,
            {
                "type": "chat.gemini.response",
                "message": f"Erro: {str(e)}\n{traceback.format_exc()}",
                "session_id": session_id or ''
            }
        )
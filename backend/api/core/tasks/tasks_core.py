# api/core/tasks/task_core.py
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from api.core.classes.google_genai import GoogleGenAI

import logging

logger = logging.getLogger(__name__)

@shared_task(name='tasks_gemini_genereate.run_task', queue='default')
def run_gemini_generate_task(prompt_text, user_group):
    try:
        channel_layer = get_channel_layer()
        
        genai = GoogleGenAI()
        response = genai.generate(prompt_text)

        async_to_sync(channel_layer.group_send)(
            user_group,
            {
                "type": "chat.gemini.response",
                "message": response
            }
        )

    except Exception as e:
        async_to_sync(channel_layer.group_send)(
            user_group,
            {
                "type": "chat.gemini.response",
                "message": f"Erro: {str(e)}"
            }
        )
from celery import shared_task

import logging

logger = logging.getLogger(__name__)

@shared_task(bind=False, name='tasks_gemini_genereate.run_task', queue='gemini_generate', max_retries=3, default_retry_delay=10)
def run_gemini_generate_task(prompt_text: str, max_output_tokens: int = 1024, temperature: float = 0.2, top_p: float = 0.8):
    """
    Celery task to generate text using Google GenAI.
    """
    from api.core.classes.google_genai import GoogleGenAI

    try:
        genai = GoogleGenAI()
        response = genai.generate(prompt_text, max_output_tokens, temperature, top_p)
        return response
    except Exception as e:
        logger.error(f"Error in run_gemini_generate_task: {e}")
        raise e
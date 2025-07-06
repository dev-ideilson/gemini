# api/core/classes/google_genai.py
import json
import logging
import traceback
import requests
import google.generativeai as genai
from api.core.models.models_app import Settings, ChatMessage, ChatSession
import uuid

looger = logging.getLogger(__name__)

PRE_PROMPT = """
You are a helpful and friendly AI assistant dedicated to assisting users by understanding their questions thoroughly and providing clear, accurate, and practical answers.

Always aim to make your responses easy to understand and directly useful to the user.

"""

class GoogleGenAI:
    def __init__(self, api_key: str=None, model: str=''):
        self.api_key = api_key if api_key else Settings.get_value('genai_api_key')
        self.model = model if model else Settings.get_value('genai_model','gemini-2.5-flash')
        self.language = Settings.get_value('genai_language', 'pt-br')
        
        if not self.api_key:
            raise ValueError("API key is required for Google GenAI")
        
    def generate(self, prompt_text:str, session_id: str = None):
        """
        Generates text using Google GenAI.
        """
        try:
            
                        # Formato esperado pelo Gemini para o histórico
            session = self.get_or_create_session(session_id)
            chat_history = self.get_chat_history(session)
            
            formatted_history = [
                {
                    'role': 'user' if m.sender == 'user' else 'model',
                    'parts': [{'text': m.text}]
                } for m in chat_history
            ]      
            
            genai.configure(api_key=self.api_key)
            model_instance = genai.GenerativeModel(self.model)
            chat = model_instance.start_chat(history=formatted_history)
           
            
            response = chat.send_message(f"""

{PRE_PROMPT}

Respond entirely in {self.language}.

User's query: {prompt_text}
""")
            
            if hasattr(response, 'text') and response.text.strip():
                # Salva mensagens
                ChatMessage.objects.create(session=session, sender='user', text=prompt_text)
                ChatMessage.objects.create(session=session, sender='ai', text=response.text.strip())
                return {
                    'message': response.text.strip(),
                    'session_id': session.session_id
                }

            return None
        
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            looger.error(f"Error generating text: {e}")
            looger.error(traceback.format_exc())
            return None

    def get_chat_history(self, session: ChatSession, limit: int = 20):
        messages = ChatMessage.objects.filter(session=session).order_by('-timestamp')[:limit]
        return reversed(messages)  # do mais antigo ao mais novo
      
    def get_or_create_session(self, session_id: str = None) -> ChatSession:
        if session_id:
            session, _ = ChatSession.objects.get_or_create(session_id=session_id)
        else:
            session_id = uuid.uuid4().hex
            session = ChatSession.objects.create(session_id=session_id)
        return session
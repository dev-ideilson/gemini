# api/core/classes/google_genai.py
import json
import logging
import traceback
import requests
import google.generativeai as genai
from api.core.models.models_app import Settings

looger = logging.getLogger(__name__)

class GoogleGenAI:
    def __init__(self, api_key: str=None, model: str='gemini-1.5-flash'):
        self.api_key = api_key if api_key else Settings.get_value('genai_api_key')
        self.model = model if model else Settings.get_value('google_genai_model','gemini-2.5-flash')
        self.language = Settings.get_value('google_genai_language', 'pt-br')
        
        if not self.api_key:
            raise ValueError("API key is required for Google GenAI")
        
    def generate(self, prompt_text:str):
        """
        Generates text using Google GenAI.
        """
        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(f"""
You are a helpful and friendly AI assistant dedicated to assisting users by understanding their questions thoroughly and providing clear, accurate, and practical answers.

Always aim to make your responses easy to understand and directly useful to the user.

Respond entirely in {self.language}.

User's query: {prompt_text}
""")
            
            if response and hasattr(response, 'text') and response.text.strip():
                return response.text.strip()
            
            return None
        
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            looger.error(f"Error generating text: {e}")
            looger.error(traceback.format_exc())
            return None
        

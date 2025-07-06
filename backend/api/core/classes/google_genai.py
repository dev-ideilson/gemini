import json
import logging
import traceback
import requests
import google.generativeai as genai
from google.generativeai import GenerationConfig
from api.core.models.models_app import Settings

looger = logging.getLogger(__name__)

class GoogleGenAI:
    def __init__(self, api_key: str=None, model: str='gemini-1.5-flash'):
        self.api_key = api_key if api_key else Settings.get_value('genai_api_key')
        self.model = model if model else Settings.get_value('google_genai_model','gemini-2.5-flash')
        self.language = Settings.get_value('google_genai_language', 'pt-br')
        
        if not self.api_key:
            raise ValueError("API key is required for Google GenAI")
        
    def generate(self, prompt_text:str, max_output_tokens:int=1024, temperature:float=0.2, top_p:float=0.8):
        """
        Generates text using Google GenAI.
        """
        try:
            genai.configure(api_key=self.api_key)
            
            generation_config = GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                top_p=top_p
            )
            
            response = genai.generate_text(
                model=self.model,
                prompt=prompt_text,
                generation_config=generation_config
            )
            
            return response.text
        
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            looger.error(f"Error generating text: {e}")
            looger.error(traceback.format_exc())
            return None
        

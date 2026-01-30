"""
Base class for AI-powered email processors to eliminate code duplication
"""
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any
from config import Config


class BaseAIProcessor(ABC):
    """Base class for all AI-powered email processing modules"""
    
    def __init__(self):
        self.api_url = "https://g4f.space/v1/chat/completions"
        self.api_key = Config.OPENAI_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
        
    def _make_api_request(self, prompt: str, system_message: str) -> str:
        """Make API request with standardized error handling"""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            data = response.json()
            
            if "error" in data:
                return f"API Error: {data['error']['message']}"
            elif "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"].strip()
            else:
                return "No response from API"
                
        except Exception as e:
            return f"Request Failed: {e}"
    
    @abstractmethod
    def process(self, email_content: str, **kwargs) -> Dict[str, Any]:
        """Abstract method that each processor must implement"""
        pass
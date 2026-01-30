import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment

class Config:
    OPENAI_API_KEY = os.getenv("API_KEY_OPENAI")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_APP_PASSWORD = os.getenv("MAIL_APP_PASSWORD")

    @classmethod
    def validate(cls):
        """Validate that all required configuration is present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("API_KEY_OPENAI is missing from environment")
        if not cls.MAIL_USERNAME:
            raise ValueError("MAIL_USERNAME is missing from environment")
        if not cls.MAIL_APP_PASSWORD:
            raise ValueError("MAIL_APP_PASSWORD is missing from environment")
        print("✅ Configuration validated successfully")

import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment

class Config:
    OPENAI_API_KEY = os.getenv("API_KEY_OPENAI")


    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing")

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")

if not API_KEY:
    raise ValueError("API key not found.")

if not MODEL:
    raise ValueError("Model not found.")

if not BASE_URL:
    raise ValueError("Base URL not found.")
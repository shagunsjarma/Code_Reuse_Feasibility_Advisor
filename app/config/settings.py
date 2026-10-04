from dotenv import load_dotenv
import os 
load_dotenv()  # Load environment variables from .env file

HF_TOKEN = os.getenv("HF_TOKEN", "")
Gemini_API_KEY = os.getenv("GOOGLE_API_KEY", "")
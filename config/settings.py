from dotenv import load_dotenv
import os

load_dotenv()

def get_groq_api():
    return os.getenv("GROQ_API_KEY")
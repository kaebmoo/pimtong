import google.generativeai as genai
from app.core.config import settings
import os

def list_models():
    api_key = settings.GOOGLE_API_KEY
    if not api_key:
        print("No API Key found in settings.")
        return

    print(f"Using API Key: {api_key[:5]}...")
    genai.configure(api_key=api_key)

    try:
        print("Fetching models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()

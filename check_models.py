import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the API Key from your .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: No API Key found. Check your .env file.")
else:
    print(f"✅ Found Key: {api_key[:10]}...")
    genai.configure(api_key=api_key)

    print("\n🔍 Asking Google for available models...")
    try:
        count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" 🌟 AVAILABLE: {m.name}")
                count += 1
        
        if count == 0:
            print("\n❌ Google said you have ZERO models available.")
            print("👉 Fix: Go to https://aistudio.google.com/app/apikey and create a NEW key.")
            
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
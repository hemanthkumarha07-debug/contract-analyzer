import os
import google.generativeai as genai
import docx
from pypdf import PdfReader

# Configure Google AI
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def extract_text(uploaded_file):
    try:
        filename = uploaded_file.name.lower()
        if filename.endswith('.pdf'):
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages[:20]: 
                text += page.extract_text() or ""
            return text
        elif filename.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
        elif filename.endswith('.txt'):
            return uploaded_file.read().decode('utf-8')
        return None
    except Exception as e:
        return f"Error reading file: {str(e)}"

def analyze_contract(text):
    if not text:
        return "Error: File appears empty."
    
    # --- SMART MODEL SELECTOR ---
    # We try the generic alias first. If that fails, we use the standard Pro model.
    try:
        print("🚀 Attempting to use: gemini-flash-latest")
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Test the connection with a tiny prompt first
        model.generate_content("ping") 
    except:
        print("⚠️ Flash failed. Switching to: gemini-pro")
        model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    You are an expert legal AI. Analyze this contract text.
    Format your response in pure HTML (no markdown ```html tags).
    Use specific Tailwind CSS classes for styling:
    - Use <h3 class="text-xl font-bold text-slate-800 mt-4 mb-2"> for headers.
    - Use <ul class="list-disc pl-5 space-y-2 text-slate-600"> for lists.
    - Use <strong class="text-red-600"> for high risks.
    
    1. **Executive Summary**: 1 sentence overview.
    2. **Critical Red Flags**: Top 3 risks.
    3. **Actionable Dates**: Renewal or termination deadlines.

    Contract Text:
    {text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return f"AI Service Error: {str(e)}"
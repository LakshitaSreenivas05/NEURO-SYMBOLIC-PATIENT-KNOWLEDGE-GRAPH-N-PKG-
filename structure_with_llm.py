import sys
# Updated to the modern LangChain Ollama integration
from langchain_ollama import OllamaLLM

try:
    llm = OllamaLLM(
        model="cniongolo/biomistral", 
        temperature=0.0,
        format="json"
    )
    print(" BioMistral initialized successfully.")
except Exception as e:
    print(f"❌ Initialization Failed: {e}")
    sys.exit(1)

def structure_entities(transcript, raw_entities):
    print("\n→ Structuring with BioMistral...")
    
    # Convert entities list to simple text
    entities_text = ", ".join([e['text'] for e in raw_entities])
    
    prompt = f"""
You are an expert clinical data extraction AI system. Your task is to process the following clinical note and detected medical terms, and map them into a strict JSON format.

CRITICAL INSTRUCTIONS:
1. Return ONLY valid, parsable JSON.
2. Do NOT wrap the output in markdown blocks (e.g., no ```json).
3. Do NOT include any conversational text, explanations, greetings, or sign-offs.
4. If a piece of information is missing from the text, use null for strings/numbers, and use an empty array [] for lists. Do not invent or hallucinate information.
5. Use the "Detected Medical Terms" to help guide what belongs in the arrays.

--- CLINICAL NOTE ---
{transcript}

--- DETECTED MEDICAL TERMS ---
{entities_text}

--- REQUIRED JSON SCHEMA ---
{{
    "patient_name": "string or null",
    "gender": "string or null",
    "diseases": ["list of strings"],
    "medications": ["list of strings"],
    "allergies": ["list of strings"],
    "symptoms": ["list of strings"],
    "important_dates": ["list of strings in YYYY-MM-DD format if possible"],
    "warnings": ["list of strings"]
}}
"""

    print("→ Sending prompt to Ollama (waiting for response...)")
    try:
        response = llm.invoke(prompt)
        print("✅ Response received from model!")
        return response
    except Exception as e:
        print(f"\n❌ CRASH DETECTED during llm.invoke():")
        print(f"Error Details: {e}")
        return None

import re
import json
from openai import OpenAI
import pdfplumber

client = OpenAI()  # assumes API key set in environment or config

def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        return "\f".join(page.extract_text() or "" for page in pdf.pages)

def detect_engine_type(filename: str, text: str) -> str:
    name = filename.upper()
    text = text.upper()
    if "CFM" in name or re.search(r"\bCFM56\b", text):
        return "cfm"
    if "LEAP" in name or re.search(r"\bLEAP-?1B\b", text):
        return "leap"
    raise ValueError("Engine type not found")

def call_extraction(text, schema):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=[
            {"role": "system", "content": "You are a PDF data extractor."},
            {"role": "user", "content": text},
        ],
        functions=[schema],
        function_call={"name": schema["name"]},
    )
    return json.loads(response.choices[0].message.function_call.arguments)# Logic for PDF text extraction, engine detection, LLM call

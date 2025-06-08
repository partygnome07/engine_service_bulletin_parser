import re
import fitz  # PyMuPDF
import json
from openai import OpenAI

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    return "\f".join([page.get_text() for page in doc])

def detect_engine_type(filename: str, first_page_text: str) -> str:
    """Detect engine type based on filename or text."""
    fname = filename.upper()
    text = first_page_text.upper()

    if "CFM56" in fname or "CFM56" in text:
        return "cfm"
    if "LEAP" in fname or "LEAP-1B" in text:
        return "leap"
    raise ValueError(f"Unknown engine type in file: {filename}")

def call_extraction(text: str, function_schema: dict, client: OpenAI) -> dict:
    """Call OpenAI function API with schema and return structured output."""
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=[
            {"role": "system", "content": "You are a PDF data extractor."},
            {"role": "user", "content": text}
        ],
        functions=[function_schema],
        function_call={"name": function_schema["name"]}
    )
    raw_args = response.choices[0].message.function_call.arguments
    try:
        return json.loads(raw_args)
    except Exception as e:
        raise ValueError(f"❌ Failed to parse function output: {raw_args}") from e

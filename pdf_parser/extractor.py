import re
import json
import pdfplumber
from openai import OpenAI
from typing import Union
import io

def extract_text_from_pdf(pdf_bytes: Union[str, bytes]) -> str:
    """Extract all text from a PDF file using pdfplumber."""
    if isinstance(pdf_bytes, str):  # fallback in case of legacy use
        with pdfplumber.open(pdf_bytes) as pdf:
            return "\f".join([page.extract_text() or "" for page in pdf.pages])
    else:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            return "\f".join([page.extract_text() or "" for page in pdf.pages])

def detect_engine_type(filename: str, first_page_text: str) -> str:
    fname = filename.upper()
    text = first_page_text.upper()
    if "CFM56" in fname or "CFM56" in text:
        return "cfm"
    if "LEAP" in fname or "LEAP-1B" in text:
        return "leap"
    raise ValueError(f"Unknown engine type in file: {filename}")

def call_extraction(text: str, function_schema: dict, client: OpenAI) -> dict:
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

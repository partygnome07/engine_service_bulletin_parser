import pdfplumber
import re

def extract_text_from_pdf(path: str) -> str:
    """
    Extracts raw text from a PDF using pdfplumber.
    Joins all pages with form feed (\f) markers.
    """
    with pdfplumber.open(path) as pdf:
        return "\f".join([page.extract_text() or "" for page in pdf.pages])

def detect_engine_type(filename: str, first_page_text: str) -> str:
    """
    Detects whether a file is for a CFM or LEAP engine based on filename or content.
    """
    fname = filename.upper()
    text = first_page_text.upper()

    if "CFM56" in fname or re.search(r"\bCFM56\b", text):
        return "cfm"
    if "LEAP" in fname or re.search(r"\bLEAP-?1B\b", text):
        return "leap"
    raise ValueError(f"Cannot detect engine type from: {filename}")

def call_extraction(text: str, function_schema: dict, client=None) -> dict:
    """
    Calls the OpenAI API using the provided schema and text.
    You must pass in a valid OpenAI `client`.
    """
    if client is None:
        raise ValueError("Missing required OpenAI client")

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
    return response.choices[0].message.function_call.arguments
r PDF text extraction, engine detection, LLM call

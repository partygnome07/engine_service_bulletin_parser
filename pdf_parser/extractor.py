import pdfplumber
from typing import Union
import io

def extract_text_from_pdf(pdf_bytes: Union[str, bytes]) -> str:
    """Extract text from a PDF file."""
    if isinstance(pdf_bytes, str):  # fallback if using a file path
        with pdfplumber.open(pdf_bytes) as pdf:
            return "\f".join([page.extract_text() or "" for page in pdf.pages])
    else:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            return "\f".join([page.extract_text() or "" for page in pdf.pages])

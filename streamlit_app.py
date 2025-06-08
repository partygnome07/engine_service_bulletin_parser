import streamlit as st
from openai import OpenAI
from pdf_parser.extractor import extract_text_from_pdf

client = OpenAI()

st.set_page_config(page_title="PDF Tester", layout="centered")
st.title("📄 Minimal PDF Text Extractor")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    try:
        file_bytes = uploaded_file.read()
        text = extract_text_from_pdf(file_bytes)

        st.success("✅ Successfully extracted text")
        st.text_area("Extracted Text", text[:3000], height=300)  # show partial preview
    except Exception as e:
        st.error(f"❌ Error extracting text: {e}")

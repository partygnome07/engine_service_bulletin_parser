
import streamlit as st
import os
import io
import pandas as pd
from pdf_parser.extractor import extract_text_from_pdf, detect_engine_type, call_extraction
from pdf_parser.schemas import leap_schema, cfm_schema
from pdf_parser.formatter import build_excel_output

st.set_page_config(page_title="🛠️ Aircraft SB Parser", layout="centered")

st.markdown("## 🛩️ Aircraft Service Bulletin Parser")
st.markdown("Upload engine PDF bulletins (CFM or LEAP) below to extract data and manage outputs.")
st.markdown("---")

uploaded_files = st.file_uploader("📄 Upload PDF Documents", type="pdf", accept_multiple_files=True)

# Paths for master Excel files
master_dir = Path("master_excels")
master_dir.mkdir(exist_ok=True)
cfm_master_path = master_dir / "cfm_master.xlsx"
leap_master_path = master_dir / "leap_master.xlsx"

def append_to_master(excel_df: pd.DataFrame, engine_type: str):
    path = cfm_master_path if engine_type == "cfm" else leap_master_path
    if path.exists():
        existing_df = pd.read_excel(path)
        combined = pd.concat([existing_df, excel_df], ignore_index=True)
    else:
        combined = excel_df
    combined.to_excel(path, index=False)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        with open(file_name, "wb") as f:
            f.write(uploaded_file.read())

        st.markdown(f"### 🧠 Processing: `{file_name}`")

        # Step 1: Extract and detect engine
        text = extract_text_from_pdf(file_name)
        engine_type = detect_engine_type(file_name, text.split("\f", 1)[0])
        schema = leap_schema if engine_type == "leap" else cfm_schema

# Streamlit UI to upload PDFs, select mode, trigger parsing

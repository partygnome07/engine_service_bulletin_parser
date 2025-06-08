from pathlib import Path
import streamlit as st
import os
import io
import tempfile
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
    return path

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            file_name = uploaded_file.name
            st.markdown(f"### 🧠 Processing: `{file_name}`")

            # Save uploaded PDF to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            # Step 1: Extract text & detect engine
            text = extract_text_from_pdf(tmp_path)
            first_page = text.split("\f", 1)[0]
            engine_type = detect_engine_type(file_name, first_page)
            schema = leap_schema if engine_type == "leap" else cfm_schema

            # Step 2: Parse the document
            parsed = call_extraction(text, schema)

            # Step 3: Build Excel
            excel_bytes, excel_df = build_excel_output(parsed, engine_type)
            output_excel_name = f"{Path(file_name).stem}_{engine_type.upper()}_parsed.xlsx"

            # Step 4: Display success
            st.success(f"✅ Successfully processed: `{file_name}`")
            st.download_button(
                label="📥 Download Parsed Excel",
                data=excel_bytes,
                file_name=output_excel_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Step 5: Add option to upload to master
            choice = st.radio(
                f"What would you like to do with `{file_name}`?",
                ["Nothing", "Add to Master Only", "Add to Master & Download"],
                key=file_name
            )

            if choice in {"Add to Master Only", "Add to Master & Download"}:
                master_path = append_to_master(excel_df, engine_type)
                st.success(f"✅ Added to {engine_type.upper()} master Excel")
                if choice == "Add to Master & Download":
                    with open(master_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Updated Master Excel",
                            data=f.read(),
                            file_name=master_path.name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

        except Exception as e:
            st.error(f"❌ Error processing `{uploaded_file.name}`: {e}")

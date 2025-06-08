for uploaded_file in uploaded_files:
    file_name = uploaded_file.name
    file_bytes = uploaded_file.read()  # read PDF in memory
    st.markdown(f"### 🧠 Processing: `{file_name}`")

    try:
        # Step 1: Extract and detect engine
        text = extract_text_from_pdf(file_bytes)
        engine_type = detect_engine_type(file_name, text.split("\f", 1)[0])
        schema = leap_schema if engine_type == "leap" else cfm_schema

        # Step 2: Run extraction
        result = call_extraction(text, schema, client)
        meta_df, parts_df, removed_df, cfg_df = build_excel_output(result, engine_type)

        # Step 3: User options
        option = st.radio(
            f"What would you like to do with `{file_name}`?",
            ("Only download parsed Excel", "Only add to master Excel", "Add to master + download"),
            key=file_name
        )

        # Step 4: Handle actions
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            meta_df.to_excel(writer, sheet_name="Metadata", index=False)
            if engine_type == "leap":
                parts_df.to_excel(writer, sheet_name="ListOfSpares", index=False)
                removed_df.to_excel(writer, sheet_name="RemovedSpares", index=False)
            else:
                parts_df.to_excel(writer, sheet_name="PartsList", index=False)
                cfg_df.to_excel(writer, sheet_name="ConfigChanges", index=False)
        output.seek(0)

        if option in ("Only add to master Excel", "Add to master + download"):
            append_to_master(parts_df, engine_type)

        if option in ("Only download parsed Excel", "Add to master + download"):
            st.download_button(
                label="⬇️ Download Excel File",
                data=output,
                file_name=f"{file_name.replace('.pdf','')}_{engine_type.upper()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Error processing {file_name}: {e}")

import os
import re
import streamlit as st
import pandas as pd
from difflib import get_close_matches
from utilities.pdf_utils import (
    extract_text_google_vision,
    clean_text,
    translate_if_needed
)

# ✅ Google Vision credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "data/pratyangira.json"

# ✅ Load drug list
drug_df = pd.read_csv("data/drug_list_200.csv")
if "Drug Name" not in drug_df.columns:
    st.error("❌ 'Drug Name' column not found in drug list CSV.")
    st.stop()

known_drugs = drug_df['Drug Name'].str.strip().str.lower().tolist()

# ✅ Streamlit UI
st.title("🧠 AI Assistant for Chemist Shops")
st.write("Upload a prescription image to extract structured drug information.")

uploaded_file = st.file_uploader("📤 Upload Prescription Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="📸 Uploaded Prescription", use_column_width=True)

    extracted_text = extract_text_google_vision(uploaded_file)

    if not extracted_text:
        st.error("❌ Could not extract text from the image.")
    else:
        st.subheader("🔍 Extracted Text")
        st.text(extracted_text)

        final_text = translate_if_needed(extracted_text)
        cleaned = clean_text(final_text)

        # 🔧 Fix common OCR errors
        cleaned = cleaned.replace(",", ".")
        cleaned = re.sub(r"(\d)\s+(\d)", r"\1.\2", cleaned)
        cleaned = re.sub(r"(\d+)\s*(mg|g|mcg)", r"\1\2", cleaned, flags=re.IGNORECASE)

        ocr_corrections = {
            "joong": "500mg",
            "sween": "seven",
            "loon": "500mg",
            "soong": "500mg",
            "loong": "500mg"
        }
        for wrong, correct in ocr_corrections.items():
            cleaned = re.sub(rf'\b{wrong}\b', correct, cleaned, flags=re.IGNORECASE)

        st.subheader("🧽 Cleaned Text")
        st.text(cleaned)

        # ✅ Extract full instruction section using regex (more robust)
        instruction_match = re.search(
            r'(sigj?|sign)\s*[:\-]?\s*(.*?)\s*(physician|lic no|ptr no|$)',
            cleaned,
            re.IGNORECASE | re.DOTALL
        )

        if instruction_match:
            full_instruction = instruction_match.group(2).strip()
        else:
            full_instruction = "--"

        tokens = cleaned.strip().split()
        drugs = []
        dosages = []
        instructions = []

        # ✅ Extract drugs
        for i in range(len(tokens)):
            token = tokens[i].lower()
            if re.match(r"\d+(\.\d+)?(mg|g|mcg)", token):
                dosage = token

                possible_names = [
                    " ".join(tokens[i - j:i]) for j in range(3, 0, -1) if i - j >= 0
                ]
                match = None
                for name in possible_names:
                    matches = get_close_matches(name.lower(), known_drugs, n=1, cutoff=0.8)
                    if matches:
                        match = matches[0]
                        break

                if match:
                    drugs.append(match.title())
                    dosages.append(dosage)
                    instructions.append(full_instruction if full_instruction else "--")

        if drugs:
            results_df = pd.DataFrame({
                "Drug Name": drugs,
                "Dosage": dosages,
                "Instructions": instructions
            })

            st.subheader("💊 Structured Drug Information")
            st.dataframe(results_df)
        else:
            st.warning("⚠️ No valid drugs matched from the known list.")
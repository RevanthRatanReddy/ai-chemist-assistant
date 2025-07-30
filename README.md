# 🧠 AI Assistant for Chemist Shops

Automatically extracts drug names from handwritten prescriptions and checks against a known drug list using OCR and NLP techniques.Converts handwritten prescriptions to structured format that helps pharmacists find drugs faster.

---

## 📸 Overview

Doctors often write prescriptions by hand, making them hard to read for chemists.  
This AI Assistant extracts drug names directly from prescription images using OCR, cleans the text, optionally translates non-English text, and matches it against a verified drug database.

---

## 🛠️ Tech Stack

- 🐍 Python – Core backend logic  
- 📊 Pandas – Structured drug data handling  
- 🎯 Streamlit – Web-based user interface  
- ☁️ Google Cloud Vision API – Primary OCR engine  
- 👁️ EasyOCR & 🧾 Tesseract – Secondary OCR fallback  
- 🌐 Google Translate – Translates non-English prescriptions  
- 🧠 Regex & Exact Matching – For drug name cleaning and lookup  
- 📁 CSV – For loading drug list (`drug_list_200.csv`)

---

## 🧠 How It Works

1. 📤 Upload a handwritten prescription image.  
2. 🔍 Text is extracted using OCR (Google Vision, EasyOCR, or Tesseract).  
3. 🧽 The text is cleaned using NLP (regex, line break fixes, etc.)  
4. 🌐 If text is not in English, it is auto-translated.  
5. 💊 Each word is compared to a known drug list for exact match.  
6. 📋 Results are shown as a **structured table** in Streamlit.

---

## 📂 Project Structure
📁 ai-bot/
├── data/
│ ├── drug_list_200.csv
│ └── pratyangira.json ← (Google Vision API key - not pushed)
├── utils/
│ └── pdf_utils.py ← OCR and NLP logic
├── main.py ← Streamlit UI + full workflow
├── requirements.txt ← Python dependencies
└── README.md ← You're reading this file

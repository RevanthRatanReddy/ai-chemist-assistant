# utilities/pdf_utils.py

import io
import os
import pandas as pd
import re
from google.cloud import vision
from langdetect import detect
from googletrans import Translator

# ✅ Set credentials for Vision API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "data/shodashi.json"

def extract_text_google_vision(image_file):
    client = vision.ImageAnnotatorClient()
    content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    else:
        return ""

def translate_if_needed(text):
    lang = detect(text)
    if lang != 'en':
        translator = Translator()
        translation = translator.translate(text, src=lang, dest='en')
        return translation.text
    return text

def clean_text(text):
    cleaned = re.sub(r'[^\w\s]', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
    return cleaned

def extract_drugs(text, known_drugs):
    found = []
    for drug in known_drugs:
        if drug in text:
            found.append(drug)
    return found

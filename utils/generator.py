# utils/generator.py

import os
import openai
from prompts import VITALS_EXTRACTION_PROMPT, SECTION_PROMPTS

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_vitals(text):
    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured RFP data."},
            {"role": "user", "content": VITALS_EXTRACTION_PROMPT.format(text=text)}
        ],
        temperature=0
    )
    return response["choices"][0]["message"]["content"]

def generate_section(section_name, text):
    prompt = SECTION_PROMPTS.get(section_name)
    if not prompt:
        return f"No prompt defined for section '{section_name}'"
    
    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a professional RFP response generator."},
            {"role": "user", "content": prompt.format(text=text)}
        ],
        temperature=0.5
    )
    return response["choices"][0]["message"]["content"]

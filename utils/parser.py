# utils/parser.py

import fitz  # PyMuPDF
import docx2txt

def parse_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def parse_docx(file):
    return docx2txt.process(file)

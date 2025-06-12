# utils/parser.py

import fitz  # PyMuPDF
import docx2txt
import json

def parse_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def parse_docx(file):
    return docx2txt.process(file)

def sanitize_dict_for_table(d):
    """Convert any list/dict values in a dict to pretty-printed strings for DataFrame display."""
    result = {}
    for k, v in d.items():
        if isinstance(v, (dict, list)):
            try:
                result[k] = json.dumps(v, indent=2, ensure_ascii=False)
            except Exception:
                result[k] = str(v)
        else:
            result[k] = v
    return result
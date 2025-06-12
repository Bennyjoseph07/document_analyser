# utils/parser.py

import fitz  # PyMuPDF
import docx2txt
import json
import pandas as pd

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

def flatten_for_csv(data):
        rows = []
        if isinstance(data, dict):
            for section, content in data.items():
                if isinstance(content, dict):
                    for k, v in content.items():
                        rows.append({"Section": section, "Key": k, "Value": str(v)})
                elif isinstance(content, list):
                    for idx, item in enumerate(content, 1):
                        if isinstance(item, dict):
                            for k, v in item.items():
                                rows.append({"Section": section, "Key": f"{k} [{idx}]", "Value": str(v)})
                        else:
                            rows.append({"Section": section, "Key": f"Item [{idx}]", "Value": str(item)})
                else:
                    rows.append({"Section": section, "Key": "", "Value": str(content)})
        return pd.DataFrame(rows)
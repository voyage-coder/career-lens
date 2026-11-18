from io import BytesIO
from docx import Document
from pypdf import PdfReader
def extract_resume_text(filename,content):
    if filename.lower().endswith(".pdf"):
        text="\n".join(p.extract_text() or "" for p in PdfReader(BytesIO(content)).pages)
    elif filename.lower().endswith(".docx"):
        text="\n".join(p.text for p in Document(BytesIO(content)).paragraphs)
    else: raise ValueError("Only PDF and DOCX files are supported")
    text="\n".join(x.strip() for x in text.splitlines() if x.strip())
    if len(text)<30: raise ValueError("Not enough text extracted; scanned PDFs need OCR support")
    return text

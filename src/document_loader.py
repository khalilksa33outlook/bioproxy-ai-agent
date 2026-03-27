import os
from pypdf import PdfReader
from docx import Document

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif ext == ".docx":
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    return text

def ingest_docs(memory):
    doc_path = "./data/company_docs/"
    for file in os.listdir(doc_path):
        if file.endswith((".pdf", ".docx")):
            full_path = os.path.join(doc_path, file)
            content = extract_text(full_path)
            # Store in the same Vector DB we used for sectors
            memory.save_entity("DOCUMENT", file, content[:1000], {"source": file})
            print(f"📖 Indexed Document: {file}")

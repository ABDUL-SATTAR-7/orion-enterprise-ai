import pdfplumber
from docx import Document


def extract_pdf_text(filepath: str):
    text = ""

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_docx_text(filepath: str):
    document = Document(filepath)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_txt_text(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def extract_text(filepath: str):
    if filepath.endswith(".pdf"):
        return extract_pdf_text(filepath)

    if filepath.endswith(".docx"):
        return extract_docx_text(filepath)

    if filepath.endswith(".txt"):
        return extract_txt_text(filepath)

    return ""
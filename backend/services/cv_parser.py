import io

import pymupdf
from docx import Document


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from a PDF file.
    """

    pdf_document = pymupdf.open(
        stream=file_content,
        filetype="pdf",
    )

    pages_text = []

    for page in pdf_document:
        text = page.get_text()

        if text:
            pages_text.append(text)

    pdf_document.close()

    return "\n".join(pages_text).strip()


def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extract text from a DOCX file.
    """

    document = Document(
        io.BytesIO(file_content)
    )

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs).strip()


def extract_cv_text(
    filename: str,
    file_content: bytes,
) -> str:
    """
    Extract text from a PDF or DOCX CV.
    """

    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_content)

    if filename.endswith(".docx"):
        return extract_text_from_docx(file_content)

    raise ValueError(
        "Only PDF and DOCX files are supported."
    )

from io import BytesIO

import pytest
from docx import Document
from reportlab.pdfgen import canvas

from app.services.resume_parser import extract_resume_text


def create_pdf(text):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(50, 750, text)
    pdf.save()
    return buffer.getvalue()


def create_docx(text):
    document = Document()
    document.add_paragraph(text)

    buffer = BytesIO()
    document.save(buffer)

    return buffer.getvalue()


def test_extract_valid_pdf():
    content = create_pdf(
        "This is a valid resume containing sufficient text for extraction."
    )

    result = extract_resume_text("resume.pdf", content)

    assert "valid resume" in result


def test_extract_valid_docx():
    content = create_docx(
        "This is a valid DOCX resume containing sufficient text for extraction."
    )

    result = extract_resume_text("resume.docx", content)

    assert "valid DOCX resume" in result


def test_unsupported_file_extension():
    with pytest.raises(ValueError, match="Only PDF and DOCX"):
        extract_resume_text("resume.txt", b"Some text")


def test_insufficient_text():
    content = create_docx("Short text")

    with pytest.raises(ValueError, match="Not enough text"):
        extract_resume_text("resume.docx", content)


def test_empty_document():
    content = create_docx("")

    with pytest.raises(ValueError, match="Not enough text"):
        extract_resume_text("resume.docx", content)


def test_whitespace_cleaning():
    content = create_docx(
        "This is a sufficiently long resume text.   "
    )

    result = extract_resume_text("resume.docx", content)

    assert result == result.strip()
    assert len(result) >= 30

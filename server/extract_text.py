from pdfminer.high_level import extract_text
import docx2txt


def extract_text_from_docx(docx_path):
    txt = docx2txt.process(docx_path)
    if txt:
        return txt.replace("\t", " ")
    return None


def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

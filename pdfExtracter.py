import os
import PyPDF2
from tagExtracter import tagExtracter

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

file = r""
resume_text = extract_text_from_pdf(file)
extracter = tagExtracter(api_key = os.getenv("GEMINI_API_KEY"), model = "gemini-2.5-flash")
tags = extracter.extract(resume_text)
print(tags)
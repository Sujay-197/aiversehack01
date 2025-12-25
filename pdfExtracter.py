import os
import PyPDF2
from tagExtracter import tagExtracter
class extractPDF:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.extracter = tagExtracter(api_key = os.getenv("GEMINI_API_KEY"), model = "gemini-2.5-flash")
    
    def extract_text(self):
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text

    def extract_tags(self):
        resume_text = self.extract_text()
        tags = self.extracter.extract(resume_text)
        return tags

if __name__ == "__main__":
    pdf_path = ""
    pdf = extractPDF(pdf_path)
    tags = pdf.extract_tags()
    print(tags)
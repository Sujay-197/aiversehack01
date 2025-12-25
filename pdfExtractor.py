import os
import PyPDF2
from tagExtractor import tagExtractor
class extractPDF:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.extractor = tagExtractor(api_key = os.getenv("GEMINI_API_KEY"), model = "gemini-2.5-flash")
    
    def extract_text(self):
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text

    def extract_tags(self):
        resume_text = self.extract_text()
        tags = self.extractor.extract(resume_text)
        return tags

if __name__ == "__main__":
    pdf_path = r""
    pdf = extractPDF(pdf_path)
    tags = pdf.extract_tags()
    print(tags)
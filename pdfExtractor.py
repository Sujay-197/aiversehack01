import os
import PyPDF2
from tagExtractor import tagExtractor

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.extractor = tagExtractor(api_key=os.getenv("GEMINI_API_KEY"), model="gemini-2.5-flash")
    
    def extract_text(self):
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or "" # Handle pages that might return None
            return text
        except FileNotFoundError:
            print(f"Error: File not found at {self.pdf_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def extract_tags(self):
        resume_text = self.extract_text()
        if resume_text:
            tags = self.extractor.extract(resume_text)
            return tags
        return None

if __name__ == "__main__":
    pdf_path = r"C:\Users\Vishal\Downloads\DOC-20251213-WA0001..pdf"
    if os.path.exists(pdf_path):
        pdf = PDFExtractor(pdf_path)
        tags = pdf.extract_tags()
        print(tags)
    else:
        print(f"File not found: {pdf_path}")
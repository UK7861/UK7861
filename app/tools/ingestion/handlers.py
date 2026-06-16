import pandas as pd
from fpdf import FPDF
from docx import Document
import docx2txt
from pypdf import PdfReader
from bs4 import BeautifulSoup
import requests
import os
import json

class FileIngestor:
    @staticmethod
    def read_file(filepath: str):
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".csv":
            return pd.read_csv(filepath).to_dict(orient="records")
        elif ext in [".xls", ".xlsx"]:
            return pd.read_excel(filepath).to_dict(orient="records")
        elif ext == ".json":
            with open(filepath, 'r') as f:
                return json.load(f)
        elif ext == ".pdf":
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        elif ext == ".docx":
            return docx2txt.process(filepath)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

class WebIngestor:
    @staticmethod
    def scrape_url(url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text()

class ReportGenerator:
    @staticmethod
    def create_pdf(content: str, filename: str):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=content)
        pdf.output(filename)

ingestor = FileIngestor()
reporter = ReportGenerator()

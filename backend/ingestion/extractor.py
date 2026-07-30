import os
from pypdf import PdfReader

def extract_txt(file_path:str):
    with open(file_path,"r",encoding="utf-8") as file:
        return file.read()
    
def extract_pdf(file_path:str):
    reader= PdfReader(file_path)

    text=""

    for page in reader.pages:
        page_text = page.extract_text()
    
        if page_text:
            text += page_text + "\n"
    
    return text

def extract_text(file_path:str):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".txt":
        return extract_txt(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )
import os
from pypdf import PdfReader

def extract_txt(file_path:str):
    """Returns a list of (page_number, text) tuples - page is None for formats without pages."""
    with open(file_path,"r",encoding="utf-8") as file:
        return [(None,file.read())]
    
def extract_pdf(file_path:str):
    """Returns one (page_number, text) tuple per PDF page, instead of merging all pages into one string."""
    reader= PdfReader(file_path)

    pages=[]

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        if page_text:
            pages.append((page_number, page_text))

    return pages


def extract_text(file_path:str):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".txt":
        return extract_txt(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )
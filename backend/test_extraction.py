from ingestion.extractor import extract_text

text = extract_text(
    "uploads/python.pdf"
)

print(text)
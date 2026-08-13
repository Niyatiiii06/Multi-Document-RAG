import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)


DOCUMENTS_PATH = "docs"

all_documents = []

pdf_files = [
    file
    for file in os.listdir(DOCUMENTS_PATH)
    if file.lower().endswith(".pdf")
]

print(f"PDF files found: {len(pdf_files)}")

for file in pdf_files:
    file_path = os.path.join(DOCUMENTS_PATH, file)
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    for doc in documents:
        doc.metadata["source_type"] = "pdf"
        doc.metadata["book"] = file

    all_documents.extend(documents)


text_path = os.path.join(
    DOCUMENTS_PATH,
    "notes.txt"
)

loader = TextLoader(
    text_path,
    encoding="utf-8"
)

text_documents = loader.load()

for doc in text_documents:
    doc.metadata["source_type"] = "text"
    doc.metadata["book"] = "notes.txt"
all_documents.extend(text_documents)

print("\n-----------------------------")
print("TOTAL DOCUMENT OBJECTS:", len(all_documents))
print("-----------------------------")

for i, doc in enumerate(all_documents[:5], start=1):
    print(f"\n--- DOCUMENT {i} ---")
    print("Source type:", doc.metadata.get("source_type"))
    print("Source:", doc.metadata.get("book"))
    print("Content:", doc.page_content[:200])


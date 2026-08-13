import os
from langchain_community.document_loaders import PyPDFLoader

Doc_path= 'docs'
all_docs=[]

pdf_files=[file
    for file in os.listdir(Doc_path)
    if file.lower().endswith('pdf')
]
print(f'PDF FILES FOUND: {len(pdf_files)}')

for file in pdf_files:
    file_path= os.path.join(Doc_path, file)

    print(f'\nLoading: {file}')
    loader= PyPDFLoader(file_path)
    documents= loader.load()
    all_docs.extend(documents)

    print(f"Pages loaded: {len(documents)}")

print("\n-----------------------------")
print("TOTAL PDFs:", len(pdf_files))
print("TOTAL PAGES:", len(all_docs))
print("-----------------------------")
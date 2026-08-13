import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
    for doc in documents:
        doc.metadata['book']= file
    all_docs.extend(documents)

    print(f"Pages loaded: {len(documents)}")

print("\n-----------------------------")
print("TOTAL PDFs:", len(pdf_files))
print("TOTAL PAGES:", len(all_docs))
print("-----------------------------")

splitter= RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap= 200
)
chunks= splitter.split_documents(all_docs)
print("Total pages:", len(all_docs))
print("Total chunks:", len(chunks))
print(chunks[0].page_content[:500])
print(chunks[0].metadata)
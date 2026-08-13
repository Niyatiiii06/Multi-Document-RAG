import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_mistralai import MistralAIEmbeddings
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
load_dotenv()

Doc_path= 'docs'
all_docs=[]

pdf_files=[file
    for file in os.listdir(Doc_path)
    if file.lower().endswith('.pdf')
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

embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0
)

while True:
    query= input('\nAsk a question (or type exit): ')
    if query.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    retrieved_docs= vectorstore.similarity_search(
        query,k=3)

    context=[]
    for doc in retrieved_docs :
        source= doc.metadata.get('book','Unknown')
        page = doc.metadata.get("page_label", "Unknown")
        context.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{doc.page_content}"
        )
    context = "\n\n---\n\n".join(context)
    messages = [
        SystemMessage(
            content=(
                "You are a helpful PDF question-answering assistant. "
                "Answer the user's question using only the provided context. "
                "If the answer cannot be found in the context, say "
                "'I couldn't find that in the provided documents.' "
                "Do not invent information."
            )
        ),
        HumanMessage(
            content=(
                f"Context:\n\n{context}\n\n"
                f"Question: {query}")
        )
    ]

    response = llm.invoke(messages)
    print("\nAssistant:")
    print(response.content)

    print("\nSources:")

    for doc in retrieved_docs:
        source = doc.metadata.get("book", "Unknown")
        page = doc.metadata.get("page_label", "Unknown")
        print(f"- {source}, page {page}")
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document as LCDocument
import os

# Set up embedding model and Chroma store
embedding_model = OllamaEmbeddings(model="mxbai-embed-large")
chroma_path = "./chroma_db"

vectorstore = Chroma(
    collection_name="documents",
    embedding_function=embedding_model,
    persist_directory=chroma_path
)

def add_document_to_vectorstore(doc_id: int, title: str, content: str):
    lc_doc = LCDocument(page_content=content, metadata={"doc_id": doc_id, "title": title})
    vectorstore.add_documents([lc_doc])
    vectorstore.persist()

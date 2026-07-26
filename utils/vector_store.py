import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from utils.pii_masker import mask_text

# Initialize embeddings and database configuration
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
CHROMA_PERSIST_DIR = "./chroma_db"

def process_and_store_document(file_path: str, customer_id: str) -> bool:
    """Load PDF, split into chunks, mask PII, and store in ChromaDB with tenant metadata."""
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        
        for chunk in chunks:
            chunk.page_content = mask_text(chunk.page_content)
            chunk.metadata["customer_id"] = customer_id
            
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )
        return True
    except Exception as e:
        print(f"Error processing and storing document: {e}")
        return False

def clear_customer_documents(customer_id: str) -> bool:
    """Clear all stored documents for a specific customer from ChromaDB."""
    try:
        vectorstore = Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=embeddings
        )
        existing = vectorstore.get(where={"customer_id": customer_id})
        if existing and existing["ids"]:
            vectorstore.delete(ids=existing["ids"])
        return True
    except Exception as e:
        print(f"Error clearing customer documents: {e}")
        return False


# app/rag_engine.py

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_DIR = "db"

def embed_documents(documents):
    embeddings = OpenAIEmbeddings()
    print(f"Embedding {len(documents)} documents...")

    vector_store = Chroma.from_documents(
        documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    vector_store.persist()
    return vector_store

def load_vector_store():
    embeddings = OpenAIEmbeddings()
    if os.path.exists(CHROMA_DIR):
        return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    return None

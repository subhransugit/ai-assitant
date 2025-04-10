import os.path

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_pdf(pdf_path:str):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"FIle Not FOund: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    documents= loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)

    chunks = splitter.split_documents(documents)
    return chunks

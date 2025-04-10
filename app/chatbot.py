# app/chatbot.py

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from rag_engine import load_vector_store
from memory_store import get_memory

def get_chatbot():
    llm = ChatOpenAI(temperature=0)

    vector_store = load_vector_store()
    if not vector_store:
        raise ValueError("Vector store not initialized. Upload a document to create embeddings first.")
    retriever = vector_store.as_retriever()

    memory = get_memory()

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        output_key="answer"
    )
    return qa_chain

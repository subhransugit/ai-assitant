# app/main.py

import streamlit as st
from chatbot import get_chatbot
from document_handler import load_and_split_pdf
from rag_engine import embed_documents
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
import os

st.set_page_config(page_title="LangChain AI Assistant", layout="wide")
st.title("🧠 LangChain Assistant with File Upload")



# Upload section
st.sidebar.header("📁 Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

# Session state init
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file:
    # Save the uploaded file temporarily
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load and chunk the document
    chunks = load_and_split_pdf(file_path)
    st.sidebar.success(f"Loaded and split into {len(chunks)} chunks.")

    # Embed & build vector store
    embed_documents(chunks)
    st.sidebar.success("✅ Embeddings created!")

    # Build chatbot
    st.session_state.chatbot = get_chatbot()
    st.sidebar.success("🤖 Chatbot is ready!")

    #Optional: Summarize
    if st.sidebar.button("Summarize Document"):
        st.subheader("📄 Document Summary")
        llm = ChatOpenAI(temperature=0)
        summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = summary_chain.run(chunks)
        st.info(summary)

# Step 2: Chat UI
st.header("💬 Ask Questions About the Document")
if st.session_state.chatbot:
    user_input = st.text_input("Your question:")
    if user_input:
        output = st.session_state.chatbot.invoke({"question": user_input})
        response = output["answer"]
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {msg}")
else:
    st.info("⬅️ Upload a document first to start chatting.")

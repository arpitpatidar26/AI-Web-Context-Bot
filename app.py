import streamlit as st
import os

# --- CONFIGURATION ---
os.environ["USER_AGENT"] = "my-chatbot/1.0"
# -------------------

from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.embeddings import HuggingFaceEmbeddings

from backend import (
    load_and_process_url,
    create_vector_store,
    get_rag_chain,
    DB_FAISS_PATH
)

# Page config
st.set_page_config(page_title="Humanli.ai Chatbot", layout="wide")
st.title("Humanli.ai: Website-Based Chatbot")

# Sidebar: API key and URL
with st.sidebar:
    st.header("Settings")
    url_input = st.text_input("Enter Website URL")

    # Groq API Key
    api_key = st.text_input("Groq API Key", type="password")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key

    if st.button("Index Website"):
        if not url_input or not api_key:
            st.error("Please provide both a URL and a Groq API Key.")
        else:
            with st.spinner("Crawling and Indexing..."):
                splits = load_and_process_url(url_input)
                if isinstance(splits, str):
                    st.error(splits)
                else:
                    create_vector_store(splits)
                    st.success("Indexing Complete! You can now ask questions.")
                    st.session_state.chat_history = []

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load vectorstore helper
def load_vectorstore():
    if os.path.exists(DB_FAISS_PATH):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(
            DB_FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore
    return None

# Chat interface
user_query = st.chat_input("Ask a question about the website...")

if user_query:
    vectorstore = load_vectorstore()
    if not vectorstore:
        st.warning("Please index a website first.")
    else:
        with st.chat_message("Human"):
            st.write(user_query)

        with st.chat_message("AI"):
            rag_chain = get_rag_chain(vectorstore)
            response = rag_chain.invoke({
                "input": user_query,
                "chat_history": st.session_state.chat_history
            })
            answer = response["answer"]
            st.write(answer)

            # Update chat history
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=answer))
import streamlit as st
import os

# --- CONFIGURATION ---
os.environ["USER_AGENT"] = "my-chatbot/1.0"

# 1. PERMANENT API KEY LOGIC
# This checks Streamlit Secrets first so you don't have to enter the key every time.
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
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
st.set_page_config(page_title="AI-Web-Context-Bot", layout="wide")
st.title("AI-Web-Context-Bot")

# Sidebar: API key and URL
with st.sidebar:
    st.header("Settings")
    url_input = st.text_input("Enter Website URL")

    # 2. API KEY FALLBACK
    # If the secret isn't set, show the input field. If it IS set, this stays hidden.
    if "GROQ_API_KEY" not in os.environ:
        api_key = st.text_input("Groq API Key", type="password")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key

    if st.button("Index Website"):
        if not url_input:
            st.error("Please provide a URL.")
        elif "GROQ_API_KEY" not in os.environ:
            st.error("Groq API Key is missing. Please add it to Secrets or the sidebar.")
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
@st.cache_resource
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

# --- 3. CHAT HISTORY DISPLAY LOGIC ---
# This loop ensures that previous questions/answers stay on the screen
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)

# Chat interface
user_query = st.chat_input("Ask a question about the website...")

if user_query:
    vectorstore = load_vectorstore()
    if not vectorstore:
        st.warning("Please index a website first.")
    else:
        # Display current user message
        with st.chat_message("Human"):
            st.markdown(user_query)

        # Generate and display AI response
        with st.chat_message("AI"):
            rag_chain = get_rag_chain(vectorstore)
            response = rag_chain.invoke({
                "input": user_query,
                "chat_history": st.session_state.chat_history
            })
            answer = response["answer"]
            st.markdown(answer)

        # Update session state history
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=answer))

# AI-Web-Context-Bot: Website-Based RAG Assistant

## 🚀 Project Overview

AI-Web-Context-Bot is a Retrieval-Augmented Generation (RAG) application that turns any website into a conversational knowledge base. Users provide a URL, and the bot crawls, extracts, and indexes the content to answer queries with high factual accuracy.

## 🔗 Live Demo
You can access the live application here:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-web-context-bot.streamlit.app)

## 🏗️ Architecture Explanation

The system follows a standard RAG pipeline:

1.Ingestion: WebBaseLoader extracts raw HTML content from the provided URL.

2.Chunking: RecursiveCharacterTextSplitter breaks text into 1000-character segments with a 200-character overlap to maintain semantic continuity.

3.Indexing: Text segments are converted into embeddings and stored in a local FAISS index.

4.Retrieval: The system performs a similarity search to find the top $k$ relevant chunks for a user query.

5.Generation: A rephrasing chain ensures the query is standalone, and a QA chain generates the final answer using the retrieved context.
## 🛠️ Frameworks & Tools

- Framework: LangChain was used for its robust ecosystem in managing document loaders, prompt templates, and chain orchestration.
-  Streamlit: Provides the interactive web-based user interface for URL input and real-time chat.

- LLM Model: Llama-3.3-70b-versatile (via Groq). It offers state-of-the-art reasoning capabilities with exceptionally low latency via Groq's LPUs, making the chatbot feel responsive in real-time.

- Vector Database: FAISS (Facebook AI Similarity Search). It is an efficient, open-source library for dense vector similarity search that runs locally on CPU, removing the need for external cloud database overhead.

- Embedding Strategy: sentence-transformers/all-MiniLM-L6-v2. This model provides a great balance between performance and speed for English text, running locally to ensure data privacy and zero API costs for embeddings.
## 💻 Setup and Run Instructions

- Prerequisites

  - Python 3.9+
  - A Groq API Key (obtainable from Groq Cloud)

- Clone the project

```bash
  git clone https://github.com/arpitpatidar26/AI-Web-Context-Bot.git
  cd AI-Web-Context-Bot
```

- Create a Virtual Environment

```bash
  For Windows
  python -m venv venv .\venv\Scripts\activate

  For Mac/Linux
  python3 -m venv venv source venv/bin/activate
```

- Install dependencies

```bash
  pip install -r requirements.txt
```

- Run the Application

```bash
  streamlit run app.py
```


## 📝 Assumptions, Limitations & Future Improvements

- Assumptions: The target website does not block scraping via robots.txt or heavy JavaScript rendering (SPA).

- Limitations:

  - The bot currently processes a single URL rather than crawling an entire domain.

  - FAISS index is stored locally and is session-dependent in the current Streamlit configuration.

- Future Improvements:

  - Implement LangGraph to create a multi-step research agent that can browse multiple links.

  - Add support for multi-modal RAG (processing images on the website).

  - Integrate a persistent cloud vector store like Pinecone for long-term memory.

AI-Web-Context-Bot: Website-Based RAG Assistant
🚀 Project Overview
AI-Web-Context-Bot is a Retrieval-Augmented Generation (RAG) application that turns any website into a conversational knowledge base. Users can provide a URL, and the bot will crawl, extract, and index the content to answer specific queries.

🏗️ Architecture & Requirements
This project implements a complete RAG pipeline with the following specifications:

Streamlit UI: A clean chat interface for user interaction.

Data Extraction: Content is extracted using WebBaseLoader, focusing on core information by removing noise.

Semantic Chunking: Documents are split into segments of 1000 characters with a 200-character overlap to preserve context.

Vector Database: Embeddings are generated and persisted using FAISS for efficient retrieval.

Conversational Memory: Short-term memory is implemented to allow for follow-up questions.

Strict Grounding: If information is missing from the website, the bot responds exactly with: "The answer is not available on the provided website."

🛠️ Tech Stack
Framework: LangChain (Orchestration).

LLM: Llama-3.3-70b (via Groq).

Embeddings: sentence-transformers/all-MiniLM-L6-v2.

Vector Storage: FAISS (Local).

💻 Setup and Run
Clone the Repo:

Bash
git clone https://github.com/arpitpatidar26/AI-Web-Context-Bot.git
cd AI-Web-Context-Bot
Install Dependencies:

Bash
pip install -r requirements.txt
Run Application:

Bash
streamlit run app.py
🚀 Final Push Instructions
Now that you have all the files (app.py, backend.py, README.md, requirements.txt, and .gitignore), run these commands in your terminal:

Bash
git init
git add .
git commit -m "Complete project: AI-Web-Context-Bot with mandatory RAG requirements"
git branch -M main
git remote add origin https://github.com/arpitpatidar26/AI-Web-Context-Bot.git
git push -u origin main





AI-Web-Context-Bot: Website-Based RAG Assistant
🚀 Project Overview
AI-Web-Context-Bot is a Retrieval-Augmented Generation (RAG) application that turns any website into a conversational knowledge base. Users provide a URL, and the bot crawls, extracts, and indexes the content to answer queries with high factual accuracy.

🏗️ Architecture Explanation
The system follows a standard RAG pipeline:
Ingestion: WebBaseLoader extracts raw HTML content from the provided URL.

Chunking: RecursiveCharacterTextSplitter breaks text into 1000-character segments with a 200-character overlap to maintain semantic continuity.

Indexing: Text segments are converted into embeddings and stored in a local FAISS index.

Retrieval: The system performs a similarity search to find the top $k$ relevant chunks for a user query.

Generation: A rephrasing chain ensures the query is standalone, and a QA chain generates the final answer using the retrieved context.

🛠️ Frameworks & ToolsFramework: 
LangChain was used for its robust ecosystem in managing document loaders, prompt templates, and chain orchestration.

LLM Model: Llama-3.3-70b-versatile (via Groq).
Why: It offers state-of-the-art reasoning capabilities with exceptionally low latency via Groq's LPUs, making the chatbot feel responsive in real-time.

Vector Database: FAISS (Facebook AI Similarity Search).
Why: It is an efficient, open-source library for dense vector similarity search that runs locally on CPU, removing the need for external cloud database overhead.

Embedding Strategy: sentence-transformers/all-MiniLM-L6-v2.
Why: This model provides a great balance between performance and speed for English text, running locally to ensure data privacy and zero API costs for embeddings.

💻 Setup and Run Instructions

Clone the Repo:
Bash
git clone https://github.com/arpitpatidar26/AI-Web-Context-Bot.git
cd AI-Web-Context-Bot

Install Dependencies:
Bash
pip install -r requirements.txt

Run Application:
Bash
streamlit run app.py


📝 Assumptions, Limitations & Future 
ImprovementsAssumptions: 
The target website does not block scraping via robots.txt or heavy JavaScript rendering (SPA).

Limitations:
The bot currently processes a single URL rather than crawling an entire domain.
FAISS index is stored locally and is session-dependent in the current Streamlit configuration.

Future Improvements:
Implement LangGraph to create a multi-step research agent that can browse multiple links.
Add support for multi-modal RAG (processing images on the website).
Integrate a persistent cloud vector store like Pinecone for long-term memory.
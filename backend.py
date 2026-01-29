import os
import time

# --- IMPORTS FOR WEB LOADING & TEXT PROCESSING ---
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

# --- IMPORT FOR GROQ CHAT ---
from langchain_groq import ChatGroq

# Vector store path
DB_FAISS_PATH = "vectorstore/db_faiss"

def load_and_process_url(url):
    try:
        loader = WebBaseLoader(web_paths=(url,))
        docs = loader.load()
        if not docs: 
            return "Error: No content found."
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        if not splits: 
            return "Error: No chunks created."
        
        for split in splits:
            split.metadata['source_url'] = url
        return splits
    except Exception as e:
        return f"Error: {str(e)}"

def create_vector_store(splits):
    if not splits: 
        return None
    
    # HUGGINGFACE EMBEDDINGS (FREE)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # BATCH PROCESSING
    batch_size = 20
    vectorstore = None
    print(f"Processing {len(splits)} chunks...")

    for i in range(0, len(splits), batch_size):
        batch = splits[i : i + batch_size]
        if vectorstore is None:
            vectorstore = FAISS.from_documents(batch, embedding=embeddings)
        else:
            vectorstore.add_documents(batch)
        # print(f"Batch {i} done. Sleeping 2s...")
        # time.sleep(2)
    
    vectorstore.save_local(DB_FAISS_PATH)
    return vectorstore

def get_rag_chain(vectorstore):
    # GROQ LLM
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

    retriever = vectorstore.as_retriever()
    output_parser = StrOutputParser()

    # PROMPTS
    rephrase_prompt = ChatPromptTemplate.from_messages([
        ("system", "Rephrase the user question to be standalone given the chat history."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer using the context. If the answer is not in the context, say EXACTLY: 'The answer is not available on the provided website.'\n\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    rephrase_chain = rephrase_prompt | llm | output_parser
    answer_chain = qa_prompt | llm | output_parser

    def run_rag_logic(inputs):
        if inputs.get("chat_history"):
            query = rephrase_chain.invoke(inputs)
        else:
            query = inputs["input"]
        
        docs = retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])
        
        return {"answer": answer_chain.invoke({
            "context": context,
            "chat_history": inputs.get("chat_history", []),
            "input": inputs["input"]
        })}

    return RunnableLambda(run_rag_logic)
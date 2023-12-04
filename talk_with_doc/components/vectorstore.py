import streamlit as st
from langchain.vectorstores import faiss
from langchain.embeddings import OpenAIEmbeddings, GPT4AllEmbeddings
from components.paths import model_path

@st.cache_data
def get_vectorstore(text_chunks, service = "other"):
    if service == "openai":
        embedding = OpenAIEmbeddings()
    else:
        embedding = GPT4AllEmbeddings(
            model_name = model_path,
            n_threads = 4
        )
    vectorstore = faiss.FAISS.from_texts(
        texts = text_chunks,
        embedding = embedding
    )
    return vectorstore
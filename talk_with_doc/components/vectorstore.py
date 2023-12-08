import streamlit as st
from langchain.vectorstores import faiss
from langchain.embeddings.google_palm import GooglePalmEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from components.paths import model_path

@st.cache_data
def get_vectorstore(text_chunks, service = "other"):
    if service == "openai":
        embedding = OpenAIEmbeddings()
    else:
        embedding = GooglePalmEmbeddings()
    vectorstore = faiss.FAISS.from_texts(
        texts = text_chunks,
        embedding = embedding
    )
    return vectorstore
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OctoAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import faiss

@st.cache_data
def extract_raw_text(docs:list):
    text = "" # Store the whole docs as a single string
    for doc in docs: # for handling multiple files
        pdf_reader = PdfReader(doc)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

@st.cache_data
def extract_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )

    text_chunks = text_splitter.split_text(raw_text)
    return text_chunks

@st.cache_data
def get_vectorstore(text_chunks, service = "instructor_embedding"):
    if service == "openai_embedding":
        embedding = OctoAIEmbeddings()
    else:
        embedding = HuggingFaceInstructEmbeddings(
            model_name = "hkunlp/instructor-xl"
        )
    vectorstore = faiss.FAISS.from_texts(
        texts = text_chunks,
        embedding = embedding
    )
    return vectorstore


def main():
    load_dotenv() # Auto loading the Keys from .env file
    st.set_page_config(
        page_title = "Talk With Docs",
        page_icon = "📚",
        layout = "centered",
        initial_sidebar_state = "expanded"
    )

    st.title(
        body = "📚 Talk With Doc"
    )
    st.text_input("Let's start asking questions...")

    with st.sidebar:
        st.header("Your docs")
        st.divider()
        docs = st.file_uploader(
            label = "Upload your pdf here 👇",
            accept_multiple_files = True
        )
        
        if st.button("Process"):
            with st.spinner("Processing..."): # Spinning progress bar
                # extract raw texts from the documents
                raw_text = extract_raw_text(docs)
                # extract text chunks from raw text (Embeddings)
                text_chunks = extract_text_chunks(raw_text)
                # create Vector Store with the Embeddings of text_chunks
                vector_store = get_vectorstore(
                    text_chunks = text_chunks,
                    service = "instructor_embedding"
                )
                st.write(vector_store)

if __name__ == "__main__":
    main()


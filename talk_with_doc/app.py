import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OctoAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import faiss
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from html_templates import css, bot_template, user_template

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

@st.cache_data
def get_conversation_chain(vector_store):
    llm = ChatOpenAI
    memory = ConversationBufferMemory(
        memory_key = "chat_history",
        return_messages = True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vector_store.as_retriever(),
        memory = memory
    )

    return conversation_chain


if "conversation" not in st.session_state:
    st.session_state.conversation = None

def main():
    load_dotenv() # Auto loading the Keys from .env file
    st.set_page_config(
        page_title = "Talk With Docs",
        page_icon = "📚",
        layout = "centered",
        initial_sidebar_state = "expanded"
    )

    # Apply css styling to the web app
    st.write(
        css,
        unsafe_allow_html = True
    )

    st.title(
        body = "📚 Talk With Doc"
    )
    st.text_input("Let's start asking questions...")

    st.write(
        user_template.replace("{{MSG}}", "Hello AI"),
        unsafe_allow_html = True
    )

    st.write(
        bot_template.replace("{{MSG}}", "Hello Human"),
        unsafe_allow_html = True
    )

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
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vector_store)

if __name__ == "__main__":
    main()


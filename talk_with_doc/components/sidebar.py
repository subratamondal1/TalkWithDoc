import streamlit as st
from components.extraction import extract_raw_text, extract_text_chunks
from components.vectorstore import get_vectorstore
from components.conversation_chain import get_conversation_chain

def my_sidebar():
    with st.sidebar:
        st.image(
            image = "https://images.unsplash.com/photo-1544396821-4dd40b938ad3?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGRvY3VtZW50c3xlbnwwfHwwfHx8MA%3D%3D"
        )
        st.divider()

        st.session_state.docs = st.file_uploader(
            label = "Upload your documents here 👇",
            accept_multiple_files = True,
            type = ["PDF"]
        )

        st.session_state.openai_api_key = st.text_input(
            label = "`Required`",
            placeholder = "Your OpenAI API KEY"
        )

        if st.session_state.openai_api_key and st.session_state.docs:
            button = st.button("Process")
            if button:
                with st.spinner("Processing..."): # Spinning progress bar
                    # extract raw texts from the documents
                    raw_text = extract_raw_text(docs)
                    # extract text chunks from raw text (Embeddings)
                    text_chunks = extract_text_chunks(raw_text)
                    # create Vector Store with the Embeddings of text_chunks
                    vector_store = get_vectorstore(
                        text_chunks = text_chunks,
                        service = "other"
                    )
                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vector_store)
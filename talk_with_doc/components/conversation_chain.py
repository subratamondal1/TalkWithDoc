import streamlit as st
from components.paths import model_path
from langchain.chat_models import ChatOpenAI
from langchain.llms.gpt4all import GPT4All
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


@st.cache_data
def get_conversation_chain(vector_store, model = "other"):
    if model == "openai":
        # use openai model
        llm = ChatOpenAI()
    else:
        # use huggingface model
        llm = GPT4All(
            model_path = model_path,
            model_type = "GGUF",
            n_threads = 4
        )

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

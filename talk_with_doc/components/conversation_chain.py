import streamlit as st
from components.paths import model_path
from langchain.chat_models import ChatOpenAI
from langchain.llms.gpt4all import GPT4All
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms.google_palm import GooglePalm


# @st.cache_data
def get_conversation_chain(vector_store, model = "other"):
    if model == "openai":
        # use openai model
        llm = ChatOpenAI()
    else:
        # use googel palm model
        llm = GooglePalm()

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

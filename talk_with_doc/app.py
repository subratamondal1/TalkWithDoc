import streamlit as st
from dotenv import load_dotenv
from components.sidebar import my_sidebar
from components.html_templates import css, bot_template, user_template

def  handle_user_input(user_question):
    response = st.session_state.conversation(
        {
            "question":user_question
        }
    )

    st.session_state.chat_history = response["chat_history"]
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html = True
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content),
                unsafe_allow_html = True
            )

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

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = None

    if "docs" not in st.session_state:
        st.session_state.docs = None

    st.title(
        body = "📚 Talk With Doc"
    )

    if not st.session_state.openai_api_key:
        st.warning("OpenAI API Key not detected ⚠️")
    if not st.session_state.docs:
        st.warning("Docs not detected ⚠️")
    
    if (st.session_state.openai_api_key is not None) and (st.session_state.docs is not None):
        st.success("Success 🎉")

    user_question = st.text_input("Let's start asking questions...")
    if user_question:
        handle_user_input(user_question)

    st.write(
        user_template.replace("{{MSG}}", ""),
        unsafe_allow_html = True
    )

    st.write(
        bot_template.replace("{{MSG}}", "Hi, I'm your AI Assistant"),
        unsafe_allow_html = True
    )

    my_sidebar()

if __name__ == "__main__":
    main()


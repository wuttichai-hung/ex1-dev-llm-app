import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI

# from dotenv import load_dotenv
# load_dotenv(override=True)

st.write("# Welcome to Translation App")
with st.sidebar:
    st.title('Google API Key Settings')
    st.write("Get Google API Key [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)")
    google_api_key = st.text_input('Enter your Google API key:', type='password')
    language = st.selectbox(
        "Translate to?",
        ("English", "Chinese", "Thai")
    )
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=1.0, step=0.05)


if google_api_key:
    prompt_template = ChatPromptTemplate.from_messages([
        ('system', "Translate the following into {language}:"),
        ('user', 'Text: {text}')
    ])
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=temperature, google_api_key=google_api_key)
    parser = StrOutputParser()
    chain = prompt_template | llm | parser
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
        
    # Display chat messages from history on app rerun
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if user_input := st.chat_input("Ask me a question?"):
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # Display assistant response in chat message container
        with st.chat_message("ai"):
            with st.spinner("Thinking..."):
                result = chain.invoke({"text": user_input, "language": language})
                st.write(result)
                st.session_state["chat_history"].append({"role": "ai", "content": result})
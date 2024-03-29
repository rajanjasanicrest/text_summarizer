from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

import streamlit as st 
import os
import time
import random
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def gen_response(user_input):
    prompt = PromptTemplate.from_template('Give the summary for the following article wrapped between <article> tags in not more than 500 words \n <article>{paragraph}</article> ' )
    model = ChatOpenAI(model='gpt-3.5-turbo')    
    chain = prompt | model | StrOutputParser()
    response = chain.invoke(user_input)
    print("it somehow worked")
    for word in response.split():
        yield word + " "
        time.sleep(0.1)

def gen_initial():
    response = random.choice(
        [
            "Hello! I am Text Summarizer, Pass me an article and I will summarize it for you?",
            "Hola my friend, What can i summarize for you?",
            "Pass me an article, and I will summarize it for you!",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Summarize your Article")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(gen_response(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
else:
    with st.chat_message('assistant'):
        start_message = st.write_stream(gen_initial())
    st.session_state.messages.append({'role':'assistant', "content": start_message})


import pandas as pd
import numpy as np
import streamlit as st
import random
import time
from hugchat import hugchat
from hugchat.login import Login
from time import sleep
#from hugchat_api import HuggingChat
import os

# App title
st.set_page_config(page_title="🤗💬 AABIChat")

sign = Login(email='zurich.suyash@gmail.com', passwd='Roche@2107')
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)
#st.set_page_config(layout="wide")
st.set_page_config(page_title="Roche Creative Generation", layout = "wide")
st.markdown("<h6 style='text-align: center; color: black;'> Intelligent Content Drafing Suite </h6>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'> Instruction Based Promotional Content Generation </h3>", unsafe_allow_html=True)

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 LLMChat App')
    st.markdown('''
    ## About
    This app is an LLM-powered Generative Engine:
    
    💡 Note: Free and Secure Access
    ''')
    # add_vertical_space(5)
    # st.write('Made with ❤️ by [Data Professor](https://youtube.com/dataprofessor)')
    #[OpenAssistant/oasst-sft-6-llama-30b-xor](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor) LLM model

    

#######
# Get the input text from the user

option0 = st.sidebar.selectbox(
'Contemt Designer Role',
('pharma communication', 'scientific communication', 'marketing communication'))
option1 = st.sidebar.selectbox(
'Product',
('Phesgo', 'Tecentriq'))
option2 = st.sidebar.selectbox(
'Target Audience',
('HCP', 'Patients', 'Patients and their Families'))

option3 = st.sidebar.selectbox(
'Tone of Generation',
('Professional','Empathetic', 'Informative', 'Patient-centered','Ethical', 'Engaging','Trustworthy', 'Compassionate and Reassuring'
))

option4 = st.sidebar.selectbox(
'Content Type',
('None','scientific newsletter',' newsletter','scientific Email','email', 'executive summary','scientific blog post','blog post', 
    ))
option5 = st.sidebar.selectbox(
'Objective',
('Increase User Engagement','Generate Interest', 'Share Product Update', 'Increase Product Adoption', ' Provide Hope and Information'
    ))

option6 = st.sidebar.selectbox(
'Output Language',
('','in French', 'in Spanish', 'in German', 
    'in Italian'))

option8 = st.sidebar.selectbox(
'Target Audience Expectation',
('Alternative Treatment', 'Ease of Access', 'Higher Safety', 'Higher Efficacy', 'Quality of life', 'Lower Price'))


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    for dict_message in st.session_state.messages:
        string_dialogue = "You are a helpful assistant."
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    prompt = f"{string_dialogue} {prompt_input} Assistant: "
    return chatbot.query(prompt,web_search=True,truncate=4096)


# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)

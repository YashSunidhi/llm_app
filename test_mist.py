import streamlit as st
import random
import time
import pandas as pd
import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

def query_text(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	

st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = query_text({"inputs": (prompt + ". Assistant: \n\n "),"parameters": {'max_new_tokens': 3500 }})
        st.write(full_response[0]['generated_text'].split('Assistant:')[1])
        #message_placeholder.markdown(full_response)#['generated_text'])
    # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response[0]['generated_text']})


df = pd.DataFrame(st.session_state.messages)
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

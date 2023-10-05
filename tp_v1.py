import pandas as pd
import numpy as np
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from time import sleep
from hugchat_api import HuggingChat
import os

def chatbot():
    st.title("AI powered Chat GPT 💬")
    st.markdown('''
      - This may produce inacurate information about people, places, or facts
      - Limited knowledge of world and events after 2021
      
      
      💡 Note: No Sign-in or API key required!
      ''')
    sign = Login(email='zurich.suyash@gmail.com', passwd='Roche@2107')
    cookies = sign.login()

    # Save cookies to the local directory
    
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)

    
    try:
        cookie=sign.loadCookiesFromDir(cookie_path_dir)
    except Exception as e:
        st.error(f"An error occurred during login: {str(e)}")
        st.stop()
    cookie=sign.loadCookiesFromDir(cookie_dir_path=cookie_path_dir)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Function to generate a response        
    def generate_response(dialogue_history):
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        # Create a new conversation
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        #response = chatbot.chat(dialogue_history, stream=True)
        response = chatbot.query(dialogue_history, web_search=True,truncate=4096)
        if isinstance(response, str):
            return response
        else:
            return response.delta.get("content", "")
    # Accept user input
    if prompt := st.chat_input("Send your query"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Append the dialogue history to the user's prompt
        dialogue_history = "\n".join([message["content"] for message in st.session_state.messages])
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.spinner('Generating response....'):
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                try:
                    for response in generate_response(dialogue_history):
                        full_response += response
                        message_placeholder.markdown(full_response + "▌")
                        sleep(0.01)
                    message_placeholder.markdown(full_response)

                    # Check if there are follow-up questions
                    if "?" in prompt:
                    # Update the chat history with the assistant's response
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        # Clear the chat input box
                        st.session_state.prompt = ""
                        # Set the chat input box value to the assistant's response
                        st.chat_input("Follow-up question", value=full_response)

                    # Update the chat history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"An error occurred during response generation: {str(e)}")
                    # Update the chat history with the error message
                    st.session_state.messages.append({"role": "assistant", "content": f"An error occurred: {str(e)}"})

if __name__=='__main__':
    chatbot()

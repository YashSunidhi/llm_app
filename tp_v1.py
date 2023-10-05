import pandas as pd
import numpy as np
import streamlit as st
import random
import time
from hugchat import hugchat
from hugchat.login import Login
from time import sleep
#from hugchat_api import HuggingChat
from deep_translator import GoogleTranslator
import os
import pathlib
from PIL import Image

# App title
st.set_page_config(page_title="Roche Creative Generation", layout = "wide")
st.markdown("<h6 style='text-align: center; color: black;'> Intelligent Content Drafing Suite </h6>", unsafe_allow_html=True)
#st.markdown("<h3 style='text-align: center; color: grey;'> Instruction Based Promotional Content Generation </h3>", unsafe_allow_html=True)

def text_gen():
    st.markdown("<h3 style='text-align: center; color: grey;'> Instruction Based Promotional Content Generation </h3>", unsafe_allow_html=True)
    hf_email = 'zurich.suyash@gmail.com'
    hf_pass = 'Roche@2107'
    sign = Login(email='zurich.suyash@gmail.com', passwd='Roche@2107')
    cookies = sign.login()
    
    # Save cookies to the local directory
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)
    #st.set_page_config(layout="wide")
    
    
    # Sidebar contents
    with st.sidebar:
        st.title('🤗💬 AABI Chat Assistant')
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
    ('content','scientific newsletter',' newsletter','scientific Email','email', 'executive summary','scientific blog post','blog post', 
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
    st.title("Prompt Design Template")
    option7 = st.text_input('Input your prompt here',"")
    default_prompt = ["As a " + option0 +" expert, Create a content " + option6 + " for " + option2+ ", emphasizing the " +option3+ " tone. Craft a "+ option4+ " that educates them about " + option1 +" role in cancer treatment and its potential benefits. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7]
    #prompt = st.text_input('Input your prompt here')
    prompt_design = st.write(default_prompt[0])
    
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
        # Create a new conversation
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
    
        for dict_message in st.session_state.messages:
            string_dialogue = "You are a helpful assistant."
            if dict_message["role"] == "user":
                string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
        prompt = f"{string_dialogue} {prompt_input} Assistant: "
        return chatbot.query(prompt,web_search=True, truncate = 8192,max_new_tokens= 2048)
    
    
    # User-provided prompt
    if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
    
    # Generate a new response if last message is not from assistant
    #st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, hf_email, hf_pass) 
                st.write(response) 
                st.warning("Referred Resources",icon = '🚨')
                count = 0
                for source in response.web_search_sources:
                    count = count+1
                    st.write(str(count)+ str(": "), source.title, source.link,source.hostname)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
    df = pd.DataFrame(st.session_state.messages)
    def convert_df(df):
       return df.to_csv(sep='\t', index=False)#index=False).encode('utf-8')
    
    csv = convert_df(df)
    
    st.download_button(
       "Press to Download and save",
       csv,
       "file.txt",
       "text/csv",
       key='download-txt'
    )
    


def text_trans():
    st.markdown("<h3 style='text-align: center; color: grey;'> Translation In EU5 Languages </h3>", unsafe_allow_html=True)
    with st.sidebar:
        st.title('🤗💬 AABI Content Translator')
        st.markdown('''
        ## About
        This app is an LLM-powered Generative Engine:
        
        💡 Note: Free and Secure Access
        ''')
        # add_vertical_space(5)
        # st.write('Made with ❤️ by [Data Professor](https://youtube.com/dataprofessor)')
        #[OpenAssistant/oasst-sft-6-llama-30b-xor](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor) LLM model
    uploaded_files = st.sidebar.file_uploader("Choose final text", accept_multiple_files=True, type={"csv", "txt"})
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        #st.write(bytes_data)
        st.markdown(bytes_data)
        if uploaded_file:
            for line in uploaded_file:
                st.markdown(line)
        # file_extension = pathlib.Path(uploaded_file.name).suffix
        # if file_extension=='.csv':
        #     df = pd.read_csv(uploaded_file)
        #     st.dataframe(df)
    #         st.markdown(df['content'].iloc[-1])
    #         #text = st.markdown(df['content'].iloc[-1])
    # #######
    #         # Get the input text from the user
            
    #         # option0 = st.sidebar.select(
    #         # 'Select a Language of Interest',
    #         # ('French', 'German', 'Spanish', 'Italian','Portugense'))

    # if uploaded_files is not None:
    #     df = pd.read_csv(uploaded_files)
    #     text = df['content'].iloc[-1]
    # else:
    #     text = st.text_input(
    #     "Text to analyze",
    #     )
    text = text = st.text_input(
        "Text to analyze",
        )
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Original','French','German','Italian','Spanish'])
    with tab1:
        # Use any translator you like, in this example GoogleTranslator
        #translated = GoogleTranslator(source='auto', target='french').translate(text)
        st.markdown(text)
    with tab2:
        # Use any translator you like, in this example GoogleTranslator
        translated = GoogleTranslator(source='auto', target='french').translate(text)
        st.markdown(translated)
    with tab3:
        # Use any translator you like, in this example GoogleTranslator
        translated = GoogleTranslator(source='auto', target='german').translate(text)
        st.markdown(translated)
    with tab4:
        # Use any translator you like, in this example GoogleTranslator
        translated = GoogleTranslator(source='auto', target='italian').translate(text)
        st.markdown(translated)
    with tab5:
        # Use any translator you like, in this example GoogleTranslator
        translated = GoogleTranslator(source='auto', target='spanish').translate(text)
        st.markdown(translated)
            
def image_gen():
    if 'name' not in st.session_state:
        st.session_state['name'] = '1_image'

    def change_name(name):
      st.session_state['name'] = name
    #######
    # Get the input text from the user
    st.title("Content Driven Image Generation")
    
    
    def file_selector(folder_path='.'):
      filenames = os.listdir(folder_path)
      selected_filename = st.sidebar.selectbox('Select a file', filenames)
      return os.path.join(folder_path, selected_filename)
    
    
    
    
    # Sidebar contents
    with st.sidebar:
      st.title('🤗💬 ImageChat App')
      st.markdown('''
      ## About
      This app is an text-2-image or text/image-2-image Generative Engine:
      
      💡 Note: Free and Secure Access
      ''')
    
    if __name__ == '__main__':
      # Select a file
      if st.sidebar.checkbox('Select a file in current directory'):
          folder_path = '.'
          if st.sidebar.checkbox('Change directory'):
              folder_path = st.text_input('Enter folder path', '.')
          filename = file_selector(folder_path=folder_path)
          st.sidebar.write('You selected `%s` ' % filename)
    
    option1 = st.sidebar.selectbox(
    'Portrait Enhancement',
    ('Basic', 'Hyper-Realistic',"Hospitalized Aesthetic"))
    option2 = st.sidebar.selectbox(
    'Character Portrait',
    ('High Quality', 'Volumetric Lighting'))
    
    option3 = st.sidebar.selectbox(
    'Tone of Generation',
    ('photorealistic','hyper realism', 'highly detailed',
    ))
    
    option4 = st.sidebar.selectbox(
    'Photography',
    ('85mm portrait photography', 'award winning','full shot photograph','intense close-ups'
      ))
    option5 = st.sidebar.selectbox(
    'Landscapes',
    ('Swiss','Scottish', 'French', 'Indian'
      ))
    option8 = st.text_area('Prompt for Generation Content',
    (
    "Create marketing content in English for patients, emphasizing the Professional tone. Draft a Newsletter that educates them about Phesgo role in cancer treatment and its potential benefits. The objective is to Increase User Engagement to those seeking Alternative Treatment options."))
    
    option6 = st.selectbox(
    'Recommended Image Prompts',
    ("A photograph of a doctor or healthcare professional in a clinical setting, looking compassionate and confident while interacting with a patient. This image should convey a sense of trust and expertise.",
    "An illustration or graphic representation of cancer cells or tumors, with arrows or other visual elements highlighting the effects of Phesgo on the cancer cells. This image should help readers understand how Phesgo works and its potential benefits.",
    "A picture of a person receiving chemotherapy or other cancer treatments, with a caption or surrounding text that discusses the potential side effects and limitations of traditional cancer treatments. This image should help readers empathize with the need for alternative treatment options.",
    "A diagram or flowchart showing the mechanism of action of Phesgo, highlighting how it targets and destroys cancer cells while minimizing harm to healthy cells. This image should help readers understand the science behind Phesgo and its unique advantages.",
    "A photo of a patient who has benefited from Phesgo treatment, with a testimonial quote or accompanying text that describes their positive experience. This image should help build credibility and trust with readers.",
    "An infographic comparing the effectiveness and safety of Phesgo to other cancer treatments, using charts, graphs, or other visual elements to highlight the benefits of Phesgo. This image should help readers see the value of considering Phesgo as an alternative treatment option.",
    "A stylized image of the Phesgo logo or branding, used consistently throughout the newsletter to reinforce the company's identity and message. This image should be visually appealing and memorable.",
    "A photograph or illustration of a person in a natural setting, such as a park or garden, symbolizing hope, renewal, and the possibility of healing. This image should evoke emotions and create a positive association with Phesgo.",
    "A chart or table listing the key benefits of Phesgo, such as targeted therapy, reduced side effects, and improved quality of life. This image should summarize the main points of the newsletter and serve as a quick reference guide for readers.",
    "A call-to-action button or banner, encouraging readers to take the next step and learn more about Phesgo, request information, or schedule a consultation. This image should be prominently displayed and designed to prompt engagement."))
    
    option7 = st.selectbox('Recommended feedback here',("","Create a very high quality image. "," Try emphasizing on facial expression."))
    option9 = st.text_input("Insert Your feedback","")
    default_prompt = [ option6 + str(" ")+ option1 + str(", ") +  option2+  str(", ")+ option3+  str(", ")+ option4+  str(", ")+ option5+ str(", ")+option7 + str(" ") +option9]
    #prompt = st.text_input('Input your prompt here')
    st.markdown("<h3 style='text-align: center; color: grey;'> Final Instruction for Image Generation </h3>", unsafe_allow_html=True)
    prompt_design = st.warning(default_prompt[0],icon='🤖')
    
    on = st.toggle('Examine Generated Images')
    
    if on:
    
      #st.header(st.session_state['name'])
      with st.spinner("Thinking..."):
          time.sleep(10)
          tab1, tab2, tab3 = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
          with tab1:
              tot1 = st.image("./images_generated/prompt_2.png")
              tot11 = st.button('Select Image 1', on_click=change_name, args=['1_image'])
              if tot11:
                  with open("./images_generated/prompt_2.png", "rb") as file:
                      btn = st.download_button(
                              label="Download image",
                              data=file,
                              file_name="flower.png",
                              mime="image/png"
                          )
          with tab2:
              tot2 = st.image("./images_generated/prompt_5.png")
              tot22 = st.button('Select Image 2', on_click=change_name, args=['2_image'])
              if tot22:
                  with open("./images_generated/prompt_5.png", "rb") as file:
                      btn = st.download_button(
                              label="Download image",
                              data=file,
                              file_name="flower.png",
                              mime="image/png"
                          )
          with tab3:
              tot3 = st.image("./images_generated/prompt_4.png")
              tot33 = st.button('Select Image 3', on_click=change_name, args=['3_image'])
              if tot33:
                  with open("./images_generated/prompt_4.png", "rb") as file:
                      btn = st.download_button(
                              label="Download image",
                              data=file,
                              file_name="flower.png",
                              mime="image/png"
                          )
    
    #st.header(st.session_state['name'])
    
    on1 = st.toggle('Examine Generated Infographics')
    
    if on1:
      st.warning('These informgraphics are generated for design ideation. It should not be used for any content creation.',icon="⚠️")
      with st.spinner("Thinking..."):
          time.sleep(10)
    
          #st.header(st.session_state['name'])
          tab1, tab2, tab3 = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
          with tab1:
              tot4 = st.image("./images_generated/info_1.png")
              tot44 = st.button('Select Image 4', on_click=change_name, args=['4_image'])
              if tot44:
                  with open("./images_generated/info_1.png", "rb") as file:
                      btn = st.download_button(
                              label="Download image",
                              data=file,
                              file_name="flower.png",
                              mime="image/png"
                          )
          with tab2:
              tot5 = st.image("./images_generated/info_2.png")
              tot55 = st.button('Select Image 5', on_click=change_name, args=['5_image'])
                          #im = Image.open("/Users/mishrs39/Downloads/auto_tag_chat_app/images_generated/info_3.png")
              if tot55:
                  with open("./images_generated/info_2.png", "rb") as file:
                      btn = st.download_button(
                              label="Download image",
                              data=file,
                              file_name="flower.png",
                              mime="image/png"
                          )
          with tab3:
              tot6 = st.image("./images_generated/info_3.png")
              tot66 = st.button('Select Image 6', on_click=change_name, args=['6_image'])
              #im = Image.open("/Users/mishrs39/Downloads/auto_tag_chat_app/images_generated/info_3.png")
              if tot66:
                  with open("./images_generated/info_3.png", "rb") as file:
                      btn = st.download_button(
                              label="Download image",
                              data=file,
                              file_name="flower.png",
                              mime="image/png"
                          )
def final_out():
    st.markdown("<h3 style='text-align: center; color: grey;'> Integration of Generated Text and Image for final outcome </h3>", unsafe_allow_html=True)
    st.warning('Text and Images are arranged in order',icon="⚠️")
    # Sidebar contents
    with st.sidebar:
      st.title('🤗💬 Content Integration')
      st.markdown('''
      ## About
      Combine Image and Text
      💡 Note: Free and Secure Access
      ''')
    uploaded_files = st.sidebar.file_uploader("Choose final text and image file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        #st.write(bytes_data)
        file_extension = pathlib.Path(uploaded_file.name).suffix
        print("File Extension: ", file_extension)
        if file_extension=='.csv':
            df = pd.read_csv(uploaded_file,encoding = "ISO-8859-1")
            st.dataframe(df)
        if file_extension=='.png':
            st.image(uploaded_file)
        
    
    
    
page_names_to_funcs = {
    "Content Generation": text_gen,
    "Content Translation": text_trans,
    "Image Generation": image_gen,
    "Final Document": final_out,
}

selected_page = st.sidebar.selectbox("Select Gen AI Application", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

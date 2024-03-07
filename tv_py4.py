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
import requests
import io
from PIL import Image
import warnings 
warnings.filterwarnings('ignore')

# App title
st.set_page_config(page_title="Roche Creative Generation", layout = "wide")
st.markdown("<h6 style='text-align: center; color: black;'> Intelligent Content Drafing Suite </h6>", unsafe_allow_html=True)
#st.markdown("<h3 style='text-align: center; color: grey;'> Instruction Based Promotional Content Generation </h3>", unsafe_allow_html=True)

def text_gen():
    #try:
    st.markdown("<h3 style='text-align: center; color: grey;'> Instruction Based Promotional Content Generation </h3>", unsafe_allow_html=True)
    try:
        hf_email = 'zurich.suyash@gmail.com'
        hf_pass = 'Herceptin@2107'
        sign = Login(email='zurich.suyash@gmail.com', passwd='Herceptin@2107')
        cookies = sign.login()
    except:
        pass
    
    # Save cookies to the local directory
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
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
        # id = chatbot.new_conversation()
        # chatbot.change_conversation(id)
        #chatbot.switch_llm(model_v)
    
        for dict_message in st.session_state.messages:
            string_dialogue = "You are a helpful assistant."
            if dict_message["role"] == "user":
                string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
        prompt = f"{string_dialogue} {prompt_input} Assistant: "
        #response = chatbot.query(prompt,web_search=webs,truncate = 4096,max_new_tokens= 4096,return_full_text=True,use_cache=True)
        out_no_web = chatbot.chat(prompt,web_search=False,truncate = 4096,max_new_tokens= 4096,return_full_text=True,use_cache=True)
        return out_no_web

    def generate_response_web(prompt_input, email, passwd):
        # Hugging Face Login
        sign = Login(email, passwd)
        cookies = sign.login()
        # Create ChatBot                        
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        # Create a new conversation
        # id = chatbot.new_conversation()
        # chatbot.change_conversation(id)
        # chatbot.switch_llm(model_v)
    
        for dict_message in st.session_state.messages:
            string_dialogue = "You are a helpful assistant."
            if dict_message["role"] == "user":
                string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
        prompt = f"{string_dialogue} {prompt_input} Assistant: "
        #response = chatbot.query(prompt,web_search=webs,truncate = 4096,max_new_tokens= 4096,return_full_text=True,use_cache=True)
        out_web = chatbot.chat(prompt,web_search=True,truncate = 4096,max_new_tokens= 4096,return_full_text=True,use_cache=True)
        return out_web

    def query_text(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    
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
    #with st.sidebar:
        #st.title('🤗💬 Web Search Inclusion (Default Not Included')
        option0C = st.sidebar.text_area('Input context reference if any','Drug costs are also a barrier to Phesgo use and Safety concerns over fixed SC dosing vs weight-based IV dosing.')
        option0m = st.sidebar.selectbox('Select Model',('Fast Inference Model','Base Inference Model'))
        option0ll = st.sidebar.selectbox('Mode of execution',('Base','Active'))
        option0w = st.sidebar.selectbox('Select Web Search',(False,True))
      
                                                        
        st.title('🤗💬 User Input for Base Prompt')
        ups = st.sidebar.checkbox('Select to use "User Input for Base Prompt Design"')
        if ups:
            option0 = st.sidebar.selectbox(
            'Content Designer Role',
            ('global communication','pharma communication', 'scientific communication', 'marketing communication'))
            option1 = st.sidebar.selectbox(
            'Product',
            ('Ocrevus', ' Tecentriq ','Phesgo',' Polivy ',' Crovalimab ',' Vabysmo '))
            option2 = st.sidebar.selectbox(
            'Target Audience',
            ('HCP', 'Patients', 'Patients and their Families'))
            
            option3 = st.sidebar.selectbox(
            'Tone of Generation',
            ('Engaging','Professional','Empathetic', 'Informative', 'Patient-centered','Ethical', 'Engaging','Trustworthy', 'Compassionate and Reassuring'
            ))
            
            option4 = st.sidebar.selectbox(
            'Content Type',
            ('Email','scientific newsletter',' newsletter','scientific Email', 'executive summary','scientific blog post','blog post', 
                ))
            option5 = st.sidebar.selectbox(
            'Objective',
            ('To improve adoption','Differentiate with Standard of Care (SoC)','Increase User Engagement','Generate Interest', 'Share Product Update', 'Increase Product Adoption', ' Provide Hope and Information'
                ))
            
            option6 = st.sidebar.selectbox(
            'Output Language',
            ('','in French', 'in Spanish', 'in German', 
                'in Italian'))
            
            option8 = st.sidebar.selectbox(
            'Target Audience Expectation',
            ('Alternative Treatment', 'Ease of Access', 'Higher Safety', 'Higher Efficacy', 'Quality of life', 'Lower Price'))
    
            option11 = st.sidebar.selectbox(
            'Indication',
            ('Multiple Sclerosis', 'Breast Cancer', 'Lung Cancer', 'Paroxysmal Nocturnal Hemoglobinuria (PNH)'))
    
            option12 = st.sidebar.selectbox(
            'Company',
            ("Roche's", "Genentech's"))
            st.title("Prompt Design Template")
            option7 = st.text_input('Input your prompt here',"")
            #option0C = st.sidebar.text_area('Input context reference if any','.')
            #default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using information of " + option11 + " in less than 1500 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7 ]
            if option1=='Ocrevus':
                default_prompt = ["As an Global Communication Expert of Brand Team Ocrevus, Write a well structured and engaging email in 1000 words to HCPs, Neurologists to share an update of Insights from Market Research about Ocrevus vs Kesimpta and how we are addressing challenge of Internal Insight . Along with web search, Please use context to draft response from ''' External Insight ''' " + option0C]
            elif option1=='Phesgo':
                default_prompt = ["As an Pharma Communication Expert, Write a engaging email in more than 1000 words to HCPs, aboust Phesgo inregards to address concern of Cost Barriers and Safety issues. Please include specific concern from " + option0C]
                
            prompt_design = st.write(default_prompt[0])

        st.title('🤗💬 Product Positioning')
        pps = st.sidebar.checkbox('Select if you want to pass "Product Positioning"')
        if pps:
            option01 = st.sidebar.text_area('For - Eligible Population','treatment-naive and experienced C5i-eligible PNH patients')
            option02 = st.sidebar.text_area('Who - Target Patient Identifier','value treatment autonomy and convenience')
            option03 = st.sidebar.text_area('Drug - Product Category','next-generation subcutaneous (SC) C5i')
            option04 = st.sidebar.text_area('That Uniquely - Rational differentiator','reducing patient burden through simple q4w SC injections, either administered at home or in a clinical setting')
            option05 = st.sidebar.text_area('Because - Reason to believe','match the proven efficacy and safety of the trusted C5i Standard of Care (SoC) while introducing a novel dose interval-extending recycling mechanism')
            option06 = st.sidebar.text_area('So that - Emotional Benefit','patients to regain control over their lives by managing their PNH effectively')

            tot = "In line with our product positioning strategy, which targets "+ option01 + ",particularly those who " +option02+", we will highlight drug as a" + option03 + ". This product uniquely distinguishes itself by " + option04+ ". The rationale behind this positioning is the product's ability to " +option05+". This, in turn, offers the emotional benefit of allowing " + option06

            if option0C:
                if pps:
                    default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using information of " + option11 + " in less than 1500 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7 + str('""" ')+tot + str(' """ ') + str(' """ ')+ option0C + str(' """ ')]
                    prompt_design = st.write(default_prompt[0])
                else:
                    default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using information of " + option11 + " in less than 1500 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7+ str('""" ') +option0C + str('""" ')]
                    prompt_design = st.write(default_prompt[0])
            elif pps:
                default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using information of " + option11 + " in less than 1500 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7 + str('""" ')+tot + str(' """ ')]
                prompt_design = st.write(default_prompt[0])

    
    
    # User-provided prompt
    if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

  
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if option0ll == 'Base':
                        time.sleep(7)
                        if option1=='Ocrevus':
                            dv = pd.read_csv('content_output_Ocrevus.csv')
                        elif option1=='Phesgo':
                            dv = pd.read_csv('content_output_Phesgo.csv')
                        response = dv['Outcome'][0]
                        st.write(response)
                        message = {"role": "assistant", "content": response}
                    elif option0w==False:
                        if option0m == 'Base Inference Model':
                            response = generate_response(prompt, hf_email, hf_pass)
                            st.write(response)
                            message = {"role": "assistant", "content": response}
                        elif option0m == 'Fast Inference Model':
                            for dict_message in st.session_state.messages:
                                string_dialogue = "You are a helpful assistant."
                                if dict_message["role"] == "user":
                                    string_dialogue += "User: " + dict_message["content"] + "\n\n"
                                else:
                                    string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
                            prompt = f"{string_dialogue} {prompt} Assistant: "
                            try:
                                API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
                                headers = {"Authorization": "Bearer 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"}
                                output = query_text({"inputs": (prompt),"parameters": {'max_new_tokens': 5500 }})
                                response = output[0]['generated_text'].split('Assistant:')[1]
                                st.write(response)
                                message = {"role": "assistant", "content": response}
                            except:
                                API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
                                headers = {"Authorization": "Bearer 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"}
                                output = query_text({"inputs": (prompt),"parameters": {'max_new_tokens': 5500 }})
                                response = output[0]['generated_text'].split('Assistant:')[1]
                                st.write(response)
                                message = {"role": "assistant", "content": response}
                                
     
                    else:
                        response = generate_response_web(prompt, hf_email,hf_pass)
                        st.write(response)
                        message = {"role": "assistant", "content": response}
                        st.warning("Referred Resources",icon = '🚨')
                        count = 0
                        for source in response.web_search_sources:
                            count = count+1
                            st.write(str(count)+ str(": "), source.title, source.link,source.hostname)
                except:
                    st.write("Seems Like API is down, Please reach out to AABI Team")
                pass

        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
        try:
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
        except:
            pass
    # except:
    #     st.write(" Refresh Web Page of APP")
    #     pass



def text_trans():
    st.markdown("<h3 style='text-align: center; color: grey;'> Translation In EU5 Languages </h3>", unsafe_allow_html=True)
    option0ll = st.sidebar.selectbox('Mode of execution',('Base','Active'))
    with st.sidebar:
        st.title('🤗💬 AABI Content Translator')
        st.markdown('''
        ## About
        This app is an LLM-powered Generative Engine:
        
        💡 Note: Free and Secure Access
        ''')
    if option0ll == 'Active':
        uploaded_files = st.sidebar.file_uploader("Choose final text", accept_multiple_files=True, type={"csv", "txt"})
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            #st.write("filename:", uploaded_file.name)
     
            if uploaded_file is not None:
                #st.write(uploaded_file)
                if uploaded_file.type=='text/plain':
                    from io import StringIO
                    stringio=StringIO(uploaded_file.getvalue().decode('utf-8'))
                    read_data=stringio.read()
                    #st.write(read_data)
                    read_data = read_data.split('assistant')[-1]
    
                    text = st.text_input(
                        "Text to analyze",read_data
                        )
                    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Original','French','German','Italian','Spanish'])
                    with tab1:
                        # Use any translator you like, in this example GoogleTranslator
                        #translated = GoogleTranslator(source='auto', target='french').translate(text)
                        st.markdown(text)
                        st.download_button(
                           "Press to Download and save",
                           text,
                           "file_eng.txt",
                           "text/csv",
                           key='download-txt_e'
                        )
                    with tab2:
                        # Use any translator you like, in this example GoogleTranslator
                        translated = GoogleTranslator(source='auto', target='french').translate(text)
                        st.markdown(translated)
                        st.download_button(
                           "Press to Download and save",
                           translated,
                           "file_french.txt",
                           "text/csv",
                           key='download-txt_f'
                        )                    
                    with tab3:
                        # Use any translator you like, in this example GoogleTranslator
                        translated = GoogleTranslator(source='auto', target='german').translate(text)
                        st.markdown(translated)
                        st.download_button(
                           "Press to Download and save",
                           translated,
                           "file_german.txt",
                           "text/csv",
                           key='download-txt_g')               
                    
                    
                    with tab4:
                        # Use any translator you like, in this example GoogleTranslator
                        translated = GoogleTranslator(source='auto', target='italian').translate(text)
                        st.markdown(translated)
                        st.download_button(
                           "Press to Download and save",
                           translated,
                           "file_italian.txt",
                           "text/csv",
                           key='download-txt_i'  )
                    with tab5:
                        # Use any translator you like, in this example GoogleTranslator
                        translated = GoogleTranslator(source='auto', target='spanish').translate(text)
                        st.markdown(translated)
                        st.download_button(
                           "Press to Download and save",
                           translated,
                           "file_spanish.txt",
                           "text/csv",
                           key='download-txt_s' )
    else:
        time.sleep(7)
        dv = pd.read_csv('content_output1.csv')
        text = dv['Outcome'][0]
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Original','French','German','Italian','Spanish'])
        with tab1:
            # Use any translator you like, in this example GoogleTranslator
            #translated = GoogleTranslator(source='auto', target='french').translate(text)
            st.markdown(text)
            st.download_button(
               "Press to Download and save",
               text,
               "file_eng.txt",
               "text/csv",
               key='download-txt_e'
            )
        with tab2:
            # Use any translator you like, in this example GoogleTranslator
            translated = GoogleTranslator(source='auto', target='french').translate(text)
            st.markdown(translated)
            st.download_button(
               "Press to Download and save",
               translated,
               "file_french.txt",
               "text/csv",
               key='download-txt_f'
            )                    
        with tab3:
            # Use any translator you like, in this example GoogleTranslator
            translated = GoogleTranslator(source='auto', target='german').translate(text)
            st.markdown(translated)
            st.download_button(
               "Press to Download and save",
               translated,
               "file_german.txt",
               "text/csv",
               key='download-txt_g')               
        
    
        with tab4:
            # Use any translator you like, in this example GoogleTranslator
            translated = GoogleTranslator(source='auto', target='italian').translate(text)
            st.markdown(translated)
            st.download_button(
               "Press to Download and save",
               translated,
               "file_italian.txt",
               "text/csv",
               key='download-txt_i'  )
        with tab5:
            # Use any translator you like, in this example GoogleTranslator
            translated = GoogleTranslator(source='auto', target='spanish').translate(text)
            st.markdown(translated)
            st.download_button(
               "Press to Download and save",
               translated,
               "file_spanish.txt",
               "text/csv",
               key='download-txt_s' )

            
def image_gen():
    if 'name' not in st.session_state:
        st.session_state['name'] = '1_image'
    if "messages_1" not in st.session_state:
        st.session_state.messages_1 = []

    def change_name(name):
      st.session_state['name'] = name
    #######
    # Get the input text from the user
    st.markdown("<h4 style='text-align: center; color: grey;'> Image Generation in Context to Text Generation </h4>", unsafe_allow_html=True)
    
    
    def file_selector(folder_path='.'):
      filenames = os.listdir(folder_path)
      selected_filename = st.sidebar.selectbox('Select a file', filenames)
      return os.path.join(folder_path, selected_filename)
    hf_email = 'zurich.suyash@gmail.com'
    hf_pass = 'Herceptin@2107'
    def generate_response(prompt_input, email, passwd):
        # Hugging Face Login
        sign = Login(email, passwd)
        cookies = sign.login()
        # Create ChatBot                        
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        # Create a new conversation
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        chatbot.switch_llm(0)
    
        prompt = f''' Can you write detailed paragraph for 5 images placeholders using artifacts description like number of person, location, geneder, race, eye contact, body posture, facial expression, light description  ensuring realism in instruction suitable for text to image generation from context """  {prompt_input} """. Assistant: '''
        return chatbot.query(prompt,web_search=False)
    # API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    # headers = {"Authorization": "Bearer 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"}
    
    # def query_text(payload):
    # 	response = requests.post(API_URL, headers=headers, json=payload)
    # 	return response.json()
    
    
    # Sidebar contents
    with st.sidebar:
      st.title('🤗💬 ImageChat App')
      st.markdown('''
      ## About
      This app is an text-2-image or text/image-2-image Generative Engine:
      ''')
    
    if __name__ == '__main__':
      # Select a file
      if st.sidebar.checkbox('Select a file in current directory'):
          folder_path = '.'
          if st.sidebar.checkbox('Change directory'):
              folder_path = st.text_input('Enter folder path', '.')
          filename = file_selector(folder_path=folder_path)
          st.sidebar.write('You selected `%s` ' % filename)
    option0ll = st.sidebar.selectbox('Mode of execution',('Base','Active'))
    optionr = st.sidebar.selectbox('Tune to Geopgraphy of Interest',('Default','France','India','China','Mexico','Saudi Arabia'))
    option1 = st.sidebar.selectbox(
    'High Quality Iteration Model 1',
    (110,50,75,100,125))
    option2 = st.sidebar.selectbox(
    'High Quality Iteration Model 2',
    (50,110,75,100,125))
    option3 = st.sidebar.selectbox(
    'High Quality Iteration Model 3',
    (50,110,75,100,125))
    option4 = st.sidebar.selectbox(
    'High Quality Iteration Model 4',
    (110,50,75,100,125))
    option5 = st.sidebar.selectbox(
    'High Quality Iteration Model 5',
    (110,50,75,100,125))

    option8 = st.text_area('Insert Either User Finalized User Instruction or Generated Outcome for Drafting Image Placeholders',
    (""))
    prompt = f''' Can you write detailed paragraph for 5 images placeholders using artifacts description like number of person, location, geneder, race, eye contact, body posture, facial expression, light description  ensuring realism in instruction suitable for text to image generation from context """  {option8} """. Assistant: \n\n'''
    result = st.button('Generating Image Placeholders')
    if result:
        if option0ll == 'Base':
            time.sleep(7)
            dv = pd.read_csv('content_output1.csv')
            text = dv['Image_Outcome'][0]
            st.markdown("<h6 style='text-align: center; color: grey;'> Generated Image Placeholders from Finalized Text Generation Prompt </h6>", unsafe_allow_html=True)
            st.session_state.messages_1.append(text)
            #st.write(text)
        else:
            try:
                API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
                headers = {"Authorization": "Bearer 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"}
                
                def query_text(payload):
                    response = requests.post(API_URL, headers=headers, json=payload)
                    return response.json()
                output = query_text({"inputs": (prompt),"parameters": {'max_new_tokens': 1500 }})
                response = output[0]['generated_text'].split('Assistant:')[1]
                # except:
                #     API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
                #     headers = {"Authorization": "Bearer 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"}
                    
                #     def query_text(payload):
                #         response = requests.post(API_URL, headers=headers, json=payload)
                #         return response.json()
                #     output = query_text({"inputs": (prompt),"parameters": {'max_new_tokens': 1500 }})
                #     response = output[0]['generated_text'].split('Assistant:')[1]
            except:
                st.write("Seems Like API is down, Please carefully examine the outcome")
                try:
                     response = generate_response(option8,hf_email, hf_pass)
                except:
                    pass
            st.session_state.messages_1.append(response)
            st.markdown("<h6 style='text-align: center; color: grey;'> Generated Image Placeholders from Finalized Text Generation Prompt </h6>", unsafe_allow_html=True)
    try:
        st.markdown(st.session_state.messages_1[-1])
    except:
        st.write("No Image Placeholders available")
        pass
            
    # if result is not None:      
    #     dv = pd.read_csv('content_output1.csv')
    #     text = dv['Image_Outcome'][0]
    #     st.markdown(text)


    option6 = st.text_area(
    'Select one of the Recommended Image Placeholder and Paste here')
    option7 = st.selectbox('Recommended feedback here',("","Create a very high quality image. "," Try emphasizing on facial expression."))
    option9 = st.text_input("Insert Your feedback","")

    if option6:
        try:
            st.write(torpedo)
            default_prompt = [ option6 + str(", ")+option7 + str(" ") +option9] # + str(" ")+ option1 + str(", ") +  option2+  str(", ")+ option3+  str(", ")+ option4+  str(", ")+ option5+ str(", ")+option7 + str(" ") +option9]
        except:
            default_prompt = [ option6 + str(", ")+option7 + str(" ") +option9] # + str(" ")+ option1 + str(", ") +  option2+  str(", ")+ option3+  str(", ")+ option4+  str(", ")+ option5+ str(", ")+option7 + str(" ") +option9]
            
    else:
        default_prompt = ["A photograph of a doctor or healthcare professional in a clinical setting, looking compassionate and confident while interacting with a patient. This image should convey a sense of trust and expertise."]           
            #prompt = st.text_input('Input your prompt here')
    st.markdown("<h3 style='text-align: center; color: grey;'> Final Instruction for Image Generation </h3>", unsafe_allow_html=True)
    prompt_design = st.warning('These are AI Generated images, These images are not corrected for any biases than model has learned from training process.',icon='🤖')

    # API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    # headers = {"Authorization": "Bearer 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"}
            
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    on = st.toggle('Examine Generated Images')
    
    
    if on:
    
      #st.header(st.session_state['name'])
        with st.spinner("Thinking..."):
            if option0ll == 'Active':
                st.markdown('''
                    Live text-2-image Generation:💡 
                    ''')
                tab10, tab20, tab30, tab40, tab50 = st.tabs(['Live Generated Image 1','Live Generated Image 2','Live Generated Image 3','Live Generated Image 4','Live Generated Image 5'])
            
                with tab10:
    
                    try:
            
                        #API_URL = "https://api-inference.huggingface.co/models/Yntec/Dreamshaper8"
                        API_URL = "https://api-inference.huggingface.co/models/stablediffusionapi/realistic-vision-v51"
                        headers = {"Authorization": "Bearer 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"}
                        image_bytes = query({
                            "inputs": default_prompt[0] + " high resolution photograph, realistic skin texture, photorealistic, hyper realism, highly detailed, 85mm portrait photography ",
                            "parameters": {'num_inference_steps': (option1) ,'num_images_per_prompt':1},
                            "negative_prompt":['ugly', 'deformed', 'disfigured', 'poor details', 'bad anatomy','deformed fingers','poorly Rendered face','poorly drawn face','poor facial details','poorly drawn hands','poorly rendered hands','low resolution','Images cut out at the top, left, right, bottom.','bad composition','mutated body parts','blurry image','disfigured','oversaturated','bad anatomy','deformed body features','extra fingers', 'mutated hands', 'poorly drawn hands', 'poorly drawn face', 'mutation', 'deformed', 'blurry', 'dehydrated','bad anatomy', 'bad proportions', 'extra limbs', 'cloned face', 'disfigured', 'gross proportions', 'malformed limbs', 'missing arms', 'missing legs', 'extra arms', 'extra legs', 'fused fingers', 'too many fingers', 'long neck', 'username', 'watermark', 'signature']
                        
                        })
                        image = Image.open(io.BytesIO(image_bytes))
                        result = io.BytesIO()
                        image.save(result, format="JPEG")
                        byte_im = result.getvalue()
                
                        tot11 = st.image(image)
                        st.download_button(
                            "Press to Download and save",
                            byte_im,
                            "live_gen_1.jpeg",
                            "image/png",
                            key='download-image_s1' )
                    except:
                        st.write('Could Not Process the Image Generation')
                        pass
            
                with tab20:
                    try:
                        API_URL = "https://api-inference.huggingface.co/models/Yntec/AbsoluteReality"
                        headers = {"Authorization": "Bearer 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"}
                        image_bytes = query({
                            "inputs": default_prompt[0] + " high resolution photograph, realistic skin texture, photorealistic, hyper realism, highly detailed, 85mm portrait photography ",
                            "parameters": {'num_inference_steps': (option2) ,'num_images_per_prompt':1},
                            "negative_prompt":['ugly', 'deformed', 'disfigured', 'poor details', 'bad anatomy','deformed fingers','poorly Rendered face','poorly drawn face','poor facial details','poorly drawn hands','poorly rendered hands','low resolution','Images cut out at the top, left, right, bottom.','bad composition','mutated body parts','blurry image','disfigured','oversaturated','bad anatomy','deformed body features','extra fingers', 'mutated hands', 'poorly drawn hands', 'poorly drawn face', 'mutation', 'deformed', 'blurry', 'dehydrated','bad anatomy', 'bad proportions', 'extra limbs', 'cloned face', 'disfigured', 'gross proportions', 'malformed limbs', 'missing arms', 'missing legs', 'extra arms', 'extra legs', 'fused fingers', 'too many fingers', 'long neck', 'username', 'watermark', 'signature']
                            
                        })
                        image = Image.open(io.BytesIO(image_bytes))
                        result = io.BytesIO()
                        image.save(result, format="JPEG")
                        byte_im = result.getvalue()
                        
                        tot12 = st.image(image)
                        st.download_button(
                            "Press to Download and save",
                            byte_im,
                            "live_gen_2.jpeg",
                            "image/png",
                            key='download-image_s2' )
                    except:
                        st.write('Could Not Process the Image Generation')
                        pass
                        
                with tab30:
                    try:
                        API_URL = "https://api-inference.huggingface.co/models/Yntec/realistic-vision-v12"
                        headers = {"Authorization": "Bearer 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"}
                        image_bytes = query({
                            "inputs": default_prompt[0] + " high resolution photograph, realistic skin texture, photorealistic, hyper realism, highly detailed, 85mm portrait photography ",
                            "parameters": {'num_inference_steps': (option3) ,'num_images_per_prompt':1},
                            "negative_prompt":['ugly', 'deformed', 'disfigured', 'poor details', 'bad anatomy','deformed fingers','poorly Rendered face','poorly drawn face','poor facial details','poorly drawn hands','poorly rendered hands','low resolution','Images cut out at the top, left, right, bottom.','bad composition','mutated body parts','blurry image','disfigured','oversaturated','bad anatomy','deformed body features','extra fingers', 'mutated hands', 'poorly drawn hands', 'poorly drawn face', 'mutation', 'deformed', 'blurry', 'dehydrated','bad anatomy', 'bad proportions', 'extra limbs', 'cloned face', 'disfigured', 'gross proportions', 'malformed limbs', 'missing arms', 'missing legs', 'extra arms', 'extra legs', 'fused fingers', 'too many fingers', 'long neck', 'username', 'watermark', 'signature']
                            
                        })
                        image = Image.open(io.BytesIO(image_bytes))
                        result = io.BytesIO()
                        image.save(result, format="JPEG")
                        byte_im = result.getvalue()
                        
                        tot13 = st.image(image)
                        st.download_button(
                            "Press to Download and save",
                            byte_im,
                            "live_gen_3.jpeg",
                            "image/png",
                            key='download-image_s3' )
                    except:
                        st.write('Could Not Process the Image Generation')
                        pass
    
    
                with tab40:
                    try:
                        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
                        headers = {"Authorization": "Bearer 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"}
                        image_bytes = query({
                            "inputs": default_prompt[0] + " high resolution photograph, realistic skin texture, photorealistic, hyper realism, highly detailed, 85mm portrait photography ",
                            "parameters": {'num_inference_steps': (option4) ,'num_images_per_prompt':1},
                            "negative_prompt":['ugly', 'deformed', 'disfigured', 'poor details', 'bad anatomy','deformed fingers','poorly Rendered face','poorly drawn face','poor facial details','poorly drawn hands','poorly rendered hands','low resolution','Images cut out at the top, left, right, bottom.','bad composition','mutated body parts','blurry image','disfigured','oversaturated','bad anatomy','deformed body features','extra fingers', 'mutated hands', 'poorly drawn hands', 'poorly drawn face', 'mutation', 'deformed', 'blurry', 'dehydrated','bad anatomy', 'bad proportions', 'extra limbs', 'cloned face', 'disfigured', 'gross proportions', 'malformed limbs', 'missing arms', 'missing legs', 'extra arms', 'extra legs', 'fused fingers', 'too many fingers', 'long neck', 'username', 'watermark', 'signature']
                            
                        })
                        image = Image.open(io.BytesIO(image_bytes))
                        result = io.BytesIO()
                        image.save(result, format="JPEG")
                        byte_im = result.getvalue()
                        
                        tot14 = st.image(image)
                        st.download_button(
                            "Press to Download and save",
                            byte_im,
                            "live_gen_4.jpeg",
                            "image/png",
                            key='download-image_s4' )
                    except:
                        st.write('Could Not Process the Image Generation')
                        pass
    
                with tab50:
                    try:
                        API_URL = "https://api-inference.huggingface.co/models/Yntec/CyberRealistic"
                        headers = {"Authorization": "Bearer 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"}
                        image_bytes = query({
                            "inputs": default_prompt[0] + " high resolution photograph, realistic skin texture, photorealistic, hyper realism, highly detailed, 85mm portrait photography ",
                            "parameters": {'num_inference_steps': (option5) ,'num_images_per_prompt':1},
                            "negative_prompt":['ugly', 'deformed', 'disfigured', 'poor details', 'bad anatomy','deformed fingers','poorly Rendered face','poorly drawn face','poor facial details','poorly drawn hands','poorly rendered hands','low resolution','Images cut out at the top, left, right, bottom.','bad composition','mutated body parts','blurry image','disfigured','oversaturated','bad anatomy','deformed body features','extra fingers', 'mutated hands', 'poorly drawn hands', 'poorly drawn face', 'mutation', 'deformed', 'blurry', 'dehydrated','bad anatomy', 'bad proportions', 'extra limbs', 'cloned face', 'disfigured', 'gross proportions', 'malformed limbs', 'missing arms', 'missing legs', 'extra arms', 'extra legs', 'fused fingers', 'too many fingers', 'long neck', 'username', 'watermark', 'signature']
                            
                        })
                        image = Image.open(io.BytesIO(image_bytes))
                        result = io.BytesIO()
                        image.save(result, format="JPEG")
                        byte_im = result.getvalue()
                        
                        tot14 = st.image(image)
                        st.download_button(
                            "Press to Download and save",
                            byte_im,
                            "live_gen_5.jpeg",
                            "image/png",
                            key='download-image_s5' )
                    except:
                        st.write('Could Not Process the Image Generation')
                        pass
            else:
                time.sleep(7)
                if optionr == "Default":
                    tab1, tab2, tab3 = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
                    with tab1:
                        tot1 = st.image("./images_generated/no5.jpg")
                        tot11 = st.button('Select Image 1', on_click=change_name, args=['1_image'])
                        if tot11:
                            with open("./images_generated/no5.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.jpeg",
                                        mime="image/jpeg"
                                    )
                    with tab2:
                        tot2 = st.image("./images_generated/no4.jpg")
                        tot22 = st.button('Select Image 2', on_click=change_name, args=['2_image'])
                        if tot22:
                            with open("./images_generated/no4.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
                    with tab3:
                        tot3 = st.image("./images_generated/no55.jpg")
                        tot33 = st.button('Select Image 3', on_click=change_name, args=['3_image'])
                        if tot33:
                            with open("./images_generated/no55.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
   
                elif optionr == 'France':
                    tab1, tab2, tab3 = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
                    with tab1:
                        tot1 = st.image("./images_generated/no33.jpg")
                        tot11 = st.button('Select Image 1', on_click=change_name, args=['1_image'])
                        if tot11:
                            with open("./images_generated/no33.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.jpeg",
                                        mime="image/jpeg"
                                    )
                    with tab2:
                        tot2 = st.image("./images_generated/no44.jpg")
                        tot22 = st.button('Select Image 2', on_click=change_name, args=['2_image'])
                        if tot22:
                            with open("./images_generated/no44.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
                    with tab3:
                        tot3 = st.image("./images_generated/no555.jpg")
                        tot33 = st.button('Select Image 3', on_click=change_name, args=['3_image'])
                        if tot33:
                            with open("./images_generated/no555.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
    
                elif optionr == 'India':
                    tab1, tab2, tab3 = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
                    with tab1:
                        tot1 = st.image("./images_generated/no_ind_3.jpg")
                        tot11 = st.button('Select Image 1', on_click=change_name, args=['1_image'])
                        if tot11:
                            with open("./images_generated/no_ind_3.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.jpeg",
                                        mime="image/jpeg"
                                    )
                    with tab2:
                        tot2 = st.image("./images_generated/no_ind_4.jpg")
                        tot22 = st.button('Select Image 2', on_click=change_name, args=['2_image'])
                        if tot22:
                            with open("./images_generated/no_ind_5.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
                    with tab3:
                        tot3 = st.image("./images_generated/no_ind_5.jpg")
                        tot33 = st.button('Select Image 3', on_click=change_name, args=['3_image'])
                        if tot33:
                            with open("./images_generated/no_ind_5.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
                elif optionr == 'China':
                    tab1, tab2, tab3 = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
                    with tab1:
                        tot1 = st.image("./images_generated/no_chn_3.jpg")
                        tot11 = st.button('Select Image 1', on_click=change_name, args=['1_image'])
                        if tot11:
                            with open("./images_generated/no_chn_3.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.jpeg",
                                        mime="image/jpeg"
                                    )
                    with tab2:
                        tot2 = st.image("./images_generated/no_chn_4.jpg")
                        tot22 = st.button('Select Image 2', on_click=change_name, args=['2_image'])
                        if tot22:
                            with open("./images_generated/no_chn_5.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
                    with tab3:
                        tot3 = st.image("./images_generated/no_chn_5.jpg")
                        tot33 = st.button('Select Image 3', on_click=change_name, args=['3_image'])
                        if tot33:
                            with open("./images_generated/no_chn_5.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )       

                elif optionr == 'Mexico':
                    tab1, tab2, tab3 = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
                    with tab1:
                        tot1 = st.image("./images_generated/no_mex_3.jpg")
                        tot11 = st.button('Select Image 1', on_click=change_name, args=['1_image'])
                        if tot11:
                            with open("./images_generated/no_mex_3.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.jpeg",
                                        mime="image/jpeg"
                                    )
                    with tab2:
                        tot2 = st.image("./images_generated/no_mex_4.jpg")
                        tot22 = st.button('Select Image 2', on_click=change_name, args=['2_image'])
                        if tot22:
                            with open("./images_generated/no_mex_4.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
                    with tab3:
                        tot3 = st.image("./images_generated/no_mex_5.jpg")
                        tot33 = st.button('Select Image 3', on_click=change_name, args=['3_image'])
                        if tot33:
                            with open("./images_generated/no_mex_5.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )

                else:
                    tab1, tab2, tab3 = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
                    with tab1:
                        tot1 = st.image("./images_generated/no_sau_3.jpg")
                        tot11 = st.button('Select Image 1', on_click=change_name, args=['1_image'])
                        if tot11:
                            with open("./images_generated/no_sau_3.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.jpeg",
                                        mime="image/jpeg"
                                    )
                    with tab2:
                        tot2 = st.image("./images_generated/no_sau_4.jpg")
                        tot22 = st.button('Select Image 2', on_click=change_name, args=['2_image'])
                        if tot22:
                            with open("./images_generated/no_sau_4.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
                    with tab3:
                        tot3 = st.image("./images_generated/no_sau_5.jpg")
                        tot33 = st.button('Select Image 3', on_click=change_name, args=['3_image'])
                        if tot33:
                            with open("./images_generated/no_sau_5.jpg", "rb") as file:
                                btn = st.download_button(
                                        label="Download image",
                                        data=file,
                                        file_name="flower.png",
                                        mime="image/png"
                                    )
        
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


    on1 = st.toggle('Examine Logos Generation based on Known Images')
    
    if on1:
      st.warning('These Logos are generated for design ideation. It should not be used for any content creation.',icon="⚠️")
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
        #st.write("filename:", uploaded_file.name)
        #st.write(bytes_data)
        file_extension = pathlib.Path(uploaded_file.name).suffix
        if uploaded_file:
            #st.write(uploaded_file)
            if uploaded_file.type=='text/plain':
                from io import StringIO
                stringio=StringIO(uploaded_file.getvalue().decode('utf-8'))
                read_data=stringio.read()
                read_data = read_data.split('assistant')[-1]
                st.markdown(read_data)
            #st.dataframe(df)
        if file_extension=='.png':
            st.image(uploaded_file)
        
    
    
    
page_names_to_funcs = {
    "Content Generation": text_gen,
    "Content Translation": text_trans,
    "Image Generation": image_gen,
    "Final Document": final_out,
}
with st.sidebar:
    st.title('Select Gen AI Application')
selected_page = st.sidebar.selectbox("", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

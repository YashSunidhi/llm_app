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

# App title
st.set_page_config(page_title="Roche Creative Generation", layout = "wide")
st.markdown("<h6 style='text-align: center; color: black;'> Intelligent Content Drafing Suite </h6>", unsafe_allow_html=True)
#st.markdown("<h3 style='text-align: center; color: grey;'> Instruction Based Promotional Content Generation </h3>", unsafe_allow_html=True)
def prompt_gen():
    st.markdown("<h3 style='text-align: center; color: grey;'> Instruction Based Promotional Content Generation </h3>", unsafe_allow_html=True)
    hf_email = 'zurich.suyash@gmail.com'
    hf_pass = 'Herceptin@2107'
    sign = Login(email='zurich.suyash@gmail.com', passwd='Herceptin@2107')
    cookies = sign.login()
    
    # Save cookies to the local directory
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)
    #st.set_page_config(layout="wide")

    if "messages_p" not in st.session_state:
        st.session_state.messages_p = []
    
    # def clear_chat_history():
    #     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    # st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": "Bearer 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"}
    
    def query_text(payload):
    	response = requests.post(API_URL, headers=headers, json=payload)
    	return response.json()

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
    
        prompt = f''' As a smart AI Assistant, can you you generate 5 rephrases outcome from this text """  {prompt_input} """. Assistant: '''
        return chatbot.query(prompt,web_search=False)
    
    
    # Sidebar contents
    #with st.sidebar:
    st.sidebar.title('🤗💬 AABI Chat Assistant')
    st.sidebar.markdown('''
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
    # option0w = st.sidebar.selectbox('Select Web Search',(False,True))
    option0C = st.sidebar.text_area('Input context reference if any','')
    #model_val = {'Base Model':0,'Large Model':2,'Small Model':3}
    # model_val = {'Base Model':0,'Large Model':2}
    # option0m = st.sidebar.selectbox('Select Model',('Base Model','Large Model','Small Model'))
    # model_v = model_val[option0m]


                                                    
#with st.sidebar:
    st.sidebar.title('🤗💬 Product Positioning')
    pps = st.sidebar.checkbox('Select if you want to pass "Product Positioning"')
    if pps:
        option01 = st.sidebar.text_area('For - Eligible Population','treatment-naive and experienced C5i-eligible PNH patients')
        option02 = st.sidebar.text_area('Who - Target Patient Identifier','value treatment autonomy and convenience')
        option03 = st.sidebar.text_area('Drug - Product Category','next-generation subcutaneous (SC) C5i')
        option04 = st.sidebar.text_area('That Uniquely - Rational differentiator','reducing patient burden through simple q4w SC injections, either administered at home or in a clinical setting')
        option05 = st.sidebar.text_area('Because - Reason to believe','match the proven efficacy and safety of the trusted C5i Standard of Care (SoC) while introducing a novel dose interval-extending recycling mechanism')
        option06 = st.sidebar.text_area('So that - Emotional Benefit','patients to regain control over their lives by managing their PNH effectively')

        tot = "In line with our product positioning strategy, which targets "+ option01 + ",particularly those who " +option02+", we will highlight drug as a" + option03 + ". This product uniquely distinguishes itself by " + option04+ ". The rationale behind this positioning is the product's ability to " +option05+". This, in turn, offers the emotional benefit of allowing " + option06

#with st.sidebar:
    st.sidebar.title('🤗💬 User Input for Base Prompt')
    ups = st.sidebar.checkbox('Select to use "User Input for Base Prompt Design"')
    if ups:
        option0 = st.sidebar.selectbox(
        'Content Designer Role',
        ('pharma communication', 'scientific communication', 'marketing communication'))
        option1 = st.sidebar.selectbox(
        'Product',
        (' Phesgo ', ' Tecentriq ',' Ocrevus ',' Polivy ',' Crovalimab ',' Vabysmo '))
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
        ('Differentiate with Standard of Care (SoC)','Increase User Engagement','Generate Interest', 'Share Product Update', 'Increase Product Adoption', ' Provide Hope and Information'
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
        ("Genentech's", "Roche's"))
        st.title("Prompt Design Template")
        option7 = st.text_input('Input your prompt here',"")

    if option0C:
        if pps:
            default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using tone of " + option11 + " in less than 3000 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. While generating outcome, please consider recent facts from year 2022 and 2023. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7 + str('""" ')+tot + str(' """ ') + str(' """ ')+ option0C + str(' """ ')]
        else:
            default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using tone of " + option11 + " in less than 3000 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. While generating outcome, please consider recent facts from year 2022 and 2023. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7+ str('""" ') +option0C + str('""" ')]
    elif pps:
        default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using tone of " + option11 + " in less than 3000 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. While generating outcome, please consider recent facts from year 2022 and 2023. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7 + str('""" ')+tot + str(' """ ')]
        #prompt = st.text_input('Input your prompt here')
    else:
        default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using tone of " + option11 + " in less than 3000 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. While generating outcome, please consider recent facts from year 2022 and 2023. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7 ]

    prompt_design = st.write(default_prompt[0])
    prompt = f''' As a smart AI Assistant, can you you generate 5 rephrases outcome from this text """  {prompt_design} """. Assistant: \n\n'''
   
    if st.button('Generating Image Placeholders'):
        try:
            output = query_text({"inputs": (prompt),"parameters": {'max_new_tokens': 5000 }})
            response = output[0]['generated_text'].split('Assistant:')[1]
        except:
            st.write("Seems Like API is down, Please carefully examine the outcome")
            try:
                 response = generate_response(prompt_design,hf_email, hf_pass)
            except:
                pass
        st.session_state.messages_p.append(response)

    
    
  

    df = pd.DataFrame(st.session_state.messages_p)
        
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

def text_gen():
    st.markdown("<h3 style='text-align: center; color: grey;'> Instruction Based Promotional Content Generation </h3>", unsafe_allow_html=True)
    hf_email = 'zurich.suyash@gmail.com'
    hf_pass = 'Herceptin@2107'
    sign = Login(email='zurich.suyash@gmail.com', passwd='Herceptin@2107')
    cookies = sign.login()
    
    # Save cookies to the local directory
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)
    #st.set_page_config(layout="wide")

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
    
    
    # Sidebar contents
    #with st.sidebar:
    st.sidebar.title('🤗💬 AABI Chat Assistant')
    st.sidebar.markdown('''
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
    option0w = st.sidebar.selectbox('Select Web Search',(False,True))
    option0C = st.sidebar.text_area('Input context reference if any','')
    #model_val = {'Base Model':0,'Large Model':2,'Small Model':3}
    model_val = {'Base Model':0,'Large Model':2}
    option0m = st.sidebar.selectbox('Select Model',('Base Model','Large Model','Small Model'))
    model_v = model_val[option0m]


                                                    
#with st.sidebar:
    st.sidebar.title('🤗💬 Product Positioning')
    pps = st.sidebar.checkbox('Select if you want to pass "Product Positioning"')
    if pps:
        option01 = st.sidebar.text_area('For - Eligible Population','treatment-naive and experienced C5i-eligible PNH patients')
        option02 = st.sidebar.text_area('Who - Target Patient Identifier','value treatment autonomy and convenience')
        option03 = st.sidebar.text_area('Drug - Product Category','next-generation subcutaneous (SC) C5i')
        option04 = st.sidebar.text_area('That Uniquely - Rational differentiator','reducing patient burden through simple q4w SC injections, either administered at home or in a clinical setting')
        option05 = st.sidebar.text_area('Because - Reason to believe','match the proven efficacy and safety of the trusted C5i Standard of Care (SoC) while introducing a novel dose interval-extending recycling mechanism')
        option06 = st.sidebar.text_area('So that - Emotional Benefit','patients to regain control over their lives by managing their PNH effectively')

        tot = "In line with our product positioning strategy, which targets "+ option01 + ",particularly those who " +option02+", we will highlight drug as a" + option03 + ". This product uniquely distinguishes itself by " + option04+ ". The rationale behind this positioning is the product's ability to " +option05+". This, in turn, offers the emotional benefit of allowing " + option06

#with st.sidebar:
    st.sidebar.title('🤗💬 User Input for Base Prompt')
    ups = st.sidebar.checkbox('Select to use "User Input for Base Prompt Design"')
    if ups:
        option0 = st.sidebar.selectbox(
        'Content Designer Role',
        ('pharma communication', 'scientific communication', 'marketing communication'))
        option1 = st.sidebar.selectbox(
        'Product',
        (' Phesgo ', ' Tecentriq ',' Ocrevus ',' Polivy ',' Crovalimab ',' Vabysmo '))
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
        ('Differentiate with Standard of Care (SoC)','Increase User Engagement','Generate Interest', 'Share Product Update', 'Increase Product Adoption', ' Provide Hope and Information'
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
        ("Genentech's", "Roche's"))
        st.title("Prompt Design Template")
        option7 = st.text_input('Input your prompt here',"")

        if option0C:
            if pps:
                default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using tone of " + option11 + " in less than 3000 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. While generating outcome, please consider recent facts from year 2022 and 2023. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7 + str('""" ')+tot + str(' """ ') + str(' """ ')+ option0C + str(' """ ')]
            else:
                default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using tone of " + option11 + " in less than 3000 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. While generating outcome, please consider recent facts from year 2022 and 2023. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7+ str('""" ') +option0C + str('""" ')]
        elif pps:
            default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using tone of " + option11 + " in less than 3000 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. While generating outcome, please consider recent facts from year 2022 and 2023. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7 + str('""" ')+tot + str(' """ ')]
            #prompt = st.text_input('Input your prompt here')
        else:
            default_prompt = ["As a " + option0 +" expert, Write a " +option4 +" using tone of " + option11 + " in less than 3000 words for HCP/ doctors highlighting about " + option12 + option1+ "role in treatment and its potential benefits in terms of mechanism of action, safety, efficacy and clinical trials (trial name, trial objective ,trial dosing /formulation and trial outcome). Use an " +option3+ " tone. While generating outcome, please consider recent facts from year 2022 and 2023. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7 ]

        prompt_design = st.write(default_prompt[0])
    

    
    
    # Function for generating LLM response
    def generate_response(prompt_input, email, passwd, model_v):
        # Hugging Face Login
        sign = Login(email, passwd)
        cookies = sign.login()
        # Create ChatBot                        
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        # Create a new conversation
        # id = chatbot.new_conversation()
        # chatbot.change_conversation(id)
        chatbot.switch_llm(model_v)
    
        for dict_message in st.session_state.messages:
            string_dialogue = "You are a helpful assistant."
            if dict_message["role"] == "user":
                string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
        prompt = f"{string_dialogue} {prompt_input} Assistant: "
        #response = chatbot.query(prompt,web_search=webs,truncate = 4096,max_new_tokens= 4096,return_full_text=True,use_cache=True)
        out_no_web = chatbot.query(prompt,web_search=False,truncate = 4096,max_new_tokens= 4096,return_full_text=True,use_cache=True)
        return out_no_web

    def generate_response_web(prompt_input, email, passwd, model_v):
        # Hugging Face Login
        sign = Login(email, passwd)
        cookies = sign.login()
        # Create ChatBot                        
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        # Create a new conversation
        # id = chatbot.new_conversation()
        # chatbot.change_conversation(id)
        chatbot.switch_llm(model_v)
    
        for dict_message in st.session_state.messages:
            string_dialogue = "You are a helpful assistant."
            if dict_message["role"] == "user":
                string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
        prompt = f"{string_dialogue} {prompt_input} Assistant: "
        #response = chatbot.query(prompt,web_search=webs,truncate = 4096,max_new_tokens= 4096,return_full_text=True,use_cache=True)
        out_web = chatbot.query(prompt,web_search=True,truncate = 4096,max_new_tokens= 4096,return_full_text=True,use_cache=True)
        return out_web
    
    
    # User-provided prompt
    if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
    
    # Generate a new response if last message is not from assistant
    #st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": "Bearer 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"}
    
    def query_text(payload):
    	response = requests.post(API_URL, headers=headers, json=payload)
    	return response.json()
  
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # output = query_text({"inputs": (prompt +". Assistant: \n\n"),"parameters": {'max_new_tokens': 3000 }})
                # response = output[0]['generated_text'].split('Assistant:')[1]
                #try:
                if option0w==False:
                    try:
                        print('I am working on it...')
                        output = query_text({"inputs": (prompt +". Assistant: \n\n"),"parameters": {'max_new_tokens': 3500 }})
                        response = output[0]['generated_text'].split('Assistant:')[1]
                        st.write(response)
                        #st.write(st.session_state.messages[-1]['content'])
                        if not output:
                            response = generate_response(prompt, hf_email, hf_pass, model_v)
                            st.write(response)
                    except:
                        st.write("API Service Down, Lets try another API")
                        
                        #st.session_state.messages.append(message)
                else:
                    try:
                        response = generate_response_web(prompt, hf_email,hf_pass, model_v)
                        st.write(response)
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
    option0 = st.sidebar.selectbox(
        'Select a Language of Interest',
        ('French', 'German', 'Spanish', 'Italian','Portugense'))
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
        #st.write("filename:", uploaded_file.name)
        if uploaded_file:
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
    
        prompt = f''' Can you write detailed description of 5 diverse images placeholders using artifacts like geneder, race, eye contact , body posture, facial expression,  light description etc.  ensuring realism suitable for text to image generation from context """  {prompt_input} """. Assistant: '''
        return chatbot.query(prompt,web_search=False)
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": "Bearer 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"}
    
    def query_text(payload):
    	response = requests.post(API_URL, headers=headers, json=payload)
    	return response.json()
    
    
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
    
    option1 = st.sidebar.selectbox(
    'High Quality Iteration Model 1',
    (110,50,75,100,125))
    option2 = st.sidebar.selectbox(
    'High Quality Iteration Model 2',
    (110,50,75,100,125))
    option3 = st.sidebar.selectbox(
    'High Quality Iteration Model 3',
    (110,50,75,100,125))
    option4 = st.sidebar.selectbox(
    'High Quality Iteration Model 4',
    (110,50,75,100,125))

    option5 = st.sidebar.selectbox(
    'High Quality Iteration Model 5',
    (110,50,75,100,125))
    # option2 = st.sidebar.selectbox(
    # 'Character Portrait',
    # ('High Quality', 'Volumetric Lighting'))
    
    # option3 = st.sidebar.selectbox(
    # 'Tone of Generation',
    # ('photorealistic','hyper realism', 'highly detailed',
    # ))
    
    # option4 = st.sidebar.selectbox(
    # 'Photography',
    # ('85mm portrait photography', 'award winning','full shot photograph','intense close-ups'
    #   ))
    # option5 = st.sidebar.selectbox(
    # 'Landscapes',
    # ('Swiss','Scottish', 'French', 'Indian'
    #   ))
    option8 = st.text_area('Insert Either User Finalized User Instruction or Generated Outcome for Drafting Image Placeholders',
    (""))
    prompt = f''' Can you recommend detailed description as instructions in bullet points for 5 diverse images placeholders using artifacts like geneder, race, eye contact , body posture, facial expression,  light description, image background setting etc.  ensuring realism suitable for task text to image generation from context """  {option8} """. Assistant: \n\n'''
    response_o = []
    if st.button('Generating Image Placeholders'):
        try:
            output = query_text({"inputs": (prompt),"parameters": {'max_new_tokens': 3500 }})
            response = output[0]['generated_text'].split('Assistant:')[1]
        except:
            st.write("Seems Like API is down, Please carefully examine the outcome")
            try:
                 response = generate_response(option8,hf_email, hf_pass)
            except:
                pass
        st.session_state.messages_1.append(response)
        # if response:
        #     #torpedo = st.write(response)
        #     try:
        #         st.session_state.messages_1.append(response)
        #     except:
        #         st.write("Seems Like we missed Connection, Generate Again!!!")
        #     else:
        #         st.session_state.messages_1.append(response.text)
                

    st.markdown("<h6 style='text-align: center; color: grey;'> Generated Image Placeholders from Finalized Text Generation Prompt </h6>", unsafe_allow_html=True)
    try:
        st.markdown(st.session_state.messages_1[-1])
    except:
        st.write("No Image Placeholders available")
        pass
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
    prompt_design = st.warning(default_prompt[0],icon='🤖')

    # API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    # headers = {"Authorization": "Bearer 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"}
            
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    on = st.toggle('Examine Generated Images')
    
    
    if on:
    
      #st.header(st.session_state['name'])
        with st.spinner("Thinking..."):
            st.markdown('''
                Live text-2-image Generation:💡 
                ''')
            tab10, tab20, tab30, tab40, tab50 = st.tabs(['Live Generated Image 1','Live Generated Image 2','Live Generated Image 3','Live Generated Image 4','Live Generated Image 5'])
        
            with tab10:

                try:
        
                    API_URL = "https://api-inference.huggingface.co/models/Yntec/Dreamshaper8"
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
                    API_URL = "https://api-inference.huggingface.co/models/Gauri54damle/sdxl-lora-model"
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
          # #time.sleep(10)
          #   tab1, tab2, tab3 = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
          #   with tab1:
          #       tot1 = st.image("./images_generated/prompt_2.png")
          #       tot11 = st.button('Select Image 1', on_click=change_name, args=['1_image'])
          #       if tot11:
          #           with open("./images_generated/prompt_2.png", "rb") as file:
          #               btn = st.download_button(
          #                       label="Download image",
          #                       data=file,
          #                       file_name="flower.jpeg",
          #                       mime="image/jpeg"
          #                   )
          #   with tab2:
          #       tot2 = st.image("./images_generated/prompt_5.png")
          #       tot22 = st.button('Select Image 2', on_click=change_name, args=['2_image'])
          #       if tot22:
          #           with open("./images_generated/prompt_5.png", "rb") as file:
          #               btn = st.download_button(
          #                       label="Download image",
          #                       data=file,
          #                       file_name="flower.png",
          #                       mime="image/png"
          #                   )
          #   with tab3:
          #       tot3 = st.image("./images_generated/prompt_4.png")
          #       tot33 = st.button('Select Image 3', on_click=change_name, args=['3_image'])
          #       if tot33:
          #           with open("./images_generated/prompt_4.png", "rb") as file:
          #               btn = st.download_button(
          #                       label="Download image",
          #                       data=file,
          #                       file_name="flower.png",
          #                       mime="image/png"
          #                   )
        
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
    "Prompt Design & Generation": prompt_gen,
    "Content Generation": text_gen,
    "Content Translation": text_trans,
    "Image Generation": image_gen,
    "Final Document": final_out,
}
with st.sidebar:
    st.title('Select Gen AI Application')
selected_page = st.sidebar.selectbox("", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

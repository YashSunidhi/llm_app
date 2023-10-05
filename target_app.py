import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from hugchat.login import Login
import time
#from trubrics_utils import trubrics_config, trubrics_successful_feedback
from trubrics.integrations.streamlit import FeedbackCollector
collector = FeedbackCollector(email='smnitrkl50@gmail.com', password='Ram@2107', project="default")
if "response" not in st.session_state:
    st.session_state.response = ""
if "feedback_key" not in st.session_state:
    st.session_state.feedback_key = 0
if "logged_prompt" not in st.session_state:
    st.session_state.logged_prompt = ""
if 'name' not in st.session_state:
    st.session_state['name'] = '1_image'

def change_name(name):
  st.session_state['name'] = name
# Log in to huggingface and grant authorization to huggingchat
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


# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm AABIChat, How may I help you?"]
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

def submit():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ''

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    #response = chatbot.chat(prompt)
    response = chatbot.query(prompt, web_search=True, return_full_text=True,use_cache = True,truncate=4096)
    # count = 0
    # for source in response.web_search_sources:
    #   count = count+1
    #   print(str(count)+ str(": "), source.title, source.link,source.hostname)
    # # Create a new conversation
    # id = chatbot.new_conversation()
    # chatbot.change_conversation(id)
    # # Get conversation list
    conversation_list = chatbot.get_conversation_list()
    return response

def generate_translate(prompt):
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    translate = chatbot.chat(prompt, temperature =0.05)
    return translate

def reset_conversation():
    # st.session_state.response = ""
    # st.session_state.user_input = ""
    st.session_state.generated = ["I'm AABIChat, How may I help you?"]
    st.session_state.past = ['Hi!']
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
    
reset = st.sidebar.button('Reset Chat', on_click=reset_conversation)
# if reset:
#     if 'user_input' not in st.session_state:
#         st.session_state.user_input = ''
# else:
#     user_input = st.session_state.user_input
## Conditional display of AI generated responses as a function of user provided prompts
tabx1, tabx2, tabx3, tabx4 = st.tabs(['Content Gen Workbench','Text Translation/Generation','Image Gen Workbench','Approved Outcome'])
with response_container:
    with tabx1:
        st.title("Prompt Design")
        option7 = st.text_input('Input your prompt here',"")
        default_prompt = ["As a " + option0 +" expert, Create a marketing content " + option6 + " for " + option2+ ", emphasizing the " +option3+ " tone. Craft a "+ option4+ " that educates them about " + option1 +" role in cancer treatment and its potential benefits. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7]
        #prompt = st.text_input('Input your prompt here')
        prompt_design = st.write(default_prompt[0])
        st.title("Using Designed Prompt for Generation")
        ## Applying the user input box
        with input_container:
            user_input = tabx1.text_area(label="user_input", label_visibility="collapsed", placeholder="What would you like to know?",key='widget', on_change=submit)
        user_input = st.session_state.user_input
        resp = []
        us_in = []
        res = []
        if user_input:
            st.warning("User Query",icon = '💬')
            st.markdown(user_input)
            response = generate_response(user_input)
            resp.append(response.text)
            st.warning("Assistant Response",icon = '🤖')
            st.markdown(response.text)
            st.warning("Referred Resources",icon = '🚨')
            count = 0
            for source in response.web_search_sources:
                count = count+1
                res.append((str(count)+ str(": "), source.title, source.link,source.hostname))
                st.write(str(count)+ str(": "), source.title, source.link,source.hostname)

            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)
            st.session_state.user_input == ''
        st.session_state.feedback_key += 1
        tot33 = st.button('Approve Text', on_click=change_name, args=['1_image'])
        if tot33:
            df = pd.DaraFrame(response.text)
            csv = convert_df(df)
            btn = st.download_button(
                  label="Download image",
                  data=csv,
                  file_name="approved.csv",
                  mime="final/csv"
              )
        

        
    
            # # response2 = generate_response(user_input)
            # # response3 = generate_response(user_input)
            # st.session_state.past.append(user_input)
            # st.session_state.generated.append(response)
            # st.warning("User Query",icon = '💬')
            # st.markdown(user_input)
            # st.warning("Assistant Response",icon = '🤖')
            # st.markdown(response)
            # st.warning("Referred Resources",icon = '🚨')
            # count = 0
            # for source in response.web_search_sources:
            #     count = count+1
            #     st.write(str(count)+ str(": "), source.title, source.link,source.hostname)
with tabx2:
    on1 = st.toggle('Examine Translation of Generated Text', key = '_trsw')
    if on1:
        if resp[-1]:
            print(res[-1])
            with st.spinner("Thinking..."):
                try:
                    tab0, tab1, tab2, tab3 = st.tabs(["Generated Outcome","French Translation","German Translation","Spanish Translation"])
                    with tab0:
                        st.markdown(res[-1])
                    with tab1:
                        response1= generate_translate(f''' translate the context in french {str('""" ')+ resp[-1] + str(' """')} ''')
                        st.markdown(response1)
                    # with tab2:
                    #     response2= tab2.write(generate_response(f''' translate the context in german {str('""" ')+ st.session_state["generated"][i] + str(' """')} '''))
                    #     st.markdown(response2)
                    # with tab3:
                    #     response3= tab3.write(generate_response(f''' translate the context in spanish {str('""" ')+ st.session_state["generated"][i] + str(' """')} '''))
                    #     st.markdown(response3)
                except:
                    pass
        #st.session_state.response = response

# if reset:
#     if 'user_input' not in st.session_state:
#         st.session_state.user_input = ''
# else:
#     user_input = st.session_state.user_input
            # st.session_state.generated.append(response2)
            # st.session_state.generated.append(response3)
# # model =  'LLAMA2'
# # email='smnitrkl50@gmail.com'
#     with tabx2:
#         if st.session_state['generated']:
#             #message(st.session_state["generated"][0], key=str(0))
#             for i in range(len(st.session_state['generated'])):
#                 message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
#                 #message(st.session_state["generated"][10], key=str(10))
#                 #tab1, tab2, tab3 = st.tabs(['Generated Outcome 1','Generated Outcome 1','Generated Outcome 1' ])
#                 with st.spinner("Thinking..."):
#                     response_text= st.session_state["generated"][i]
#                     #response_text= st.markdown(st.session_state["generated"][i])
#                     if len(st.session_state["generated"])>1:
#                         on1 = st.toggle('Examine Translation of Generated Text', key = str(i)+'_trs')
#                         if on1: 
#                             #try:
#                             tab1, tab2, tab3, tab4 = st.tabs(["Original Generation","French Translation","German Translation","Spanish Translation"])
#                             with tab1:
#                                 st.markdown(st.session_state["generated"][i])
#                             with tab2:
#                                 response1= generate_translate(f''' translate the context in french {str('""" ')+ st.session_state["generated"][i] + str(' """')} ''')
#                                 st.markdown(response1)
#                             with tab3:
#                                 response2= generate_translate(f''' translate the context in german {str('""" ')+ st.session_state["generated"][i] + str(' """')} ''')
#                                 st.markdown(response2)
#                             with tab4:
#                                 response3= generate_translate(f''' translate the context in spanish {str('""" ')+ st.session_state["generated"][i] + str(' """')} ''')
#                                 st.markdown(response3)
#                             # except:
#                             #     pass
#                     # st.session_state.logged_prompt = collector.log_prompt(
#                     #     config_model={"model": model}, prompt=user_input, generation=response_text, tags=["llm_app.py"], user_id=email
#                     # )
#                     st.session_state.response = response_text
#                     st.session_state.feedback_key += 1
                #break
                    #on1 = st.toggle('Examine Translation of Generated Text', key = str(i)+'_trs')
                    #if on1: 
    
                #st.markdown(st.session_state["generated"][i])
        # model =  'LLAMA2'
        # email='smnitrkl50@gmail.com'
        # if st.session_state.generated:
        #     #st.markdown(f"#### :violet[{st.session_state.response}]")
        
        #     feedback = collector.st_feedback(
        #         component="default",
        #         feedback_type="thumbs",
        #         open_feedback_label="[Optional] Provide additional feedback",
        #         #prompt_id=st.session_state.logged_prompt.id,
        #         model=model,
        #         align="flex-start",
        #         tags=["llm_app.py"],
        #         key=f"feedback_{st.session_state.feedback_key}",  # overwrite with new key
        #         user_id=email,
        #     )
        #     if feedback:
        #         st.write("#### Raw feedback saved to Trubrics:")
        #         st.write(feedback)

with tabx3:
    if 'name1' not in st.session_state:
        st.session_state['name1'] = '2_image'
    def change_name(name):
        st.session_state['name1'] = name
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
    
    option6 = tabx3.selectbox(
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
    
    on4 = tabx3.toggle('Examine Generated Images')
    
    if on4:
    
        #st.header(st.session_state['name'])
        with st.spinner("Thinking..."):
            time.sleep(10)
            tab1a, tab2a, tab3a = tabx3.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
            with tab1a:
                tot1 = tabx3.image("./images_generated/prompt_2.png")
                tot11 = tabx3.button('Select Image 1', on_click=change_name, args=['1_image'])
                if tot11:
                    with open("./images_generated/prompt_2.png", "rb") as file:
                        btn = tabx3.download_button(
                                label="Download image",
                                data=file,
                                file_name="flower.png",
                                mime="image/png"
                            )
            with tab2a:
                tot2 = tabx3.image("./images_generated/prompt_5.png")
                tot22 = tabx3.button('Select Image 2', on_click=change_name, args=['2_image'])
                if tot22:
                    with open("./images_generated/prompt_5.png", "rb") as file:
                        btn = tabx3.download_button(
                                label="Download image",
                                data=file,
                                file_name="flower.png",
                                mime="image/png"
                            )
            with tab3a:
                tot3 = tabx3.image("./images_generated/prompt_4.png")
                tot33 = tabx3.button('Select Image 3', on_click=change_name, args=['3_image'])
                if tot33:
                    with open("./images_generated/prompt_4.png", "rb") as file:
                        btn = tabx3.download_button(
                                label="Download image",
                                data=file,
                                file_name="flower.png",
                                mime="image/png"
                            )
    
    #st.header(st.session_state['name'])
    
    on3 = st.toggle('Examine Generated Infographics')
    
    if on3:
        st.warning('These informgraphics are generated for design ideation. It should not be used for any content creation.',icon="⚠️")
        with st.spinner("Thinking..."):
            time.sleep(10)
    
            #st.header(st.session_state['name'])
            tab1b, tab2b, tab3b = st.tabs(['Generated Image 1','Generated Image 2','Generated Image 3'])
            with tab1b:
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
            with tab2b:
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
            with tab3b:
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

    
with tabx4:
    pass

import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from hugchat.login import Login
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
st.title("Prompt Design")
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

option7 = st.text_input('Input your prompt here',"")

default_prompt = ["As a " + option0 +" expert, Create a marketing content " + option6 + " for " + option2+ ", emphasizing the " +option3+ " tone. Craft a "+ option4+ " that educates them about " + option1 +" role in cancer treatment and its potential benefits. The objective is to " + option5 + " to those seeking "+ option8+" options. " + option7]
#prompt = st.text_input('Input your prompt here')
prompt_design = st.write(default_prompt[0])
st.title("Using Designed Prompt for Generation")
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
## Applying the user input box
with input_container:
    user_input = st.text_area(label="user_input", label_visibility="collapsed", placeholder="What would you like to know?",key='widget', on_change=submit)

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    #response = chatbot.chat(prompt)
    response = chatbot.query(prompt, web_search=True, return_full_text=True,truncate=4096)
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

def reset_conversation():
    # st.session_state.response = ""
    # st.session_state.user_input = ""
    st.session_state.generated = ["I'm AABIChat, How may I help you?"]
    st.session_state.past = ['Hi!']
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
    
reset = st.sidebar.button('Reset Chat', on_click=reset_conversation)
if reset:
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''
else:
    user_input = st.session_state.user_input
## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    
    if user_input:
        response = generate_response(user_input)

        # response2 = generate_response(user_input)
        # response3 = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        st.warning("User Query",icon = '💬')
        st.markdown(user_input)
        st.warning("Assistant Response",icon = '🤖')
        st.markdown(response)

  
        st.warning("Referred Resources",icon = '🚨')
        count = 0
        for source in response.web_search_sources:
            count = count+1
            st.write(str(count)+ str(": "), source.title, source.link,source.hostname)
        # if st.session_state['generated']:
        #     on1 = st.toggle('Examine Translation of Generated Text', key = '_trs')
        #     if on1:
        #         with st.spinner("Thinking..."):
        #             try:
        #                 tab1, tab2, tab3 = st.tabs(["French Translation","German Translation","Spanish Translation"])
        #                 with tab1:
        #                     response1= generate_response(f''' translate the context in french {str('""" ')+ st.session_state["generated"][i] + str(' """')} ''')
        #                     st.markdown(response1)
        #                 with tab2:
        #                     response2= tab2.write(generate_response(f''' translate the context in german {str('""" ')+ st.session_state["generated"][i] + str(' """')} '''))
        #                     st.markdown(response2)
        #                 with tab3:
        #                     response3= tab3.write(generate_response(f''' translate the context in spanish {str('""" ')+ st.session_state["generated"][i] + str(' """')} '''))
        #                     st.markdown(response3)
        #             except:
        #                 pass
        st.session_state.response = response
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
        # st.session_state.generated.append(response2)
        # st.session_state.generated.append(response3)
    # model =  'LLAMA2'
    # email='smnitrkl50@gmail.com'
    if st.session_state['generated']:
        #message(st.session_state["generated"][0], key=str(0))
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            #message(st.session_state["generated"][10], key=str(10))
            #tab1, tab2, tab3 = st.tabs(['Generated Outcome 1','Generated Outcome 1','Generated Outcome 1' ])
            with st.spinner("Thinking..."):
                response_text= st.session_state["generated"][i]
                #response_text= st.markdown(st.session_state["generated"][i])
                if len(st.session_state["generated"])>1:
                    on1 = st.toggle('Examine Translation of Generated Text', key = str(i)+'_trs')
                    if on1: 
                        try:
                            tab1, tab2, tab3 = st.tabs(["French Translation","German Translation","Spanish Translation"])
                            with tab1:
                                response1= generate_response(f''' translate the context in french {str('""" ')+ st.session_state["generated"][i] + str(' """')} ''')
                                st.markdown(response1)
                            with tab2:
                                response2= tab2.write(generate_response(f''' translate the context in german {str('""" ')+ st.session_state["generated"][i] + str(' """')} '''))
                                st.markdown(response2)
                            with tab3:
                                response3= tab3.write(generate_response(f''' translate the context in spanish {str('""" ')+ st.session_state["generated"][i] + str(' """')} '''))
                                st.markdown(response3)
                        except:
                            pass
                # st.session_state.logged_prompt = collector.log_prompt(
                #     config_model={"model": model}, prompt=user_input, generation=response_text, tags=["llm_app.py"], user_id=email
                # )
                st.session_state.response = response_text
                st.session_state.feedback_key += 1
            #break
                #on1 = st.toggle('Examine Translation of Generated Text', key = str(i)+'_trs')
                #if on1: 

            #st.markdown(st.session_state["generated"][i])
model =  'LLAMA2'
email='smnitrkl50@gmail.com'
if st.session_state.generated:
    #st.markdown(f"#### :violet[{st.session_state.response}]")

    feedback = collector.st_feedback(
        component="default",
        feedback_type="thumbs",
        open_feedback_label="[Optional] Provide additional feedback",
        #prompt_id=st.session_state.logged_prompt.id,
        model=model,
        align="flex-start",
        tags=["llm_app.py"],
        key=f"feedback_{st.session_state.feedback_key}",  # overwrite with new key
        user_id=email,
    )
    if feedback:
        st.write("#### Raw feedback saved to Trubrics:")
        st.write(feedback)


                    # Clear the Chat Messages


                # if feedback:
                #     trubrics_successful_feedback(feedback)

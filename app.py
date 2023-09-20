import streamlit as st
#from trubrics_utils import trubrics_config, trubrics_successful_feedback

from trubrics.integrations.streamlit import FeedbackCollector
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def trubrics_config(default_component: bool = True):
    st.subheader("Input your Trubrics credentials:")
    email = st.text_input(
        label="email", placeholder="email", label_visibility="collapsed", value=st.secrets.get("TRUBRICS_EMAIL", "")
    )

    password = st.text_input(
        label="password",
        placeholder="password",
        label_visibility="collapsed",
        type="password",
        value=st.secrets.get("TRUBRICS_PASSWORD", ""),
    )

    if default_component:
        return email, password

    feedback_component = st.text_input(
        label="feedback_component",
        placeholder="Feedback component name",
        label_visibility="collapsed",
    )

    feedback_type = st.radio(
        label="Select the component feedback type:", options=("faces", "thumbs", "textbox"), horizontal=True
    )

    return email, password, feedback_component, feedback_type

model_name_or_path = "TheBloke/WizardLM-13B-V1.2-GPTQ"
#model_name_or_path = 'togethercomputer/LLaMA-2-7B-32K'
#model_name_or_path = 'TheBloke/Yarn-Llama-2-13B-128K-GPTQ'
# To use a different branch, change revision
# For example: revision="main"
model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                             device_map="auto",
                                             trust_remote_code=False,
                                             revision="main")

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

# Inference can also be done using transformers' pipeline

print("*** Pipeline:")
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.1,
    top_p=0.95,
    top_k=40,
    repetition_penalty=1.1
)


if "response" not in st.session_state:
    st.session_state.response = ""
if "feedback_key" not in st.session_state:
    st.session_state.feedback_key = 0
if "logged_prompt" not in st.session_state:
    st.session_state.logged_prompt = ""

st.title("LLM User Feedback with Trubrics")

with st.sidebar:
    email, password = trubrics_config()

if email and password:
    try:
        collector = FeedbackCollector(email=email, password=password, project="default")
    except Exception:
        st.error(f"Error authenticating '{email}' with [Trubrics](https://trubrics.streamlit.app/). Please try again.")
        st.stop()
else:
    st.info(
        "To ask a question to an LLM and save your feedback to Trubrics, add your email and password in the sidebar."
        " Don't have an account yet? Create one for free [here](https://trubrics.streamlit.app/)!"
    )
    st.stop()

models = ("llama2-13b","gpt-3.5-turbo",)
model = st.selectbox(
    "Choose your LLM",
    models,
    help="Consult https://platform.openai.com/docs/models/gpt-3-5 for model info.",
)

# openai.api_key = st.secrets.get("OPENAI_API_KEY")
# if openai.api_key is None:
#     st.info("Please add your OpenAI API key to continue.")
#     st.stop()

prompt = st.text_area(label="Prompt", label_visibility="collapsed", placeholder="What would you like to know?")
button = st.button(f"Ask {model}")
prompt_template=f'''A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {prompt} ASSISTANT:

'''

print("\n\n*** Generate:")

if button:
    response = pipe(prompt_template)
    response_text = response[0]["generated_text"]
    st.session_state.logged_prompt = collector.log_prompt(
        config_model={"model": model}, prompt=prompt, generation=response_text, tags=["llm_app.py"], user_id=email
    )
    st.session_state.response = response_text
    st.session_state.feedback_key += 1

if st.session_state.response:
    st.markdown(f"#### :violet[{st.session_state.response}]")

    feedback = collector.st_feedback(
        component="default",
        feedback_type="thumbs",
        open_feedback_label="[Optional] Provide additional feedback",
        prompt_id=st.session_state.logged_prompt.id,
        model=model,
        align="flex-start",
        tags=["llm_app.py"],
        key=f"feedback_{st.session_state.feedback_key}",  # overwrite with new key
        user_id=email,
    )

    if feedback:
        trubrics_successful_feedback(feedback)

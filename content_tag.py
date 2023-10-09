import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from hugchat.login import Login
import time
import sys, fitz
import pdfplumber
import base64
from pathlib import Path
from PIL import Image
import re
import os
import pandas as pd
import plotly.express as px
import numpy as np
import itertools
import io
import ast

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: black;'> Content Tagging Workbench </h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: black;'> A Step towards Creation of Component Library </h5>", unsafe_allow_html=True)

uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files=True)
file_name = []
data_f = []
for upf in uploaded_files:
    doc = fitz.open(stream = upf.read(), filetype="pdf")
    file_name.append(upf.name)
    data_f.append(doc)


if uploaded_files:
    ontology = st.sidebar.selectbox("select taxonomy of interest",['global','oce-p','oce-d'])
    filen = st.sidebar.selectbox("select upload file of interest",file_name)


    mx = pd.DataFrame(file_name , columns =  ['files_name'])
    mx['data'] = data_f
    #doc = mx[mx['file_name'] ==filen]['data'].reset_index(drop=True)[0]
    col2, col1, col4 = st.tabs(['Key Statistics','Page Review of Uploaded Document', 'Tags Recommendation'])
    col1.markdown("<h3 style='text-align: center; color: grey;'> Selected Page from Document under Review </h3>", unsafe_allow_html=True)

    #for i, k in zip(data_f, filen):
    #st.write(k)
    #doc = i
    doc = mx[mx['files_name'] ==filen]['data'].reset_index(drop=True)[0]
    page_option = col1.selectbox(
    'Page Selection',
    (range(0,len(doc))))

    # text_option = st.sidebar.selectbox(
    # 'Page Selection',
    # ('text', 'blocks', 'words', 'html', 
    #     'dict', 'json', 'rawDict', 'xhtml', 'xml'))
        

    zoom = 2
    mat = fitz.Matrix(zoom, zoom)
    val = f"image_{page_option+1}.png"
    page = doc.load_page(page_option)
    pix = page.get_pixmap(matrix=mat)
    pix.save(os.path.join(os.getcwd(),str(val)))

    imager = Image.open(os.path.join(os.getcwd(),str(val)))
    col1.image(imager, caption=val)
    col1.markdown("<h3 style='text-align: center; color: grey;'> Raw Text Extraction from Page </h3>", unsafe_allow_html=True)
    page = doc[page_option]
    col1.write(page.get_text("spans",sort=True))

    col1.markdown("<h3 style='text-align: center; color: grey;'> Intelligent Extraction Based Outcome </h3>", unsafe_allow_html=True)
    page = doc[page_option]


    # text = page.get_text(text_options)
    #page = doc[1]
    mnbb = []
    for p in range(0,len(doc)):
        page = doc[p]
        # text = page.get_text(text_options)
        #page = doc[1]
        #mnb = []
        all_infos = page.get_text("dict", sort=True)
        for i in range(0, len(all_infos['blocks'])):
            try:
                for n in  range(0, len(all_infos['blocks'][i]['lines'])):
                    m = pd.DataFrame.from_dict(all_infos)['blocks'][i]['lines'][n]['spans'][0]
                    res = {key: m[key] for key in m.keys()
                            & {'size', 'flags', 'font', 'color', 'ascender', 'descender', 'text'}}
                    print(res)

                    mm = pd.DataFrame(list(res.keys()), columns = ['Key Text Attribute'])
                    mm['Text Attribute Value'] = list(res.values())
                    


                    mmm = mm.T
                    mmm.columns = mmm.iloc[0]
                    mmm = mmm[1:]
                    mmm['page'] = p
                    mmm['blocks'] = i
                    mmm['lines'] = n
                    mnbb.append(mmm)
            except:
                pass
    tt = pd.concat(mnbb).reset_index(drop=True)
    tt.rename(columns={"size": "sizes"})

    ### Tables
    torx = []
    num_tab = []
    for p in range(0,len(doc)):
        page = doc[p]
        try:

            # Look for tables on this page and display the table count
            tabs = page.find_tables()
            print(f"{len(tabs.tables)} table(s) on {page}")
            num_tab.append(len(tabs.tables))
            tor = []
            for tab in tabs:
                df = tab.to_pandas()
                df['page'] = p
                tor.append(df)
            torx.append(tor)
        except:
            pass


    tabl = list(itertools.chain.from_iterable(torx))
    #ttb = pd.concat(tabl).reset_index(drop=True)

    ### Images Extraction
    # Output directory for the extracted images
    output_dir = filen
    # Desired output image format
    output_format = "png"
    # Minimum width and height for extracted images
    min_width = 100
    min_height = 100
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    # Iterate over PDF pages
    num_imag = []
    for page_index in range(len(doc)):
        # Get the page itself
        page = doc[page_index]
        # Get image list
        image_list = page.get_images(full=True)
        # Print the number of images found on this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            num_imag.append(len(image_list))
        else:
            num_imag.append(len(image_list))
            print(f"[!] No images found on page {page_index}")
        # Iterate over the images on the page
        for image_index, img in enumerate(image_list, start=1):
            # Get the XREF of the image
            xref = img[0]
            # Extract the image bytes
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            # Get the image extension
            image_ext = base_image["ext"]
            # Load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # Check if the image meets the minimum dimensions and save it
            if image.width >= min_width and image.height >= min_height:
                image.save(
                    open(os.path.join(output_dir, f"image{page_index + 1}_{image_index}.{output_format}"), "wb"),
                    format=output_format.upper())
            else:
                print(f"[-] Skipping image {image_index} on page {page_index} due to its small size.")
    option = col1.selectbox(
    'Document Granularity Selection',
    ('blocks','page', 'lines', 'size', 
        'flags'))

    tom = tt[tt['page']==page_option].groupby(option).agg({'text':' '.join,'font':'unique','size':'unique'})[:]

    col1.dataframe(tom)
    

    col2.markdown("<h3 style='text-align: center; color: grey;'> Key Statistics about Document under Review </h3>", unsafe_allow_html=True)
    cola, colb, colc = col2.columns(3)
    cola.metric(label="Number of Pages", value=tt.page.nunique())
    colb.metric(label="Number of Paragraphs", value=len(tt.groupby(['page','blocks']).agg({'text':'count'}).reset_index()))
    colc.metric(label="Number of Lines", value=len(tt.groupby(['page','blocks','lines']).agg({'text':'count'}).reset_index()))
    #colc.metric(label="Number of Font Size Used", value=tt.size*1000.nunique())
    #cold.metric(label="Number of Flags (type of text) Used", value=np.abs(tt.flags))
    tab1, tab2, tab3, tab4 , tab5 = col2.tabs(['Size and Type of Font','Number of Flags','Color Type','Number of Tables',"Number of Images"])
    tab1.metric(label="Number of Font Type Used", value=tt.font.nunique())
    tab1.metric(label="Number of Size Type Used", value=tt['size'].nunique())
    dft = tt.groupby(['size','font']).agg({'text':'count'}).reset_index()
    fig = px.scatter(dft,x='size',y='font',size='text',title ='Distribution of Font Type and Font Size Across Document')
    tab1.plotly_chart(fig, use_container_width=True)
    tab2.metric(label="Number of Flags Used", value=tt['flags'].nunique())
    dff = tt.groupby(['size','flags']).agg({'text':'count'}).reset_index()
    fig1 = px.scatter(dff,x='size',y='flags',size='text',title ='Distribution of Flag Type and Font Size Across Document')
    tab2.plotly_chart(fig1, use_container_width=True)
    #tab2.dataframe(pd.DataFrame(tt['flags'].unique(),columns =['Flags']))
    tab3.metric(label="Number of Color Used", value=tt.color.nunique())
    dfc = tt.groupby(['font','color','size']).agg({'text':'count'}).reset_index()
    fig2 = px.scatter(dfc,x='font',y='color',size='text',color="size",title ='Distribution of Color Type and Font Type Across Document')
    tab3.plotly_chart(fig2, use_container_width=True)
    tab4.metric(label="Number of Tables like component", value=sum(num_tab))
    tab4.markdown("Page number with tables")
    index = [i for i, x in enumerate(num_tab) if x > 0]
    tab4.write(index)
    tab5.metric(label="Number of Images like component", value=sum(num_imag))
    tab5.markdown("Page number with Images/Chart/Infographics")
    index = [i for i, x in enumerate(num_imag) if x > 0]
    tab5.write(index)
    ### Write Image
    # Iterate over PDF pages
    for page_index in range(len(doc)):
        # Get the page itself
        page = doc[page_index]
        # Get image list
        image_list = page.get_images(full=True)
        # Print the number of images found on this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            num_imag.append(len(image_list))
        else:
            num_imag.append(len(image_list))
            print(f"[!] No images found on page {page_index}")
        # Iterate over the images on the page
        for image_index, img in enumerate(image_list, start=1):
            # Get the XREF of the image
            xref = img[0]
            # Extract the image bytes
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            # Get the image extension
            image_ext = base_image["ext"]
            # Load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # Check if the image meets the minimum dimensions and save it
            if image.width >= min_width and image.height >= min_height:
                image.save(
                    open(os.path.join(output_dir, f"image{page_index + 1}_{image_index}.{output_format}"), "wb"),
                    format=output_format.upper())
            else:
                print(f"[-] Skipping image {image_index} on page {page_index} due to its small size.")
            tab5.image(image, use_column_width=False)


  
    schema = {
        "properties": {
            "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
            "language": {
                "type": "string",
                "enum": ["spanish", "english", "french", "german", "italian"],
            },
            "audience":{
                "type":"string", 
                "enum":['Administrator','Association','Case Manager','Caregiver','Consumer','Decision Maker','General Public','Government','General Practitioner','Healthcare / Regulatory Authorities','Investigator','Instructor','Media / Press','Nurse','Nurse Practitioner','Organization','Patient','Payer','Pharmacist','Prescriber','Specialist'],
                'description':"Roles and entities include healthcare administrators shaping policies, caregivers tending to individuals, decision-makers making strategic choices, governments governing regions, and specialized healthcare practitioners. Additionally, it covers media, educators, and financial entities, each with unique functions and responsibilities in their respective domains.",
            },

            "safety":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Measures intended to reflect the safety of a treatment. Pharmacovigilance (PV or PhV), also known as drug safety, is the pharmacological science relating to the collection, detection, assessment, monitoring, and prevention of adverse effects with pharmaceutical products.",
            },
            "efficacy":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "The measure of the ability of an intervention to produce the desired beneficial clinical effect in average conditions of application, usually determined in non-randomized outcome studies. Treatment effectiveness could be affected by lack of efficacy and/or patient compliance. The probability of benefit to individuals in a defined population from a medical technology applied for a given medical problem under ideal conditions of use. Efficacy is a measure of effect of therapy among appropriate patients in whom treatment is tolerated and effectively administered, under the condition of sufficient patients' compliance, usually determined in randomized trials (NCIt)",
            },
            "symptoms":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Signs and symptoms are the observed or detectable signs, and experienced symptoms of an illness, injury, or condition. General signs and symptoms are the opposite of cardinal, specific, or pathognomonic signs and symptoms. General signs and symptoms - although non-specific - , may in combinations be suggestive of certain diagnoses, helping to narrow down what may be wrong.",
            },
            "surgery":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "The branch of medical science that treats disease or injury by operative procedures.",
            },
            "dose-description":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Amount or range of medication dosing information taken by or administered to the subject collected in text form (GDSR).",
            },
            "dose-form":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Dose form of medication taken by or administered to the subject (GDSR).",
            },
            "route of administration":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Different route/presentation of the product (ex: MabThera SC) will be captured in another field under the Administration Route.",
            },
            "dosage":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "The size or frequency of a dose of a medicine or drug",
            },
            "hospital":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Health care institution providing patient treatment with specialized health science and auxiliary healthcare staff and medical equipment.",
            },
            "immunotherapy":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Therapy designed to induce changes in a patient's immune status in order to treat disease.",
            },
            "radiotherapy":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Treatment of a disease by means of exposure of the target or the whole body to radiation. Radiation therapy is often used as part of curative therapy and occasionally as a component of palliative treatment for cancer. Other uses include total body irradiation prior to transplantation.",
            },
            "Quality of Life":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "The concept holds varying meanings for different people and may evolve over time. For some individuals it implies autonomy, empowerment, capability, and choice; for others, security, social integration, or freedom from stress or illness. (NCI).",
            },
            "Minimal Residual Disease":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Evidence for remaining tumor following primary treatment that is only apparent using highly sensitive techniques.",
            },
            "diagnosis":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "The investigation, analysis and recognition of the presence and nature of disease, condition, or injury from expressed signs and symptoms; also, the scientific determination of any kind; the concise results of such an investigation.",
            },

        },
        "required": ['sentiment', 'language', 'audience', 'safety', 'efficacy', 'symptoms', 'surgery', 'dose-description', 'dose-form', 'route of administration', 'dosage', 'hospital', 'immunotherapy', 'radiotherapy', 'Quality of Life', 'Minimal Residual Disease', 'diagnosis'],
    }

    schema_1 = {
        "properties": {

            "prevention":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "A therapy that is used to prevent latent (asymptomatic) disease from progressing to clinical disease, and also to prevent initiation or recurrence of past disease.",
            },
            "treatment":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Action that does or aims to prevent, cure, ameliorate, or slow progression of a pathological condition(s)",
            },
            "epidemiology":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "The study of the causes, incidence and distribution of disease in the population and its application for prevention or control. (NCIt)",
            },
            "pharmacovigilance":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "The detection, assesment, understanding and prevention of adverse effects of medicines.",
            },
            "patient support programme":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Initiatives led by pharmaceutical companies to improve access, usage, and adherence to prescription drugs.",
            },
            "patient access":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Programs that provide access to an Investigational Medicinal Product for patients with a serious and/or life threatening disease for which no appropriate alternate treatments are available and who are not able to participate in a clinical trial. Patient Access Programs include the study purpose EAP, PTA, CU, PAA and other local country definitions that fit in those 4 categories, such as individual-patient IND, treatment IND, compassionate use, emergency use, named patient use, special access and individual patient use..",
            },
            "content complexity introductory":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Content that doesn't require any previous knowledge to be consumed",
            },
            "home":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Place where a person lives",
            },
            "content complexity intermediate":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Content that requires the consumer to know the basis of the treated topic.",
            },
            "content complexity advanced":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Content that expects the comsumer to have full knowledge of the treated topic.",
            },
            "content complexity expert":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Specialized content that requires a high level of expertise from the consumer on the topic it covers. Usually referred to scientific abstracts or articles.",
            },
            "Non Clinical Topics":{
                "type": "string",
                "enum" : ["congress","mental wellness","lifestyle","e-learning","science","technology","legal","finance","healthcare adminishtration"],
                "description" : "Mental health, encompassing emotional, psychological, and social well-being, influences our thoughts, emotions, actions, and stress management throughout life. The summary mentions various topics, including health and fitness, interactive online seminars, systematic knowledge exploration, practical application of science, compliance, finance, and healthcare management. Healthcare management involves the leadership and administration of public health systems and healthcare networks across sectors.",
            },
            "congress meeting event":{
                "type": "string",
                "enum" : ["pre-event","post-event","market access","press","product information","training"],
                "description" : "The text discusses two time frames: one preceding and one following an event. It emphasizes the importance of delivering appropriate healthcare treatments to patients, ensuring timeliness and cost-effectiveness. It also highlights product information documents, which offer approved details for healthcare professionals and patients about medications.",
            },
            "disease stage":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "The characteristics are qualifiers further specifying the indication. Disease stage is a qualifier describing the different stages the *same* disease can undergo. It does not describe the possible transformations of a disease (e.g. from an adenoma to an adenocarcinoma).",
            },
            "personalised healthcare":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Personalised Healthcare (PHC) aims at bringing together a unique understanding of human biology with new ways to analyse health data by taking into account the individual characteristics of patients and their diseases. PHC capitalises on an increasingly sophisticated understanding of differences among patients, the molecular basis of disease and of how medicines work and has the potential to further improve the efficacy and safety of treatments.",
            },

            "tolerability":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "Evaluation of degree to which overt adverse effects can be tolerated by the subject. (adapted from NCI)",
            },
            "overall survival":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "A measurement of the survival rate for a group of individuals suffering from a disease. ",
            },
            "mechanism of action":{
                "type": "string",
                "enum" : ["yes","no"],
                "description" : "n pharmacology, the term mechanism of action refers to the specific biochemical interaction through which a drug substance produces its pharmacological effect. A mechanism of action usually includes mention of the specific molecular targets to which the drug binds, such as an enzyme or receptor",
            },


        },
        "required": ['prevention', 'treatment', 'epidemiology', 'pharmacovigilance', 'patient support programme', 'patient access', 'content complexity introductory', 'home', 'content complexity intermediate', 'content complexity advanced', 'content complexity expert', 'Non Clinical Topics', 'congress meeting event', 'disease stage', 'personalised healthcare', 'tolerability', 'overall survival', 'mechanism of action'],
    }

    #col3.markdown("<h3 style='text-align: center; color: grey;'> Using Excel to Transform into Desired Schema format </h3>", unsafe_allow_html=True)
    # col3a, col3b = col3.tabs(['Schema Part 1','Schema Part 2'])
    # if ontology=='global':
    #     col3a.json(schema)
    #     col3b.json(schema_1)

    col4.markdown("<h3 style='text-align: center; color: grey;'> Tags Recommendation and Document Debrief Based on Hypothesis </h3>", unsafe_allow_html=True)
    col1a, col2a, col3a = col4.tabs(["Context Priortized","Tags with Explanation", "Document Debrief"])
    # page_option = st.sidebar.selectbox(
    # 'Page Selection',
    # (range(0,len(doc))))
    col1a.markdown("<h4 style='text-align: center; color: grey;'> Hypothesis: For PPT like PDF, Title  and Subtitle might contain most important information </h4>", unsafe_allow_html=True)
    #doc = fitz.open(stream=uploaded_file.read(), filetype="pdf") 
    mnbb = []
    for p in range(0,len(doc)):
        page = doc[p]
        # text = page.get_text(text_options)
        #page = doc[1]
        #mnb = []
        all_infos = page.get_text("dict", sort=True)
        for i in range(0, len(all_infos['blocks'])):
            try:
                for n in  range(0, len(all_infos['blocks'][i]['lines'])):
                    m = pd.DataFrame.from_dict(all_infos)['blocks'][i]['lines'][n]['spans'][0]
                    res = {key: m[key] for key in m.keys()
                            & {'size', 'flags', 'font', 'color', 'ascender', 'descender', 'text'}}
                    print(res)

                    mm = pd.DataFrame(list(res.keys()), columns = ['Key Text Attribute'])
                    mm['Text Attribute Value'] = list(res.values())
                    


                    mmm = mm.T
                    mmm.columns = mmm.iloc[0]
                    mmm = mmm[1:]
                    mmm['page'] = p
                    mmm['blocks'] = i
                    mmm['lines'] = n
                    mnbb.append(mmm)
            except:
                pass
    dg = pd.concat(mnbb).reset_index(drop=True)
    
    #dg = pd.read_csv(os.path.join(os.getcwd(),'test_breast_file_csv_updated_3.csv'))
    font_dg = pd.DataFrame(dg[['page','font','size']].value_counts()).reset_index().sort_values('size',ascending=False).reset_index(drop=True)
    #font_dg = font_dg[font_dg['page']==page_option]
    col1a.dataframe(font_dg)
    col1a.markdown("<h4 style='text-align: center; color: grey;'> Priortized Context for Analysis </h4>", unsafe_allow_html=True)
    font_dg.columns = ['page','font','size','count_para']
    if font_dg['count_para'][:10].sum()>=20:
        fontt = font_dg['font'][:10].to_list()
        rot = dg[dg['font'].isin(fontt)][['page','blocks','text']].replace('Reference:','').replace('References:','').drop_duplicates().groupby(['page']).agg({'text':''.join}).drop_duplicates().reset_index(drop=True)
        col1a.markdown(', '.join(rot['text'].to_list()))
    else:
        fontt = font_dg['font'][:15].to_list()
        rot = dg[dg['font'].isin(fontt)][['page','blocks','text']].replace('Reference:','').replace('References:','').drop_duplicates().groupby(['page']).agg({'text':''.join}).drop_duplicates().reset_index(drop=True)
        col1a.markdown(', '.join(rot['text'].to_list()))
    
    #col1.markdown("<h3 style='text-align: center; color: grey;'> Document Understanding Based on Fonts Size (Larger the Fonts Important the message) </h3>", unsafe_allow_html=True)

    col2a.markdown("<h4 style='text-align: center; color: grey;'> Proposed Tags/ Concept for Document </h4>", unsafe_allow_html=True)
    
    # # Log in to huggingface and grant authorization to huggingchat
    # sign = Login(email='zurich.suyash@gmail.com', passwd='Roche@2107')
    # cookies = sign.login()
    
    # # Save cookies to the local directory
    # cookie_path_dir = "./cookies_snapshot"
    # sign.saveCookiesToDir(cookie_path_dir)
    
    # # Load cookies when you restart your program:
    # # sign = login(email, None)
    # # cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.
    # # Create a new conversation
    # # Create a ChatBot
    # chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"
    
    # context = ', '.join(rot['text'])
    # # non stream response
    # query_result = chatbot.query(f''' 
    #         schema :{schema} \n\n
    #         context : {context} \n\n
    #         Assistant: As an intelligent medical expert, Map context strictly based on schema properties description and assign one of the enum strictly in json format with no explanation. \n\n 
    #         ''')
    # col2a.markdown(query_result)
    
    # id = chatbot.new_conversation()
    # chatbot.change_conversation(id)

    # # non stream response
    # query_result_1 = chatbot.query(f''' 
    #         schema :{schema_1} \n\n
    #         context : {context} \n\n
    #         Assistant: As an intelligent medical expert, Map context strictly based on schema properties description and assign one of the enum strictly in json format with no explanation. \n\n 
    #         ''')
    # col2a.markdown(query_result_1)
    
    # id = chatbot.new_conversation()
    # chatbot.change_conversation(id)
    dg_g = pd.read_csv(os.path.join(os.getcwd(),'Demo_lab_1 - Demo_lab.csv'))
    #print(os.getcwd())
    #print(uploaded_file.name)
    if filen == 'Residual Disease Management In HER2+ve Early Breast Cancer Setting - Case Discussion.pdf':
        col2a.write(dg_g[dg_g['Document']==filen].reset_index(drop=True)['Tags'][0])
        col3a.markdown("<h4 style='text-align: center; color: grey;'> Short Debrief of Document </h4>", unsafe_allow_html=True)
        col3a.write(dg_g['Summary'][0])
    elif filen == 'test_breast_file.pdf':
        col2a.write(dg_g[dg_g['Document']==filen].reset_index(drop=True)['Tags'][0])
        col3a.markdown("<h4 style='text-align: center; color: grey;'> Short Debrief of Document </h4>", unsafe_allow_html=True)
        col3a.write(dg_g['Summary'][1])
    elif filen == 'APAC DAN Lung PPoC Insight WP (last updated 2023.08.08).pdf':
        col2a.write(ast.literal_eval(dg_g['Tags'][2]))
        col3a.markdown("<h4 style='text-align: center; color: grey;'> Short Debrief of Document </h4>", unsafe_allow_html=True)
        col3a.write(dg_g['Summary'][2])
    else: #== 'slide deck Dépistage personnalisé cancer du sein - associations de patients.pdf':
        col2a.write(dg_g['Tags'][3])
        col3a.markdown("<h4 style='text-align: center; color: grey;'> Short Debrief of Document </h4>", unsafe_allow_html=True)
        col3a.write(dg_g['Summary'][3])
    #col2a.markdown("<h4 style='text-align: center; color: grey;'> Short Summary based on NLP Model </h4>", unsafe_allow_html=True)
    # query_result_s = chatbot.query(f'''
    #         context : {context} \n\n
    #         Assistant: As an intelligent medical expert, Write a summary in bullet points for the context. \n\n 
    #         ''')
    # col2a.markdown(query_result_s)

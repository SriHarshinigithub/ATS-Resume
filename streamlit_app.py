import streamlit as st
import google.generativeai as genai
import os
import json
import requests
import docx2txt
import PyPDF2 as pdf                                   
from dotenv import load_dotenv
from streamlit_lottie import st_lottie                                        
import time  

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Set up the model configuration for text generation
generation_config = {          
    "temperature": 0.4,                                                               
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "DANGEROUS_CONTENT"]                                                       
]   


def generate_response_from_gemini(input_text):
     # Create a GenerativeModel instance with 'gemini-pro' as the model type
    llm = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
    )
    # Generate content based on the input text
    output = llm.generate_content(input_text)
    # Return the generated text
    return output.text

def extract_text_from_pdf_file(uploaded_file):
    # Use PdfReader to read the text content from a PDF file
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += str(page.extract_text())
    return text_content

def extract_text_from_docx_file(uploaded_file):
    # Use docx2txt to extract text from a DOCX file
    return docx2txt.process(uploaded_file)

# Prompt Template to extract text from
input_prompt_template = """
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in technology, software engineering, data science, full stack web development, cloud enginner, 
cloud developers, devops engineer and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.
Your goal is to analyze the resume against the given job description match the job description and resume by using word to word matching if the word given in the job descriptions matches to the resume it has to give the percentage according to the matching, 
assign a percentage match based on key criteria of description provided and give accurate match percentage, do not change percentage values each time user ask.
if the job description and resume is  same give the percentage 100%.
if the job title and skills in the job  description and resume matches give above 90%
if the resume file size is bigger than the job description see only the skills and job title is matches in the resume then give percentage more than 90%
if the job title and skills in job description summary and resume does not match then give the percentage less than 20%
resume:{text}
description:{job_description}
I want the response in one single string having the structure, do not change job description match percentage every time user ask.
{{"Job Description Match":"%",
   "Missing Keywords":"",
   "Candidate Summary":"",
   "Experience":""}}
"""

# Streamlit app
# Initialize Streamlit app

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
def load_lottieurl(url: str): 
    r = requests.get(url)
    if r.status_code != 200: 
        return None
    return r.json() 

lottie_checking = load_lottiefile("assests/checking.json")

st.set_page_config(page_title="ATS Resume Pro")

st.title("Track My Resume" + ":sunglasses:")
st.markdown('<style>h1{color: orange; text-align: center; font-family:POPPINS}</style>', unsafe_allow_html=True)

st.text(" \n")
st.text(" \n")
st.text(" \n")


job_description = st.text_area("Paste the Job Description",height=300)
uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], help="Please upload a PDF or DOCX file")

if uploaded_file is not None:
    st.markdown('<h8 style="color: lightgreen;text-align: center;">File uploaded successfully!</h8>', unsafe_allow_html=True)
else:
    st.markdown('<h8 style="color: red;text-align: center;">Please upload your Resume!</h8>', unsafe_allow_html=True)
    
    
st.text(" \n")
st.text(" \n")
st.text(" \n")    

col1, col2, col3 = st.columns([4,4,2])

with col1:
    submit_button = st.button("Check ATS Result") 
with col2:
    submit_button1 = st.button("Check Score")
with col3:
    submit_button2 = st.button("How it Works?")

if submit_button:   
    
    if uploaded_file is not None:
        st.text(" \n")
        st.text(" \n")
        st.text(" \n")  
        st.lottie(
            lottie_checking,
            speed=1,
            loop=True,
            quality="low",
            height="200px",
            width="200px",
            key=None,
        )
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)
        response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))

        # Extract Job Description Match percentage from the response
        match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]

        # Remove percentage symbol and convert to float
        match_percentage = float(match_percentage_str.rstrip('%'))
        
        #st.subheader("ATS Evaluation Result:")
        st.markdown('<h3 style="color: yellow;text-align: left;">ATS Evaluation Result</h3>', unsafe_allow_html=True)

        # Display message based on Job Description Match percentage
        if match_percentage >= 80:
            st.markdown('<p style="color: green;font-size: 20px;text-align: left;">Move forward with hiring</p>', unsafe_allow_html=True)
        
            
        else:
            st.markdown('<p style="color: lightgreen;font-size: 20px;text-align: left;">Profile Matched!</p>', unsafe_allow_html=True)
            
        #st.write(response_text)
    else:
        st.text(" \n")
        st.text(" \n")
        st.markdown('<h6 style="color: red;text-align: center;">Please upload your Resume!</h6>', unsafe_allow_html=True)
    
elif submit_button1:  
    if uploaded_file is not None:
        st.lottie(
            lottie_checking,
            speed=1,
            loop=True,
            quality="low",
            height="200px",
            width="200px",
            key=None,
        ) 
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)
        response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))

        # Extract Job Description Match percentage from the response
        match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0] 
        
        st.markdown('<h3 style="color: yellow; text-align: left;">Your ATS Score</h3>', unsafe_allow_html=True)
        
        st.write(f"<div style='text-align:left; font-family: sans-serif; font-size: 20px;'>{match_percentage_str}</div>", unsafe_allow_html=True)
    else:
        st.text(" \n")
        st.text(" \n")
        st.markdown('<h6 style="color: red;text-align: center;">Please upload your Resume!</h6>', unsafe_allow_html=True)        
    
elif submit_button2:
    st.lottie(
            lottie_checking,
            speed=1,
            loop=True,
            quality="low",
            height="200px",
            width="200px",
            key=None,
        ) 
    
    
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
#Import all the libraries
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

#Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Funcion to get response from Gemini Model
def get_response(input, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, prompt])
    return response.text

#Creating function to read pdf
def read_pdf(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text+=str(page.extract_text())
    return text

#Preparing Prompt Template
input_prompt = """
You possess advanced expertise as an Application Tracking System proficient in the tech industry, encompassing software engineering,
data science, dev ops, web development and big data.
Your objective is to assess resumes in alignment with specific job description.
Given the highly competitive job market, your role involves offering top-notch guidance to enhance resume effectively.
Assign the percentage matching, give rating to the resume out of 10, give additional tips to resume......Based on JD and also give,
Missing keywords with high accuracy.


**Resume**: {text}
**Description"": {jd}

I want the response in markdown form and make it attractive as possible, and use emojis wherever needed:

**Match Percentage** : %

**Missing Keywords** : []

**Profile Summary** : ""

**Additional Tips** : ""

**Resume Rating** :
"""


#Build the application using streamlit
st.image("Smart Resume Assistance/logo1.PNG", width=50)
st.title("Smart Resume Assistant!")
st.text("Elevate Your Resume with our Smart ATS")
jd = st.text_area("Insert Job Description!")
upload_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload PDF file")

#Submit Button
submit = st.button("Submit for Analysis!")

if submit:
    if upload_file is not None:
        text = read_pdf(upload_file)
        response = get_response(text, input_prompt)
        st.subheader(response)
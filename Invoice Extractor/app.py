#Import Library
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

#Load the Gen AI api key and connect
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Creating a function to get response from Gemini
def get_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

#Preprocess Image
def input_image_prep(uploaded_file):
    #Check if the file is uploaded
    if uploaded_file is not None:
        #Get the file in bytes
        bytes_info = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type":uploaded_file.type,
                "data": bytes_info
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded!")

#Creating the app
#st.set_page_config(page_title="Invoice Extractor")
st.image('Invoice Extractor/invoice.jpg', width=50)
st.header("Advanced Invoice Extractor")
input = st.text_input("Input Prompt:", key="input")
upload_file = st.file_uploader("Upload the Invoice!", type=["jpg", "jpeg", "png"])

image = ""
if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)


#Prepare prompt for the Invoce
input_prompt = """
As an expert in invoice comprehension, your task is to analyze input images containing invoices 
and provice responses to question based on the content of the image.

Also provice below information by default:
- Person Name on the Bill
- Bill Date
- Company Name
- Total Bill Amount
"""

#CREATE SUBMIT BUTTON
submit = st.button("Analyse Invoice!")

#When Submitted
if submit:
    image_data = input_image_prep(upload_file)
    response = get_response(input, image_data, input_prompt)
    st.subheader("AI Response :")
    st.write(response)
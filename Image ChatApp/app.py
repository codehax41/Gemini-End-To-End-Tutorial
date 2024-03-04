#Load all the libraries
from dotenv import load_dotenv
from PIL import Image
import os
import streamlit as st
import google.generativeai as genai

#Configure Google API
load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Function to load Gemini model and generate response
def get_response(input, image):
    model = genai.GenerativeModel("gemini-pro-vision")
    if input!="":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

#Function to get/create history
def get_session_state():
    return st.session_state

#Initialize the streamlit application
session_state = get_session_state()
if "history" not in session_state:
    session_state.history = []

#st.set_page_config(page_title="Gemini Vision Pro App")
st.image("Image ChatApp/logo.png", width=100)
st.header("Gemini Vision App")
input_query = st.text_input("Input: ", key="input")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

#Show the image
image_data = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

#Create a button
submit = st.button("Ask question!")
#If the button is clicked
if submit:
    response = get_response(input_query, image)
    #Append the history
    session_state.history.append({
        "query":"Image",
        "image":image,
        "response": response
    })
    st.subheader("Vision AI: ")
    st.write(response)

#Display history
st.subheader("History")
for entry in session_state.history:
    query = entry["query"]
    image = entry.get("image")
    response = entry["response"]
    #Use the st.expander
    with st.expander(f"Query: {query}"):
        if image is not None:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        st.write("Response :", response)
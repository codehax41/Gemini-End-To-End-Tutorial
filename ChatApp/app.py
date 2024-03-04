#Import all the libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai


#Configuring Google API key
load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Lets load the Gemini model and its response
def get_response(query):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(query)
    return response.text

#Initialize the streamlit application
#st.set_page_config(page_title="Q&A App")
#Setting logo
st.image('ChatApp/logo.png', width=100)
st.header("Q&A Chat Bot")

#Function to get/create a session state in streamlit
def get_Session_state():
    return st.session_state

#Initialize history list if not already present
session_state = get_Session_state()
if "history" not in session_state:
    session_state.history=[]

#Creating a input field in the UI
input_query = st.text_input("Input: ", key="input")
#Button for submit
submit = st.button("Ask question!")

#When button is clicked
if submit:
    response = get_response(input_query)
    #Append the history
    session_state.history.append({
        "query": input_query,
        "response": response
    })
    #add the query response and print
    st.subheader("AI Bot: ")
    st.write(response)

#Display history
st.subheader("History")
for entry in session_state.history:
    query = entry['query']
    response = entry['response']
    with st.expander(f"Query: {query}"):
        st.write("Response: ", response)
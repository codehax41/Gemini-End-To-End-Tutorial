#Import all the library
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import streamlit as st

#Load the API Key
load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Function to load Google Gemini Vision Model and get response
def get_response_image(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], prompt])
    return response.text

#Function to load Google Gemini Pro Model and get response
def get_response(prompt, input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, input])
    return response.text

#Prep Image Data
def prep_image(uploaded_file):
    #Check if there is any data
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        #Get the image part information
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File is uploaded!")
    
#Initialize the streamlit app
#st.set_page_config(page_title="Planner: Discover and Plan your Culinary Adventures!")
st.image('Planner AI/logo.jpg', width=70)
st.header("Planner: Discover and Plan your Culinary Adventures!")


#Creating radio section choices
section_choice = st.radio("Choose Section:", ("Location Finder", "Trip Planner", "Weather Forecasting", "Restaurant & Hotel Planner"))
###########################################################################################
#If the choice is location finder
if section_choice == "Location Finder":
    upload_file = st.file_uploader("Choose an image", type = ["jpg", "jpeg", "png"])
    image = ""
    if upload_file is not None:
        image = Image.open(upload_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    #Prompt Template
    input_prompt_loc = """
    You are an expert Tourist Guide. As a expert your job is to provide summary about the place and,
    - Location of the place,
    - State & Capital
    - Cordinates of the place
    - Some popular places nearby
    Retun the response using markdown.
    """

    #Button
    submit = st.button("Get Location!")
    if submit:
        image_data = prep_image(upload_file)
        response = get_response_image(image_data, input_prompt_loc)
        st.subheader("Tour Bot: ")
        st.write(response)
###########################################################################################
#If the choice is trip planner
if section_choice == "Trip Planner":

    #Prompt Template
    input_prompt_planner = """
    You are an expert Tour Planner. Your job is to provide recommendations and plan for given location for giner number of days,
    even if number of days is not provided.
    Also, suggest hidden secrets, hotels, and beautiful places we shouldn't forget to visit
    Also tell best month to visit given place.
    Retun the response using markdown.
    """

    #Input
    input_plan = st.text_area("Provide location and number of days to obtain itinerary plan!")
    #Button
    submit1 = st.button("Plan my Trip!")
    if submit1:
        response = get_response(input_prompt_planner, input_plan)
        st.subheader("Planner Bot: ")
        st.write(response)
###########################################################################################
#If the choice is Weather Forecasting
if section_choice == "Weather Forecasting":

    #Prompt Template
    input_prompt_planner = """
    You are an expert weather forecaster. Your job is to provide forecast for given place and you have to provide for next 7 days,
    forecast also, from the current date.
    - Provide Precipitation
    - Provide Humidity
    - Provide Wind
    - Provide Air Quality
    - Provide Cloud Cover
    Retun the response using markdown.
    """
    #Input
    input_plan = st.text_area("Provide location to forecast weather!")
    #Button
    submit1 = st.button("Forecast Weather!")
    if submit1:
        response = get_response(input_prompt_planner, input_plan)
        st.subheader("Weather Bot: ")
        st.write(response)

###########################################################################################
#If the choice is Restaurant & Hotel Planner
if section_choice == "Restaurant & Hotel Planner":

    #Prompt Template
    input_prompt_planner = """
    You are an expert Restaurant & Hotel Planner. 
    Your job is to provide Restaurant & Hotel for given place and you have to provide not very expensive and not very cheap,
    - Provide rating of the restaurant/hotel
    - Top 5 restaurants with address and average cost per cuisine
    - Top 5 hotels with address and average cost per night
    Retun the response using markdown.
    """
    #Input
    input_plan = st.text_area("Provide location to find Hotel & Restaurants!")
    #Button
    submit1 = st.button("Find Restaurant & Hotel!")
    if submit1:
        response = get_response(input_prompt_planner, input_plan)
        st.subheader("Acomodation Bot: ")
        st.write(response)
#Import libraries
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import streamlit as st


#Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Function to load Google Gemini Pro model and get response
def get_response_diet(prompt, input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, input])
    return response.text

#Function to load Google Gemini Vision model and get response
def get_response_nutrition(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], prompt])
    return response.text

#Preprocess image data
def prep_image(uploaded_file):
    #Check if there is any data
    if uploaded_file is not None:
        #Read the file as bytes
        bytes_data = uploaded_file.getvalue()

        #get the image part information
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File is uploaded!")
    
#Configuring Streamlit App
#st.set_page_config(page_title="Health Management: Nutrition Calculator & Diet Planner")
st.image('Nutritionist/logo.jpg', width=70)
st.header("Health: Nutrition Calculator & Diet Planner")

######################################################################################
section_choice1 = st.radio("Choose Section:", ("Nutrition Calculator","Diet Planner"))

#If choice is nutrition calculator
if section_choice1 == "Nutrition Calculator":
    upload_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])
    image = ""
    if upload_file is not None:
        #Show the image
        image = Image.open(upload_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)


    #Prompt Template
    input_prompt_nutrition = """
    You are an expert Nutritionist. As a skilled nutritionist, you're required to analyze the food iems
    in the image and determine the total nutrition value. 
    Additionally, you need to furnish a breakdown of each food item along with its respective content.

    Food item, Serving size, Tatal Cal., Protien (g), Fat,
    Carb (g), Fiber (g), Vit B-12, Vit B-6,
    Iron, Zinc, Mang.

    Use a table to show above informaion.
    """
    ##if the button is clicked
    submit = st.button("Calculate Nutrition value!")
    if submit:
        image_data = prep_image(upload_file)
        response = get_response_nutrition(image_data, input_prompt_nutrition)
        st.subheader("Nutrition AI: ")
        st.write(response)

#If choice is diet planner
if section_choice1 == "Diet Planner":

    #Prompt Template
    input_prompt_diet = """
    You are an expert Nutritionist. 
    If the input contains list of items like fruits or vegetables, you have to give diet plan and suggest
    breakfast, lunch, dinner wrt given item.
    If the input contains numbers, you have to suggest diet plan for breakfast, luncg=h, dinner within
    given number of calorie for the whole day.

    Return the response using markdown.

    """
    ##if the button is clicked
    input_diet = st.text_area(" Input the list of items that you have at home and get diet plan! OR \
                              Input how much calorie you want to intake perday?:")
    submit1 = st.button("Plan my Diet!")
    if submit1:
        response = get_response_diet(input_prompt_diet, input_diet)
        st.subheader("Diet AI: ")
        st.write(response)
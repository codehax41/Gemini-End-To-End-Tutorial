#Import Library
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi


#Load the API key
load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


#Prepraring the Prompt for the Summarizer
prompt = """
You are an expert youtube video summarizer. Your task involves condesing the transcript text of a video into a concise summary
comparing key points within a limit of 600 words.

Also provide below information:
- Title of the video
- Author of the video
- Summarize the provided text and extract action items, presenting them as bullet points
"""

#Bring the trascript data from YT api
def extract_trascript(url):
    video_dt = url.split("=")[1]
    trascript_data = YouTubeTranscriptApi.get_transcript(video_dt)

    #Append the transcript data
    transcript = ""
    for i in trascript_data:
        transcript += " " + i["text"]

    return transcript

#Get response from the Gemini Model
def get_response(trascript, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([trascript, prompt])
    return response.text

#Creating Streamlit App
#st.set_page_config(page_title="Youtube Transcriptor")
st.image("Youtube Transcriptor/logo.jpg", width=100)
st.title("Youtube Transcript Summarizer App")
youtube_url = st.text_input("Enter the Youtube Video link!")

#Bring the thubnail of the video
if youtube_url:
    video_id = youtube_url.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

#Create a button
button = st.button("Get Summary!")    
if button:
    trascript_text = extract_trascript(youtube_url)

    if trascript_text:
        summary = get_response(trascript_text, prompt)
        st.markdown("## Detailed Notes!")
        st.write(summary)
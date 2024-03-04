#Import all the Libraries
import streamlit as st
import os
import sqlite3
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

#Configure the Google API
load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Lets load the Gemini model and preprare the response
def get_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

#Function to retrive query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

#Prepare the prompt:
prompt = [
    """
    You are an expert SQL Specialist, Your job is to conver english or say natural language to SQL Query.
    It has columns like "Title", "AvailableGlobally", "ReleaseDate", "HoursViewed".
    So when preparing sql query consider the column name mentioned above.
    Do not add extra information except what is asked!
    When giving output make sure to use user frendly aliases.
    Table Name: movies.

    Example 1: How many entries of record present in db?
    Answer: SELECT count(*) from movies;
    Example 2: Which top 10 titles were released during a specific month May?
    Answer: SELECT Title, ReleaseDate from moviews where strftime('%m', ReleaseDate) = 5 order by HoursViewed dec limit 10;

    Also the sql code should not have ``` in the beginning or end and sql word on the o/p.
"""
]


#Initialize the app
#st.set_page_config(page_title="Data Analysis Bot!")
st.image("SQL AI/logo.png", width=100)
st.header("Data Analysis Bot: App to Retrive SQL/Tabular Data!")

#Text area & Button
question = st.text_input("Input:", key="input")
submit = st.button("Ask the question!")

#If the button is clicked
if submit:
    response = get_response(question, prompt)
    st.write("The Generated SQL query is")
    st.code(response)

    #Execute the generated SQL Query
    result = read_sql_query(response, "movies.db")
    st.subheader("The Response is:")

    #Display the result
    if result:
        st.write(pd.DataFrame(result))
        #st.write(result)


#File uploader for CSV
st.sidebar.header("Upload CSV file")
upload_file = st.sidebar.file_uploader("Choose a CSV File", type=["csv"])

#If CSV file is uploaded
if upload_file:
    #Read the CSV into a DataFrame
    df = pd.read_csv(upload_file, header=0)
    st.sidebar.write(df.head())

    #save the data to SQLite database
    conn = sqlite3.connect("movies.db")
    df.to_sql("MOVIES", conn, if_exists="replace", index=False)
    st.sidebar.success("CSV FIle successfully stored in SQLite Database!") 
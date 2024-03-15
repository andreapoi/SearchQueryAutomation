import streamlit as st
import pandas as pd
from openai import OpenAI

#Set page layout and title
st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide")
st.title("Search Query Automation App")

#Get keys
chat_key = st.secrets['ChatGPT_key']['token']
st.write(chat_key)


#Upload files
uploaded_file_keywords = st.file_uploader("Upload your Keyword file", type=['csv'], key = 'keywords')
uploaded_file_search_terms = st.file_uploader("Upload your Search terms file", type = ['csv'], key = 'search terms')

#Set campaign and Ad_group variables
campaign = st.text_input("Please enter a campaign:", key = 'campaign')
ad_group = st.text_input("Please enter an ad_group:", key = 'ad_group')

#Only proceed if user has entered all the required fields
if uploaded_file_keywords is not None and uploaded_file_search_terms is not None and campaign != "" and ad_group != "":

    #Search Term Processing
    #Assuming the CSV has headers, otherwise use header = None
  
    search_term_data = pd.read_csv(uploaded_file_search_terms)
    search_term_data = search_term_data.sort_values(by='Cost', ascending = False)
    search_term_data['Cost'] = search_term_data['Cost'].astype(str)
    search_term_data['Concatenated'] = search_term_data['Search term'] + ' ' + search_term_data['Cost']

    #Get list of search terms for column
    search_term_col = search_term_data['Concatenated']
    
    #Combine Search terms into one string
    search_terms = ", ".join(search_term_col)

    #Keyword Processing
    #Assuming the CSV has headers, otherwise use header = None
  
    keyword_data = pd.read_csv(uploaded_file_keywords)

    #Get list of search terms for column
    keyword_col = keyword_data['Keyword']
    
    #Combine Search terms into one string
    keywords = ", ".join(keyword_col)

    st.write(keywords)
    st.write(search_terms)

    prompt = ""
    





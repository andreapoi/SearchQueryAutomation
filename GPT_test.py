import streamlit as st
import pandas as pd

st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide")

uploaded_file_keywords = st.file_uploader("Upload your input CSV file", type=['csv'], key = 'keywords')

uploaded_file_search_terms = st.file_uploader("Upload your input CSV file", type = ['csv'], key = 'search terms')

                   
if uploaded_file_keywords & uploaded_file_search_terms is not None:
    
    # Assuming the CSV has headers, otherwise use header=None
    data = pd.read_csv(uploaded_file)

    #Display
    st.write(data)

    #Get list of search terms for column
    search_term_col = data['Search term']
    
    #Combine Search terms into one string
    search_terms = ", ".join(search_term_col)
    
    #Display Search Terms
    st.write(search_terms)





import streamlit as st
import pandas as pd

st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide")

uploaded_file = st.file_uploader("Upload your input CSV file", type=['csv'])
                   
if uploaded_file is not None:
    # Assuming the CSV has headers, otherwise use header=None
    data = pd.read_csv(uploaded_file)
    st.write(data)

search_term_col = data['Search term']

search_terms = ", ".join(search_term_col)

st.write(search_terms)





import streamlit as st
import pandas as pd

data = st.file_uploader("Upload your input CSV file", type=['csv'])

st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide")
                   
if data is not None:
    # Assuming the CSV has headers, otherwise use header=None
    data = pd.read_csv(uploaded_file)
    st.write(data)




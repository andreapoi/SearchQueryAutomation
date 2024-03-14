import streamlit as st
import pandas as pd

st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide")

uploaded_file = st.file_uploader("Upload your input CSV file", type=['csv'])
                   
if data is not None:
    # Assuming the CSV has headers, otherwise use header=None
    data = pd.read_csv(uploaded_file)
    st.write(data)




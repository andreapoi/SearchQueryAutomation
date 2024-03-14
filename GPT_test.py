import streamlit as st
import pandas as pd

data = st.file_uploader("Please upload Search Query Terms", type = [csv])

st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide"
                   
if 'data' not in st.session_state:
    # Assuming the CSV has headers, otherwise use header=None
    data = pd.read_csv(uploaded_file)
    st.write(data)




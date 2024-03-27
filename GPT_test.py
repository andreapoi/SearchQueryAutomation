import streamlit as st
import pandas as pd
from openai import OpenAI

correct_password = 'Chatforthewin'

def password_protection():
  if 'authenticated' not in st.session_state:
      st.session_state.authenticated = False
      
  if not st.session_state.authenticated:
      password = st.text_input("Enter Password:", type="password")
      
      if st.button("Login"):
          if password == correct_password:
              st.session_state.authenticated = True
              main_dashboard()
          else:
              st.error("Incorrect Password. Please try again or contact the administrator.")
  else:
      main_dashboard()

#Set page layout and title
st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide")

#Get keys
chat_key = st.secrets['ChatGPT_key']['token']

def main_dashboard():
  st.markdown(f"<h1 style='text-align: center;'>Search Query Report Automation</h1>", unsafe_allow_html=True)

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
    
        
        client = OpenAI(api_key = chat_key)
    
        # Define system and user messages for a multi-turn conversation
        messages = [
            {"role": "system", "content": "You are a digital marketer analyzing a search terms report from Google Ads. You need to identify terms that could be possible additions to a given campiagn and ad group combination for a solar client called Axia solar. You should disregard any mentions of competitors (i.e. Tesla) as well as things that would be bad for business like 'free' or questions. Use your previous knowledge of Search Query reporting in this task."},
            {"role": "user", "content": f"The campaign is titled: {campaign} and the ad group is: {ad_group}. Keep in mind that in each campaign there are usually references to 1. Type - like Brand (B) or Non - Brand (NB) 2. Campaign strategy - generic or type of term 3. Location - like CA. The location means that words specific to that area should defintley be considered but terms are not limited to things referencing that area. The ad group usually gets a bit more specific and constitutes a grouping of word (ie cost, gereral solar, house)."},
            {"role": "user", "content": f"The current keywords in this group are: {keywords}. Added keywords should be pretty similar to these words but not limited to them. Use this list as a reference as to what added keywords should look like."},
            {"role": "user", "content": f"Please review the following search terms to identify any that may be relevant or irrelevant for this group. The number next to each term is the cost associated with it in Google Ads. Higher costs means that term has been referenced a number of times. Be pretty selective about words that may get added.: {search_terms}"},
        ]

        # Call the API with the updated messages and model
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="ft:gpt-3.5-turbo-0125:personal:test-mod-1:977LvAaP",  # Replace with your fine-tuned model's name
        )

        # Retrieve the output
        output = chat_completion.choices[0].message.content

        # Display the prompt and output in the Streamlit app
        with st.expander("See Prompt"):
            st.write(messages)

        with st.expander("See Output from Chat GPT"):
            st.write(output)
    
if __name__ == '__main__':
    password_protection()

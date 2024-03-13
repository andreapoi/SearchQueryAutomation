import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import matplotlib.pyplot as plt
from joblib import load
from xgboost import XGBClassifier

st.set_page_config(page_title= f"SQR Dash",page_icon="🧑‍🚀",layout="wide")


def password_protection():
  if 'authenticated' not in st.session_state:
      st.session_state.authenticated = False
      
  if not st.session_state.authenticated:
      password = st.text_input("Enter Password:", type="password")
      
      if st.button("Login"):
          if password == "SQR":
              st.session_state.authenticated = True
              main_dashboard()
          else:
              st.error("Incorrect Password. Please try again or contact the administrator.")
  else:
        main_dashboard()

def get_top_ngrams(corpus, n=None, ngram_range=(1,1)):
    vec = CountVectorizer(stop_words='english', ngram_range=ngram_range).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]

def main_dashboard():

    st.markdown(f"<h1 style='text-align: center;'>Search Query Analysis</h1>", unsafe_allow_html=True)
    #Load Data
    raw_data = pd.read_csv("Search terms report.csv", skiprows=2)

    #Load the trained model
    xgb_classifier = load('SearchQueryModel1.joblib')
    
    #Change Data Types
    data = raw_data
    data['Impr.'] = data['Impr.'].str.replace(',','').astype(int)
    data['Interactions'] = data['Interactions'].str.replace(',','').astype(int)
    data['Clicks'] = data['Clicks'].str.replace(',','').astype(int)

    #Rename Impressions col
    data.rename(columns = {"Impr.":"Impressions"}, inplace = True)

    #Get unadded terms / Filter out totals
    Unadded_data = data[data['Added/Excluded'] != "Added"]
    Unadded_data = Unadded_data[~Unadded_data['Search term'].str.contains("Total:")]
  
   

    #Pre-process Search Terms
    tfidf_vectorizer = load('tfidf_vectorizer.joblib')
    X_tfidf = tfidf_vectorizer.transform(Unadded_data['Search term'])
  
    #individual_search_term = ["solar panel cost"]

    #X_individual = tfidf_vectorizer.transform(individual_search_term)

    # For class label prediction
    #prediction = xgb_classifier.predict(X_individual)

    # For probability of the positive class ("Added" class)
    #probability = xgb_classifier.predict_proba(X_individual)[:, 1] 

    #st.write("Search Term:", individual_search_term[0])
    #st.write("Prediction:", prediction[0])  # Adjust if you decode prediction to the original label
    #st.write("Probability of 'Added':", probability[0])


    #Make Predictions
    predictions = xgb_classifier.predict(X_tfidf)  

    #Get Probabilities
    probabilities = xgb_classifier.predict_proba(X_tfidf)

    # Assuming the positive class ("Added") is the second column
    positive_probabilities = probabilities[:, 0]
    
    #Output dataframe
    # Create a DataFrame with the search terms, predictions, and probabilities
    results_df = pd.DataFrame({
        'Search Term': Unadded_data['Search term'],
        'Prediction': predictions,
        'Probability': positive_probabilities
    })

    results_df['Prediction'] = results_df['Prediction'].replace({0: 'Possible Add', 1: 'None'})

    results_df = results_df.drop_duplicates(keep='last')

     # N-Gram Analysis
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("See Top Phrases & Filter by Length")
        col3, col4 = st.columns(2)
        with col3:
            ngram_start = st.number_input('N-Gram Start', min_value=1, max_value=5, value=3)
        with col4:
            ngram_end = st.number_input('N-Gram End', min_value=1, max_value=7, value=5)
        top_ngrams = get_top_ngrams(Unadded_data['Search term'], n=10, ngram_range=(ngram_start, ngram_end))
        fig, ax = plt.subplots()
        ax.barh([x[0] for x in top_ngrams], [x[1] for x in top_ngrams])
        ax.set_xlabel('Frequency')
        ax.set_title('Top N-Grams from Search Terms')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Sort and Filter on Metrics")
        col6, col7 = st.columns(2)
        with col6:
          metric = st.selectbox("Select a metric to sort on:", ("Conversions", "Clicks", "Impressions","Cost"))
        with col7:
          quanity = st.number_input('Show top _ Rows:', value = 20)
      
        top_click = Unadded_data.nlargest(quanity, metric)
        st.write(top_click)
  
    st.markdown(f"<h3 style='text-align: center;'>Added Terms Prediction</h3>", unsafe_allow_html=True)
    st.dataframe(results_df.sort_values(by="Probability", ascending=False), width = 1500)

if __name__ == '__main__':
    password_protection()

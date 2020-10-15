import streamlit as st

import pandas as pd
import numpy as np
import json
import nltk
import seaborn as sns
from IPython.core.display import display, HTML
sns.set()

# local library
from preproc import *

@st.cache
def load_speeches():
	with open('speeches.json',encoding='utf-8') as f:
		speeches = json.load(f)
		return speeches
		
@st.cache
def load_bow():
	bow = create_bow(speeches)
	return bow

def export_speeches():
        bow.to_csv('speeches.csv', index=True)

def import_speeches():
        speech = pd.read_csv('speeches.csv')
        return speech

#data_load_state = st.text('Loading data...')
#speeches = load_speeches()
#bow = load_bow()
speech = import_speeches()
#data_load_state.text('Loading data...done!')

def write():
    
    st.write("""
    # Individual Campaign Speeches
    """)


   # st.subheader('Speech library')
   # st.write(speech[["id","index","speaker","date","title"]])

#Filters to select speeches

    c_picker = st.selectbox('Candidate:', speech['speaker'].unique(), index=0)
    c_picker2 = st.selectbox('Speech:', speech['title'], index=0)

# YouTube embedded video

    videoresult = speech.loc[(speech['title'] == c_picker2), 'id'].iloc[0]
    st.video('https://youtu.be/'+str(videoresult))

# API Transcript readout

    selectspeech = speech.loc[(speech['title'] == c_picker2), 'speech'].iloc[0]
    st.write(speech['speech'])

# Sentiment Analysis

    salex_csv = 'salex_nrc.csv'
    nrc_cols = "nrc_negative nrc_positive nrc_anger nrc_anticipation nrc_disgust nrc_fear nrc_joy nrc_sadness nrc_surprise nrc_trust".split()
    emo = 'polarity'

    salex = pd.read_csv(salex_csv).set_index('term_str')
    salex.columns = [col.replace('nrc_','') for col in salex.columns]
    salex['polarity'] = salex.positive - salex.negative

    emo_cols = "anger anticipation disgust fear joy sadness surprise trust polarity".split()

    TOKEN = tokenize(speech)
    TOKEN = TOKEN.join(salex, on='term_str', how='left')
    TOKEN[emo_cols] = TOKEN[emo_cols].fillna(0)

    TOKEN[emo_cols] = TOKEN[emo_cols].fillna(0)
    Sentiment = TOKEN.loc[speech['id']].copy()
    Sentiment[emo_cols].mean().sort_values().plot.barh()
    st.pyplot()
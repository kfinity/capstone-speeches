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
    # US Presidential Election Campaign Speeches

    ## The Data

    """)


    st.subheader('Speech library')
    st.write(speech[["id","index","speaker","date","title"]])

    c_picker = st.selectbox('Candidate:', speech['speaker'].unique(), index=0)

    bow2 = speech.copy()
    bow2['day'] = bow2['date'].str[:10]
    dates = bow2[bow2['speaker'] == c_picker].groupby(['day']).agg({'speech': 'count'}).reset_index()

    st.bar_chart(dates)
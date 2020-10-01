# Run this with "streamlit run [filename]"

import streamlit as st

import pandas as pd
import numpy as np

# local library
from preproc import *

@st.cache
def load_speeches():
	with open('speeches.json') as f:
		speeches = json.load(f)
		return speeches
		
@st.cache
def load_bow():
	bow = create_bow(speeches)
	return bow

data_load_state = st.text('Loading data...')
speeches = load_speeches()
bow = load_bow()
data_load_state.text('Loading data...done!')
    
st.write("""
# capstone-speeches
""")


st.subheader('Speech library')
st.write(bow[["index","speaker","date","title","transcript_type"]])

candidates = ['trump','biden','pence','harris']

c_picker = st.selectbox('Candidate:', candidates, index=0)

bow2 = bow.copy()
bow2['day'] = bow2['date'].str[:10]
dates = bow2[bow2['speaker'] == c_picker].groupby(['day']).agg({'speech': 'count'}).reset_index()

st.bar_chart(dates)

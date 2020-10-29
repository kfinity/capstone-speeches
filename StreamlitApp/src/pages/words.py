import streamlit as st

import pandas as pd
import numpy as np

import streamlit.components.v1 as components

from IPython.core.display import display, HTML

def import_speeches():
        speech = pd.read_csv('data/speeches.csv')
        return speech

#data_load_state = st.text('Loading data...')
#speeches = load_speeches()
#bow = load_bow()
speech = import_speeches()
#data_load_state.text('Loading data...done!')

def write():
    
    st.write("""
    # US Presidential Election Campaign Speeches

    ## The Words

    Exploring the words of the speeches, using TF-IDF and other tools.

    """)

    st.write("## TF-IDF")

    tfidf_speaker = pd.read_csv('data/tfidf_speaker.csv')
    top10 = pd.DataFrame(tfidf_speaker.sort_values('biden', ascending=False).head(10)[['index']].values)
    top10.columns = ['biden']
    top10['trump'] = tfidf_speaker.sort_values('trump', ascending=False).head(10)[['index']].values
    top10['harris'] = tfidf_speaker.sort_values('harris', ascending=False).head(10)[['index']].values
    top10['pence'] = tfidf_speaker.sort_values('pence', ascending=False).head(10)[['index']].values
    
    st.write(top10)

    st.write("## PCA")
    with open('data/pca1.html','r') as pca1:
        pca1_str = pca1.read()
        components.html(pca1_str, height=500)
    
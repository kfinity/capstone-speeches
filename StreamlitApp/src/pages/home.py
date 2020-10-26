import streamlit as st
import SessionState
import pathlib
import utils.display as udisp
import pandas as pd
import numpy as np
import json
import nltk
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.core.display import display, HTML
sns.set()
from PIL import Image

def import_speeches():
        speech = pd.read_csv('speeches.csv') # calculated in top_tfidf_with_ngrams.ipynb
        return speech

#data_load_state = st.text('Loading data...')
#speeches = load_speeches()
#bow = load_bow()
speech = import_speeches()
#data_load_state.text('Loading data...done!')


app_state = st.experimental_get_query_params()
#app_state = {k: v[0] if isinstance(v, list) else v for k, v in app_state.items()}



def write():
    image = Image.open('TitleBanner.jpg')
    st.image(image, caption='The 2020 US Presidential Election Campaign Speeches', use_column_width=True)

    st.markdown("""
        Political speeches during campaign season are known for being formulaic and repetitive. What could we learn by looking for patterns in the way the speeches change over the course of the campaign? Can we track a candidate's ideological trajectory, identify their main topics, or characterize their speaking style? How do the speeches of today's candidates compare with those from prior elections? For this project, we are preparing to look at the speeches of the 2020 U.S. Presidential election candidates. 

        To start, let's look at individual campaign speeches.""")

    st.markdown("# Explore individual speeches ")

#Filters to select speeches

    
    default_speaker = app_state["p"][0] if "p" in app_state else 'trump'
    if default_speaker not in speech['speaker'].unique():
        default_speaker_idx = 0
    else:
        default_speaker_idx = speech['speaker'].unique().tolist().index(default_speaker)

    c_picker = st.selectbox('Candidate:', speech['speaker'].unique()) #, index=default_speaker_idx)

    #st.markdown("speaker: " + default_speaker + " idx:" + str(default_speaker_idx))

    # filtered speech list for this speaker
    fspeech = speech.loc[speech['speaker']==c_picker,:].reset_index(drop=True)

    default_speech_id = app_state["s"][0] if "s" in app_state else 'none'
    if default_speech_id not in fspeech['id'].unique():
        default_speech = 0
    else:
        default_speech = fspeech.index[fspeech['id']==default_speech_id].tolist()[0]

    c_picker2 = st.selectbox('Speech:', fspeech['title']) #, index=default_speech)

    # YouTube embedded video

    videoresult = fspeech.loc[(fspeech['title'] == c_picker2), 'id'].iloc[0]
    st.video('https://youtu.be/'+str(videoresult))

    # 3 most similar

    sim = pd.read_csv('speech_similarity.csv') # calculated in top_tfidf_with_ngrams.ipynb
    # for just the current speech, locate the top 3 
    sim3 = sim.set_index('id').loc[videoresult].sort_values(ascending=False)[1:4].to_dict().items()
    # print them
    st.markdown("## 3 most similar speeches")
    for (vid,score) in sim3:
        title = speech.loc[(speech['id'] == vid), 'title'].values
        if len(title) > 0:
            st.markdown("**{}**".format(title[0]))
            st.markdown("({:4.3f} similarity) [Watch it on YouTube](https://youtu.be/{})".format(score, vid))

    # API Transcript readout

    selectspeech = fspeech.loc[(fspeech['title'] == c_picker2), 'speech'].iloc[0]
    st.write("""
    ## Speech Transcript
    """)
    st.text_area("",value=selectspeech, height=200)

    # Sentiment Analysis

    st.write("""
    ## Sentiment Analysis
    """)
    # file generated in create_sentiment.ipynb
    Sentiment = pd.read_csv('sentiment.csv').set_index('id').loc[videoresult,:]\
        .to_frame()
    Sentiment.columns = ["value"]
    fig, ax = plt.subplots()
    Sentiment.sort_values('value').plot.barh(ax=ax)
    ax.get_legend().remove()
    st.pyplot(fig)    




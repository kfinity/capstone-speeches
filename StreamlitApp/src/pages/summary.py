import streamlit as st

import pandas as pd
import numpy as np
import json
import seaborn as sns
from IPython.core.display import display, HTML
sns.set()
import altair as alt

def import_speeches():
        speech = pd.read_csv('data/speeches.csv')
        return speech
    
def import_topics():
        topics = pd.read_csv('data/topic_modeling.csv')
        return topics

#data_load_state = st.text('Loading data...')
#speeches = load_speeches()
#bow = load_bow()
speech = import_speeches()
topics = import_topics()
#data_load_state.text('Loading data...done!')

def write():
    
    st.write("""
    # US Presidential Election Campaign Speeches
    
    ## Topic Modeling
    
    Using Latent Dirichlet Allocation (LDA), we are able to model the topics
    that candidates discuss by showing the most representative words for each 
    topic, and show what proportion of their time each candidate dedicated to 
    certain topics.
    """)

    tops = alt.Chart(topics).transform_fold(['trump', 'biden', 'pence', 'harris'],
      as_=['speaker', 'value']).mark_bar().encode(
      x='value:Q',
      y=alt.Y('topterms:N', sort='-x'),
      color='speaker:N',
      order=alt.Order(
      'speaker:N',
      sort='ascending')
    )
          
    st.altair_chart(tops, use_container_width=True)
        
    st.write("""
    We can see that Biden and Harris bring a very consistent message, with 
    broad messaging focused on the nation as a whole, with health care and jobs
    as the top priorities. They also bring more attention to focused topics 
    such as the COVID-19 pandemic. In contrast, Trump focuses on what he sees 
    as his strengths, with major topics surrounding jobs, dollars, and China. 
    Pence is mainly delegated to one topic that seems to be purely about Trump
    vs. Biden, which makes sense since the majority of his speeches are his 
    introducing Trump at rallies, setting the stage for the stakes of the election.
    
    """)
    
    

    st.subheader('Speech library')
    st.write(speech[["id","speaker","date","title","transcript_type"]])

#    c_picker = st.selectbox('Candidate:', speech['speaker'].unique(), index=0)

#    bow2 = speech.copy()
#    bow2['day'] = bow2['date'].str[:10]
#    dates = bow2[bow2['speaker'] == c_picker].groupby(['day']).agg({'speech': 'count'}).reset_index()

#    st.bar_chart(dates)
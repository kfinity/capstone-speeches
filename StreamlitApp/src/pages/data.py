import streamlit as st

import pandas as pd
import numpy as np
import json
import seaborn as sns
from IPython.core.display import display, HTML
sns.set()
from PIL import Image
import base64


def import_speeches():
        speech = pd.read_csv('data/speeches.csv')
        return speech

#data_load_state = st.text('Loading data...')
#speeches = load_speeches()
#bow = load_bow()
speech = import_speeches()
#data_load_state.text('Loading data...done!')

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  json
    out: href string
        """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download speeches data as csv</a>'
    return href
        
st.markdown(get_table_download_link(speech), unsafe_allow_html=True)

def write():
    
    st.write("""
    # US Presidential Election Campaign Speeches

    ## The Data
    
    In our initial assessment of data sources, we realized that there were not 
    any data sources that had aggregated campaign speeches into a single 
    repository. Some sites had posted transcripts of extremely high profile 
    speeches, with supplementary analysis, but nobody was posting transcripts 
    for the smaller, daily stops of the campaign trail. We needed access to 
    more data in order to conduct a thorough exploration of the data.
    
    To get around this, we decided to create a scraper that would capture 
    speeches, interviews, and debates using YouTube's API. In one API call, we 
    would search for speeches made by any candidates on that specific day that 
    were over 20 minutes (in order to avoid search results such as clips or 
    news stories). In the second API call, we would then write the automated 
    video captions and any associated metadata into a JSON file. By having all 
    of our speeches coming from the same site, we had the advantage of 
    everything being formatted in a similar manner.
    
    As these are video captions and not true transcripts, the structure is a 
    bit unusual. Each caption appears as its own line (as it would in the 
    video), with an associated start time and duration, representing when that 
    caption appeared in the video. See examples below.

    """)

    image1 = Image.open('StreamlitApp/json_sample.png')
    image2 = Image.open('StreamlitApp/caption.png')

    st.image(image1, caption='Sample of captions format')
    st.image(image2, caption='Captions as they appear in videos',
             use_column_width=True)
    
    
    st.write("""
    ### Metadata
    
    The YouTube JSON format includes a variety of metadata, including:
        
    - title
    - channel
    - description
    - publishedAt (date)
    - tags
    - commnetcount
    - likecount
    - dislikecount
    - viewcount

    The raw JSON file, as well as a custom preprocessing library, and all scripts
    used in our analysis, can be found at the github linked in the left toolbar.

    """)


    st.subheader('Speech library')
    st.write(speech[["id","speaker","date","title","transcript_type"]])

#    c_picker = st.selectbox('Candidate:', speech['speaker'].unique(), index=0)

#    bow2 = speech.copy()
#    bow2['day'] = bow2['date'].str[:10]
#    dates = bow2[bow2['speaker'] == c_picker].groupby(['day']).agg({'speech': 'count'}).reset_index()

#    st.bar_chart(dates)
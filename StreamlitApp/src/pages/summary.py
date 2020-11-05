import streamlit as st

import pandas as pd
import numpy as np
import json
import seaborn as sns
from IPython.core.display import display, HTML
sns.set()
import altair as alt
import streamlit.components.v1 as components
import base64

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
    
    In a year as unpredictable as 2020, one of the key questions we were asking was:
    "What will the candidates be focusing on? What do they need to say in order to 
    win the most voters?" The COVID-19 pandemic comes to mind, along with the standard 
    issues of the economy, the environment, racial injustice and law enforcement, to
    name a few.
    
    Looking more closely, we can see exactly how Joe Biden and Donald Trump try to cater 
    to their strengths, as well as their respective bases, in choosing what issues to
    focus on. In addition, we can clearly see the role of the nominee for Vice President. 
    They are not their to discuss isses or policy. Instead, the VP candidate largely exists
    to support and talk up the presidential nominee.
    
    Using Latent Dirichlet Allocation (LDA), we are able to model the topics
    that candidates discuss by showing the most representative words for each 
    topic, and show how much time each candidate dedicated to each topic.
    """)
    """
# Removed in favor of pyLDAvis topic modeling visualization

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
    """

    st.write("""
    ### Joe Biden Topics
    """)
        
    HtmlFile = open("data/biden_viz.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    print(source_code)
    components.html(source_code, height=800, width=1200, scrolling=True)
    
    st.write("""
    ### Donald Trump Topics
    """)
        
    HtmlFile = open("data/trump_viz.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    print(source_code)
    components.html(source_code, height=800, width=1200, scrolling=True)
    
    st.write("""
    Looking at the presidential candidates, we can take away a few interesting 
    bits of information. Our visualization includes principal component analysis 
    (PCA) to estimate how similar topics are to each other. The clearest observation 
    is that the topics are varied. This may just seem like an obvious fact that 
    we should take for granted, but it is important to point out here before we 
    compare against the VP candidates.
    
    The other large takeaway is the comparison of topics between Biden and Trump.
    One of Biden's key issues was the COVID-19 pandemic, and we can see that reflected
    in Biden's 3rd largest topic, (key indicators include "virus", "school", and 
    "mask"). Other key issues of the democratic platform are also apparent such as 
    climate change and the energy sector (topic #6) or the Supreme Court (topic #7).
    Biden's second most popular topic seems to just be about attacking Trump.
    But most surprisingly, Biden's #1 topic seems to be the economy. 
    
    This is especially interesting considering that the economy is supposed to be
    Donald Trump's big selling point. Trump's topics are not quite as focused as Biden's,
    although some interesting results do emerge, such as one that seems to be focused
    on preserving controversial American monuments (topic #7) or media coverage 
    of the election (topic #5). For the most part though, while Trump's topics do 
    include mentions of his strengths, including jobs, China, and police, they all 
    seem to be lumped together with not a lot to discern them.
    """)
    
    st.write("""
    ### Kamala Harris Topics
    """)
        
    HtmlFile = open("data/harris_viz.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    print(source_code)
    components.html(source_code, height=800, width=1200, scrolling=True)
    
    st.write("""
    ### Mike Pence Topics
    """)
        
    HtmlFile = open("data/pence_viz.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    print(source_code)
    components.html(source_code, height=800, width=1200, scrolling=True)
    
    st.write("""
    If the role of Presidential candidate speeches is to cater to each candidate's
    strengths, then the role of Vice Presidential nominee speeches is to talk them up.
    
    We can clearly see in both Harris' and Pence's topics that they stay focused
    on just a few key issues. With Harris, her top 2 topics loom large obove all others
    and they seem to be just about Biden and then the election in general. Pence, on 
    the other hand, seems to talk about different subjects, but PCA indicates that all
    of these topics are extremely similar. His first, second, and fourth topics all 
    overlap each other, and they all focus Donald Trump vs. Joe Biden.
    """)
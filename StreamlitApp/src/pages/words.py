import streamlit as st

import pandas as pd
import numpy as np

import streamlit.components.v1 as components
from PIL import Image
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

    st.write("""## PCA

Principal Components Analysis organizes the data along the dimensions of highest variance. Often, this reveals underlying patterns in the data.

For this visualization, we look at the first 2 principal components for the unigram TF-IDF of the speeches. Two notable clusters emerge: Trump rallies in the lower left, and Pence speeches in the lower right. Tight clusters indicate that the speeches have low lexical variation - they have a very consistent style, reusing the same words and phrases, which makes them easily characterized.

By contrast, the Biden and Harris speeches have a wide spread, as do the Trump interviews and public appearances. This represents a more complex and diverse pattern of word usage.
    """)

    with open('data/pca1.html','r') as pca1:
        pca1_str = pca1.read()
        components.html(pca1_str, height=500)

    st.write("""## HCA dendrogram

Here we evaluate the similarity of the speeches using Hierarchical Cluster Analysis, which maps the speeches into a "family tree" where similar speeches are closely related. We use cosine similarity as the metric, and select the 4 highest-level clusters.
""")

    dendrogram = Image.open('data/dendrogram.png')
    st.image(dendrogram, use_column_width=True)


    st.write("""### Characterizing the HCA groups

Although their methods are different, PCA and HCA produce similar clusters of speeches. Here, we color the PCA plot using the 4 top clusters from the HCA grouping.
    """)

    with open('data/pca1_groups.html','r') as pca1g:
        pca1g_str = pca1g.read()
        components.html(pca1g_str, height=500)
    
    st.write("""This sheds some light on the broad cluster of speeches in the top center. When we look at the individual speeches, the yellow speeches (group 3) are mostly interviews, involving dialog and a more conversational register.

The purple speeches (group 1) are mostly Biden speeches, along with some major public appearances for Trump (SOTU, RNC, 4th of July, 60 minutes). We suggest that this group represents a more formal, "presidential" style of speech.""")
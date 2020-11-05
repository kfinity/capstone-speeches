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
    st.write("""[Term frequency–inverse document frequency](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) is a popular way to weight the words in a text document (like a speech) by how often they occur. This helps highlight words which occur *uncommonly often* in a specific speech. """)

    st.write("""We can also aggregate the TFIDF scores by speaker to look at common words each speaker uses.""")

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

    st.write("""The PCA graph also lends credence to the theory presented in the "Summary" tab about the different roles
of the VP candidates. Donald Trump and Mike Pence's speeches are clearly sectioned off. Kamala Harris' speeches,
on the other hand, do have some overlap with Biden speeches, and even Trump speeches. For the most part though,
they do seem to be concentrated in the positive side of principal component 0, the same side where Mike Pence's speeches are located.""")

    st.write("""### PCA Loadings

The *loadings* for the principal components show us how much each term contributes to the vector. So we can look at the top words associated with different directions in the PCA plot.""")

    loadings = pd.read_csv('data/loadings.csv')
    pc5 = pd.DataFrame(loadings.sort_values('0').tail(5)['term'])
    pc5.columns=['Right (PC0 positive)']
    pc5['Left (PC0 negative)'] = loadings.sort_values('0').head(5)['term'].values
    pc5['Up (PC1 positive)'] = loadings.sort_values('1').tail(5)['term'].values
    pc5['Down (PC1 negative)'] = loadings.sort_values('1').head(5)['term'].values
    pc5 = pc5.T
    pc5.columns = ['#1','#2','#3','#4','#5']
    st.write(pc5)

    st.write("""We can also look at the top loaded words for each quadrant - the lower left (Trump rallies), lower right (Pence speeches), upper left, and upper right.""")

    top10 = pd.DataFrame(loadings.sort_values('trump_rally', ascending=False).head(10)[['term']].values)
    top10.columns = ['Lower left']
    top10['Lower right'] = loadings.sort_values('pence', ascending=False).head(10)[['term']].values
    top10['Upper left'] = loadings.sort_values('interviews', ascending=False).head(10)[['term']].values
    top10['Upper right'] = loadings.sort_values('formal', ascending=False).head(10)[['term']].values
    st.write(top10)

    st.write("""Based on these loadings and the speech contexts, we theorize a gloss for principal component 0 as "conversational" to "formal" (from left to right), and a gloss for PC1 of "extemporanous" to "rehearsed" (top to bottom).""")

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



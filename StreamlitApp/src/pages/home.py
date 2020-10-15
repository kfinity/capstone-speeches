import pathlib
import utils.display as udisp

import streamlit as st
from PIL import Image

def write():
    udisp.title_awesome("2020 US Presidential Election Campaign Speeches")

    image = Image.open('Candidates.png')
    st.image(image, caption='2020 US Presidential Election Candidates', use_column_width=True)

    st.subheader('"Words are, of course, the most powerful drug used by mankind."')
    st.markdown("<h3 style='text-align: right; color: black;'>-Rudyard Kipling</h3>", unsafe_allow_html=True)




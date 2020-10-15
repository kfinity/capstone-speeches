import pathlib
import utils.display as udisp

import streamlit as st

def write():
    udisp.title_awesome("About the Project")
    st.text_area("Political speeches during campaign season are known for being formulaic and repetitive. What could we learn by looking for patterns in the way the speeches change over the course of the campaign? Can we track a candidate's ideological trajectory, identify their main topics, or characterize their speaking style? How do the speeches of today's candidates compare with those from prior elections? For this project, we are preparing to look at the speeches of the 2020 U.S. Presidential election candidates.")

    st.write("For more information contact:")
    st.write("Kevin Finity (kf2tg@virginia.edu)")
    st.write("Max McGaw (mm9tk@virginia.edu)")
    st.write("Ramit Garg (rkg4u@virginia.edu)")
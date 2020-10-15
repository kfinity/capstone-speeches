import base64
import importlib

import streamlit as st

def render_page(menupage):
    menupage.write()

def title_awesome(body: str):
    st.write(
        f"## {body} "
    )

def render_md(md_file_name):
    st.markdown(get_file_content_as_string(md_file_name))

def get_file_content_as_string(path):
    response = open(path, encoding="utf-8").read()
    return response

def show_code(file_name):
    return get_file_content_as_string(file_name)

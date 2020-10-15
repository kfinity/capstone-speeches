import streamlit as st

import utils.display as udisp

import src.pages.home
import src.pages.about
import src.pages.summary
import src.pages.details

MENU = {
    "Home" : src.pages.home,
    "Speeches Summary" : src.pages.summary,
    "Speeches Details" : src.pages.details,
    "About the Project" : src.pages.about
}

def main():
    st.sidebar.title("Menu Options")
    menu_selection = st.sidebar.radio("Choose your option...", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Loading {menu_selection} ..."):
        udisp.render_page(menu)

    st.sidebar.info(
        "https://github.com/kfinity/capstone-speeches"
    )
    st.sidebar.info(
        "capstone-speeches/StreamlitApp"
    )

if __name__ == "__main__":
    main()
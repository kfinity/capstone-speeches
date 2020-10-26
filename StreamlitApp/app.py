import streamlit as st

import utils.display as udisp

import src.pages.home
#import src.pages.about
import src.pages.summary
import src.pages.details
import src.pages.data

MENU = {
    "Home" : src.pages.home,
    "Speeches Summary" : src.pages.summary,
    "Speeches Details" : src.pages.details,
    "Data" : src.pages.data
}

app_state = st.experimental_get_query_params()
app_state = {k: v[0] if isinstance(v, list) else v for k, v in app_state.items()}

def main():
    st.sidebar.title("Navigation")
    menu_selection = st.sidebar.radio("", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Loading {menu_selection} ..."):
        udisp.render_page(menu)

    st.sidebar.info(
        "https://github.com/kfinity/capstone-speeches"
    )
    st.sidebar.markdown(
        """
        ## About 

        This site is the result of a capstone project for UVA MSDS students:

        Kevin Finity (kf2tg@virginia.edu)

        Max McGaw (mm9tk@virginia.edu)

        Ramit Garg (rkg4u@virginia.edu)
        """
    )
    st.sidebar.image('uvads.jpg', use_column_width=True)

if __name__ == "__main__":
    main()
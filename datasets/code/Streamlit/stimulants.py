from load_init import local_css
import streamlit as st

st.set_page_config(
    page_title="NC Stimulants",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
)
local_css("datasets/code/Streamlit/style.css")
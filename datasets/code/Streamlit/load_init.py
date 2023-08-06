import streamlit as st
import webbrowser

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def button_as_page_link(url):
  webbrowser.open(url)

def create_sidebar():
    pages = {
      "Home": "https://ncdrugchecking.streamlit.app/",
      "NC Xylazine": "https://ncxylazine.streamlit.app/",
      "NC Overdoses": "https://ncoverdoses.streamlit.app/",
      "NC Stimulants": "https://ncstimulants.streamlit.app/",
      "NC Drug Market": "https://ncdrugmarket.streamlit.app/",
      "NC Psychedelics & Others": "https://ncpsychedelics.streamlit.app/",
      "Get Help": "https://www.streetsafe.supply/contact",
    }
    with st.sidebar:
    # map over the pages dict and return a button for each page
    # the button should have the page name as the label and the url as the param for the button_as_page_link function in the on_click param
     for page in pages:
        st.button(page, on_click=button_as_page_link, args=[pages[page]])
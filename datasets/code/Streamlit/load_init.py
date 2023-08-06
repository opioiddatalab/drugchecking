import streamlit as st
import webbrowser

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def button_as_page_link(url):
  webbrowser.open(url)

def create_sidebar():
    pages = {
      "Home": "https://nc-drugchecking-dashboards.streamlit.app/",
      "NC Xylazine": "https://ncxylazine.streamlit.app/",
      "NC Overdoses": "https://nc-overdoses.streamlit.app/",
      "NC Stimulants": "https://nc-stimulants.streamlit.app/",
      "NC Drug Market": "https://nc-drug-market.streamlit.app/",
      "NC Psychedelics & Others": "https://ncpsychedelics.streamlit.app/",
      "streetsafe.supply": "https://www.streetsafe.supply",
    }
    with st.sidebar:
    # map over the pages dict and return a button for each page
    # the button should have the page name as the label and the url as the param for the button_as_page_link function in the on_click param
     for page in pages:
        st.button(page, on_click=button_as_page_link, args=[pages[page]])
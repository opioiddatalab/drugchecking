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
        # create a markdown string that is an anchor tag with the url as the href value and the page name as the text
        # the anchor tag should open in a new tab
        html= "<a class='click-button' class='btn-simple' href="+pages[page]+" target='_blank'>"+page+"</a>"
        st.markdown(html, unsafe_allow_html=True)

def convert_df(df):
  return df.to_csv(index=False).encode('utf-8')

region_1 = [
     "Cherokee",
     "Graham",
     "Clay",
     "Macon",
     "Jackson",
     "Swain",
     "Haywood",
      "Madison",
      "Buncombe",
      "Henderson",
      "Transylvania",
      "Polk",
      "Rutherford",
      "McDowell",
      "Yancey",
      "Mitchell",
      "Avery",
      "Burke",
      "Caldwell"
].sort()
region_2 = [
   "Watauga",
    "Ashe",
    "Alleghany",
    "Wilkes",
    "Yadkin",
    "Surry",
    "Stokes",
    "Forsyth",
    "Davie",
    "Davidson",
    "Rockingham",
    "Guilford",
    "Randolph"
].sort()
region_3 = [
   "Cleveland",
    "Lincoln",
    "Gaston",
    "Mecklenburg",
    "Cabarrus",
    "Union",
    "Stanly",
    "Anson",
    "Alexander",
    "Iredell",
    "Rowan",
].sort()
region_4 = [
   "Caswell",
    "Person",
    "Granville",
    "Vance",
    "Warren",
    "Franklin",
    "Wake",
    "Durham",
    "Orange",
    "Chatham",
    "Alamance",
    "Wilson",
    "Johnston",
    "Nash"
].sort()
region_5 = [
   "Montgomery",
    "Moore",
    "Richmond",
    "Scotland",
    "Hoke",
    "Robeson",
    "Cumberland",
    "Bladen",
    "Sampson",
    "Pender",
    "Lee",
    "Harnett",
    "Cumberland",
    "New Hanover",
    "Brunswick"
].sort()
region_6 = [
   "Onslow",
    "Duplin",
    "Wayne",
    "Greene",
    "Lenoir",
    "Jones",
    "Pitt",
    "Beaufort",
    "Craven",
    "Pamlico",
    "Carteret",
    "Hyde",
    "Tyrrell",
    "Washington",
    "Martin",
    "Bertie",
    "Dare",
    "Currituck",
    "Camden",
    "Pasquotank",
    "Perquimans",
    "Chowan",
    "Gates",
    "Halifax",
    "Northampton",
    "Hertford"
].sort()

def add_county_group(county):
  county_group = {
     region_1: region_1,
     region_2: region_2,
     region_3: region_3,
      region_4: region_4,
      region_5: region_5,
      region_6: region_6
  }
  # map over the county_group dict and return the key if the county is in the value
  for key, value in county_group.items():
    if county in value:
      return key


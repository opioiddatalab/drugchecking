import streamlit as st


st.set_page_config(
    page_title="Street Drug Data Dashboards",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "https://www.streetsafe.supply/contact"
    }
)
from load_css import local_css
local_css("datasets/code/Streamlit/style.css")

st.write("# UNC Street Drug Analysis Lab")

st.markdown(
    """
    We are a public service of the University of North Carolina at Chapel Hill.
    **👈 Select a dashboard from the sidebar** to see our latest data!
    ### Want to learn more?
    - Check out [streetsafe.supply](https://www.streetsafe.supply/)
    - Jump to our [documentation](https://github.com/opioiddatalab/drugchecking/tree/main/datasets#readme)
    ### Notable media coverage
    - [NCDHHS Opioid and Substance Use Action Plan](https://www.ncdhhs.gov/about/department-initiatives/overdose-epidemic/north-carolinas-opioid-and-substance-use-action-plan)
    - [A High-Tech Strategy for Keeping Drug Users Safe](https://www.nytimes.com/2022/12/24/us/politics/fentanyl-drug-testing.html)
"""
)
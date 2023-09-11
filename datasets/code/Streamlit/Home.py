import streamlit as st
from PIL import Image
from load_init import display_funding

if 'sidebar_state_PERSIST' not in st.session_state:
    st.session_state.sidebar_state_PERSIST = 'auto'

st.set_page_config(
    page_title="Drugchecking Data Dashboards",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
)
from load_init import local_css, create_sidebar
local_css("datasets/code/Streamlit/style.css")


create_sidebar()
st.write("# UNC Street Drug Analysis Lab")

st.markdown(
    """
    We are a public service of the University of North Carolina at Chapel Hill.
    """
    """
    ⬅️ 👀 Select a dashboard from the sidebar to see our latest data!
    """)
with st.container():
    st.header("Resources from the UNC Street Drug Analysis Lab")
    tab1, tab2, tab3 = st.tabs(["Kit Info (English)", "Drug Testing Handout", "Drug Testing Poster"])
    with tab1:
      with open("datasets/code/Streamlit/downloadables/kit_info.pdf", "rb") as pdf_file:
          PDFbyte = pdf_file.read()

          st.download_button(label="Download pdf",
            data=PDFbyte,
            file_name="kit_info.pdf",
            mime='application/octet-stream')

      eng1 = Image.open('datasets/code/Streamlit/images/kit_info_eng.png')
      st.image(eng1)
    with tab2:
      with open("datasets/code/Streamlit/downloadables/drug_checking_handout.pdf", "rb") as pdf_file:
          PDFbyte = pdf_file.read()

          st.download_button(label="Download pdf",
            data=PDFbyte,
            file_name="drug_checking_handout.pdf",
            mime='application/octet-stream')

      h_1 = Image.open('datasets/code/Streamlit/images/drug_checking_1.png')
      st.image(h_1)
    with tab3:
      with open("datasets/code/Streamlit/downloadables/drug_checking_poster.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

        st.download_button(label="Download pdf",
          data=PDFbyte,
          file_name="drug_checking_poster.pdf",
          mime='application/octet-stream')

        h_2 = Image.open('datasets/code/Streamlit/images/drug_checking_2.png')
        st.image(h_2)
st.markdown("---")
st.markdown("""
    ### Want to learn more?
    - Check out [streetsafe.supply](https://www.streetsafe.supply/)
    - Jump to our [documentation](https://github.com/opioiddatalab/drugchecking/tree/main/datasets#readme)
    ### Notable media coverage
    - [NCDHHS Opioid and Substance Use Action Plan](https://www.ncdhhs.gov/about/department-initiatives/overdose-epidemic/north-carolinas-opioid-and-substance-use-action-plan)
    - [A High-Tech Strategy for Keeping Drug Users Safe](https://www.nytimes.com/2022/12/24/us/politics/fentanyl-drug-testing.html)
"""
)
st.markdown("---")
display_funding()
st.markdown("---")# commit 5f549b446e0766dbc23bce4a0d77ac3a92c514a7
# commit 76c42f6c0d48783856e2c18f16c19d253da675df
# commit c3c3e0e9fffdff28d80ddf78fada2522acf025c5
# commit e190bf6f482a33ccf9ac596355de4289a4604665
# commit b84c53e571260028ad36d13a349912afd9b5a6a3
# commit 9c2b94c191a15f178a281a1beff85eceecc6dd6f
# commit 218ac74bc55987c1ed5f23366dec9eeca5494b26

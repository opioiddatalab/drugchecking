import requests
import streamlit as st

# URL of the mp4 audio file
url = 'https://github.com/opioiddatalab/drugchecking/blob/main/datasets/code/Streamlit/audiotest/testaudio.m4a?raw=true'

# Use requests to download the audio file
response = requests.get(url)

# Title text
st.subheader("Testing Drug Explanation Audio Files")


col1, col2 = st.columns(2, gap="small")

with col1:
	st.markdown("Substance")
	
	
with col2:
	st.audio(response.content, format='audio/mp4')


# Play the audio file in the Streamlit app
# st.audio(response.content, format='audio/mp4')




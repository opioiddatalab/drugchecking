from load_css import local_css
local_css("datasets/code/Streamlit/style.css")
import streamlit as st
import pandas as pd
import numpy as np


# create a title for the app
st.title('Overdose Dashboard Title')

with st.container():
   st.write("This is inside the container")
   st.write("Naloxone doses in era of xylazine")
   st.write("Different ODs = Different Responses")
   st.write("Naloxone is Widely Available")


# with st.expander("Comparing Opioid and Stimulant Overdoses", False):
tab1, tab2 = st.tabs(["Opioid Overdoses", "Stiumlant Overdoses"])
with tab1:
    st.header("Opioid Overdoses")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- Item 1")
        st.markdown("- Item 2")
        st.markdown("- Item 3")
    with col2:
        st.video('https://www.youtube.com/watch?v=orzgwi7sxFM')

with tab2:
    st.header("Stimulant Overdoses")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- Item 1")
        st.markdown("- Item 2")
        st.markdown("- Item 3")
    with col2:
        st.video('https://youtu.be/MVs7ZfILCjE')


outerCol1, outerCol2 = st.columns(2)
with outerCol1:
        st.header("Opioid Overdose Resources")
        st.write("here's a bullted list of resources")
        st.markdown("- Obtaining Naloxone - ordering naloxone in NC, Remedy Alliance FTP, NEXT Distro")
        st.markdown("- OD Reversal Training - signs, work in nlx doses in era of xyl concept")
        st.markdown("- Types of OD - opioids (in stims), stimulant OD (acute vs multi day), benzos (esp potent \"dark web\" variety)")

with outerCol2:
        st.header("Stimulant Overdose Resources")
        st.write("here's a bullted list of resources")

body = "this is a container for the data"

with st.container():
    st.subheader(body, anchor="data", help=None)
    st.write("Information about Overdoses in general")
   
    col1, col2, col3 = st.columns(3)
    col1.metric("Pill/Powder Reported ODs w/ our Drug Checking", "70% of samples", "-1", "normal", help="this is a help string")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    st.write("comparing opioid and stimulant overdoses in a bar chart")
    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

    st.bar_chart(chart_data)


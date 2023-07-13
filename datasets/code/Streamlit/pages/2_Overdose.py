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
        st.header("How to Get Naloxone in NC")
        st.write("Naloxone is available under the statewide standing order through participating pharmacies. It is up to each individual pharmacy to decide whether to dispense naloxone under the statewide standing order or under a separate standing order. You can contact your local pharmacy to determine whether it is currently dispensing naloxone under a standing order.")
        st.write("If you are not able to obtain naloxone through a standing order at a pharmacy, you have other options to obtain naloxone. You may seek a prescription for naloxone from a health care provider. You may also get naloxone at some local health departments or syringe exchange programs. See links below to find a syringe exchange program in your area or a participating local health department.")
       


with outerCol2:
        st.markdown("<br/><br/>", unsafe_allow_html=True)
        st.markdown("- [NC Syringe Exchange Programs](https://www.ncdhhs.gov/divisions/public-health/north-carolina-safer-syringe-initiative/syringe-services-program-north-carolina)")
        st.markdown("- [Naloxone Saves - NC Pharmacy Locations](https://naloxonesaves.org/2019/02/13/n-c-pharmacies-that-offer-naloxone-under-a-standing-order/)")
        st.markdown("- [Syringe services programs that offer naloxone](https://naloxonesaves.org/naloxone-available-through-syringe-exchange-programs/)")
        st.markdown("- [NC health departments that offer naloxone](https://naloxonesaves.org/where-can-i-get-naloxone/north-carolina-health-departments-that-offer-naloxone/)")
        st.markdown("- [North Carolina pharmacies that offer naloxone](https://naloxonesaves.org/north-carolina-pharmacies-that-offer-naloxone/)")
        st.markdown("- Talk to your medical care provider about getting naloxone")

st.markdown("---")
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


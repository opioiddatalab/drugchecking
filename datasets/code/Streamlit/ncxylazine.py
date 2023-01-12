# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
from datetime import datetime


# Import public NC sample data and cache for Streamlit
@st.cache
def get_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_analysis_dataset.csv"
    return pd.read_csv(url)
df = get_data()
df = pd.DataFrame(df)
df.set_index('sampleid', inplace=True)

# Jitter locations where sample collected for mapping
sigma = 0.1
df['lat'] = df['lat'].apply(lambda x: np.random.normal(x, sigma))
df['lon'] = df['lon'].apply(lambda x: np.random.normal(x, sigma))

# Set date format
## Retains seconds unfortunately and NaT
df['date_collect'] = pd.to_datetime(df['date_collect'], format='%d%b%Y', errors = 'coerce')


# Limit to samples with any xylazine detected
dfxyl = df[['date_collect', 'lab_xylazine_any', 'county', 'sensations', 'sen_strength', 'color', 'texture','lat', 'lon']]
dfxyl = dfxyl[dfxyl.lab_xylazine_any==1]


# Streamlit
st.title("North Carolina Xylazine Reports")
st.markdown("[UNC Drug Analysis Lab](https://streetsafe.supply) results ")

                           
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)                           

st.subheader('Number of pickups by hour')
hist_values = np.histogram(df['date_collect'].dt.day, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

"""
st.header("Where has xylzine been detected?")
st.subheader("On a map")
st.markdown("The following map shows places where we have detected xylazine in street drugs.")
st.map(dfxyl.query("lab_xylazine_any")[["latitude", "longitude"]].dropna(how="any"))
"""
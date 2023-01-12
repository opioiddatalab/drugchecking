# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import datetime


# Import public NC sample data and cache for Streamlit
#@st.cache
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
df['date_collect'] = pd.to_datetime(df['date_collect'], infer_datetime_format=True)


# df['date_collect'] = datetime.datetime.strptime('date_collect', '%d%b%Y').strftime('%d%b%Y')

#df['date_collect'] = pd.to_datetime.date(df['date_collect'])

# Limit to samples with any xylazine detected
dfxyl = df[['date_collect', 'lab_xylazine_any', 'county', 'sensations', 'sen_strength', 'color', 'texture','lat', 'lon']]
dfxyl = dfxyl[dfxyl.lab_xylazine_any==1]

"""
# Streamlit
st.title("North Carolina Xylazine Reports")
st.markdown("[UNC Drug Analysis Lab](https://streetsafe.supply) results ")



                           
                           


st.header("Where has xylzine been detected?")
st.subheader("On a map")
st.markdown("The following map shows places where we have detected xylazine in street drugs.")
st.map(dfxyl.query("lab_xylazine_any")[["latitude", "longitude"]].dropna(how="any"))
"""
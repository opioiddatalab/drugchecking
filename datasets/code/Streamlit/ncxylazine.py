# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import streamlit as st
import numpy as np



# Import public NC sample data and cache for Streamlit
@st.cache
def get_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_analysis_dataset.csv"
    return pd.read_csv(url)
df = get_data()
df = pd.DataFrame(df)
df.set_index('sampleid', inplace=True)
#df = df['county'].replace(np.nan, "")
# Jitter locations where sample collected for mapping
sigma = 0.1
df['lat'] = df['lat'].apply(lambda x: np.random.normal(x, sigma))
df['lon'] = df['lon'].apply(lambda x: np.random.normal(x, sigma))

# Set date format
## Retains seconds unfortunately and NaT
df['date_collect'] = pd.to_datetime(df['date_collect'], format='%d%b%Y', errors = 'coerce')

# Limit to samples with any xylazine detected
dfxyl = df[['date_collect', 'lab_xylazine_any', 'lab_cocaine', 'lab_cocaine', 'lab_meth', 'lab_fentanyl', 'expect_fentanyl', 'county', 'sen_strength', 'sen_strength', 'color', 'texture','lat', 'lon']]
dfxyl = dfxyl[dfxyl.lab_xylazine_any==1]

# Count total number of samples processed
rows_count = len(df.index)

# Count number of xylazine samples
xyl_count = len(dfxyl.index)

# Count total number of counties with any samples
counties_sampled = df['county'].nunique() 

# Count number of counties samples
xyl_counties = dfxyl['county'].nunique() 

# Latest date xylazine was detected
latest = dfxyl['date_collect'].max()
latest = latest.strftime('%A %B %d, %Y')

# Sensation graph
#fent = dfxyl.loc['total', 'lab_fentanyl'] = dfxyl['lab_fentanyl'].sum()
#cocaine = dfxyl.loc['total', 'lab_cocaine'] = dfxyl['lab_cocaine'].sum()
#meth = dfxyl.loc['total', 'lab_meth'] = dfxyl['lab_meth'].sum()

df1 = df['column_name'].value_counts().rename_axis('unique_values').reset_index(name='counts')


# Latest xylazine reports by county
latestreport = dfxyl.groupby(by=["county"]).max()
latestreport["date_collect"] = latestreport["date_collect"].dt.strftime('%B %d, %Y')
mostrecent = latestreport[['date_collect']].copy()
mostrecent.rename(columns={'date_collect': 'Most_Recent'}, inplace=True)


# Streamlit
st.title("North Carolina Xylazine Reports")
st.subheader("Real-time results from the [UNC Drug Analysis Lab](https://streetsafe.supply)")
st.markdown("---")

# Layout 2 headline data boxes
col1, col2 = st.columns(2)

with col1:
    st.metric(
    label="Total drug samples analayzed",
    value=rows_count
    )

with col2:
    st.metric(
    label="Counties with any drug samples",
    value=counties_sampled
    )



# Layout 2 headline data boxes
col1, col2 = st.columns(2)

with col1:
    st.metric(
    label="Samples with xylazine",
    value=xyl_count
    )
    
with col2:
    st.metric(
    label="Counties with xylazine",
    value=xyl_counties
    )
    
    
st.markdown("---")

st.write(
    label="Xylazine most recently detected",
    value=latest
    )

    
# Latest late of xylazine detection
st.write("Xylazine last detected on:")
st.subheader(latest)
st.markdown("---")


st.subheader(":hospital: [More info on xylazine](https://harmreduction.org/wp-content/uploads/2022/11/Xylazine-in-the-Drug-Supply-one-pager.pdf) in the street drug supply")
st.markdown("---")
st.header("Where has xylzine been detected?")
st.markdown("The following map shows places where we have detected xylazine in street drugs.")


# Render the map
st.map(dfxyl)                         
st.markdown("_Exact locations have been shifted to preserve anonymity._")

st.table(mostrecent)

# st.bar_chart(dfxyl['sen_strength'])

st.markdown("---")

st.markdown("## Where did these drug samples come from?")
st.markdown("A public service of the University of North Carolina. Data from North Carolina harm reduction programs. Full details at our [website](https://streetsafe.supply) and program profile in [_The New York Times_](https://www.nytimes.com/2022/12/24/us/politics/fentanyl-drug-testing.html))")
st.video('https://youtu.be/cWbOeo6pm8A')

st.markdown("Data documentation available [here](https://opioiddatalab.github.io/drugchecking/datasets/).")

st.markdown("---")
st.markdown("_fin._")

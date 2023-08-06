# -*- coding: utf-8 -*-
from load_css import local_css
local_css("datasets/code/Streamlit/style.css")

import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen
import json
# import plotly
import streamlit as st

def get_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/code/Streamlit/x_subs.csv"
    return pd.read_csv(url)
x_subs = get_data()
x_subs = pd.DataFrame(x_subs)
x_subs.set_index('rank', inplace=True)

def get_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/code/Streamlit/x_strength.csv"
    return pd.read_csv(url)
x_strength = get_data()
x_strength = pd.DataFrame(x_strength)
x_strength.set_index('order', inplace=True)

# Import public NC sample data and cache for Streamlit
@st.cache_data()
def get_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_analysis_dataset.csv"
    return pd.read_csv(url)
df = get_data()
df = pd.DataFrame(df)
df.set_index('sampleid', inplace=True)


# Set date format
## Retains seconds unfortunately and NaT
df['date_complete'] = pd.to_datetime(df['date_complete'], format='%d%b%Y', errors = 'coerce')

# Limit to samples with any xylazine detected
dfxyl = df[['date_complete', 'lab_xylazine_any', 'lab_cocaine', 'lab_cocaine', 'lab_meth', 'lab_fentanyl', 'expect_fentanyl', 'county', 'sen_strength', 'sen_strength', 'color', 'texture']]
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
latest = dfxyl['date_complete'].max()
latest = latest.strftime('%A %B %d, %Y')


# Latest xylazine reports by county
def update_entries(grp):
    # update date_complete to most recent date
    grp['date_complete'] = grp['date_complete'].max()
    # if length of county is less than 1, then replace with "County not specified"
    if len(grp['county']) < 1: 
        grp['county'] = "County not specified"
    return grp
# remove all columns except date_complete and county
dfxyl = dfxyl[['county', 'date_complete']]
# only keep the first instance of each county
dfxyl = dfxyl.groupby(by=["county"]).apply(update_entries)
mostrecent = dfxyl.drop_duplicates(subset=['county'])    

# Sensations Graph
import altair as alt

url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/code/Streamlit/x_strength.csv"

sensations = alt.Chart(url).mark_bar(size=40).encode(
    x=alt.X('sensations:N',
            sort=['weaker', 'normal', 'stronger'],
            axis=alt.Axis(title="Relative to Typical Current Supply")),
    y=alt.Y('samples:Q',
            axis=alt.Axis(title="Number of Samples")),
).properties(
    width=alt.Step(80),
    title="Sensations of Drugs Containing Xylazine"
).configure_axis(
   labelFontSize=13,
   titleFontSize=15,
   labelAngle=0
).configure_title(
   fontSize=16
)




# Streamlit
st.title("North Carolina Xylazine Report")
st.subheader("Real-time results from UNC Drug Analysis Lab")
st.markdown("[Our lab in Chapel Hill](https://streetsafe.supply) tests street drugs from 30+ North Carolina harm reduction programs, hospitals, clinics, and health departments. We analyze the samples using GCMS (mass spec). Part of the multi-disciplinary [Opioid Data Lab](https://www.opioiddata.org).")
st.markdown("---")
st.markdown("There is a new cut in street drugs and it causes terrible skin problems. But we didn't have a way to track it in North Carolina. Therefore, we are making data available from our street drug testing lab to prevent public health harms.")

st.markdown("---")

# Layout 2 headline data boxes
col1, col2 = st.columns(2)

with col1:
    st.metric(
    label="Total NC drug samples analayzed",
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
    
st.markdown(":label: Our samples do not represent the entire drug supply. People may send us samples because they suspect xylazine or have unexpected reactions.")

st.markdown("---")

st.write(
    label="Xylazine most recently detected",
    value=latest
    )

    
# Latest late of xylazine detection
st.header("Xylazine last detected on:")
st.subheader(latest)
st.markdown("---")


st.subheader(":hospital: [More info on xylazine](https://harmreduction.org/wp-content/uploads/2022/11/Xylazine-in-the-Drug-Supply-one-pager.pdf) in the street drug supply")
st.markdown("Xylazine (zie-la-zine) is a cut mixed in with other street drugs. It can cause bad skin ulcers beyond the site of injection. Treated early, we can prevent amputation. Drugs with xylazine in it can cause heavy unpleasant sedation that make it *seem* like naloxone isn't working. But naloxone can still help with the fentanyl, so keep it on hand.")

st.markdown("---")
st.header("Where has xylazine been detected?")
st.markdown(":label: Keep in mind we have more samples from the center of the state. Xylazine is certainly present elsewhere.")

# Chloropeth map
## Load public NC data
df = pd.read_csv("https://github.com/opioiddatalab/drugchecking/raw/main/datasets/nc/nc_analysis_dataset.csv")

## Create new variable that calculates the total samples by county for denominator
df["total_samples"] = df.groupby("county")["sampleid"].transform("nunique")

## Create a new dataframe that aggregates the data by county
## Create a new dataframe that aggregates the data by 'county' and 'fips'
agg_df = df.groupby(["county", "countyfips"]).agg(
    xylazine_count=("lab_xylazine_any", "sum"),
    latest_date=("date_complete", "max"),
    unique_samples=("sampleid", "nunique"),
)

## Reset the index of the aggregated dataframe
agg_df = agg_df.reset_index()

## Create percent of samples that are xylazine positive by dividing xylazine_countys by unique_samples
agg_df["percent"] = agg_df["xylazine_count"] / agg_df["unique_samples"] *100

## Add the percent symbol to the 'percent' column
agg_df["percent_str"] = agg_df["percent"].astype(str) + "%"

## Round the 'percent' column to one decimal place
agg_df["percent_str"] = np.round(agg_df["percent"], 1)

## Generate map
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig = px.choropleth_mapbox(agg_df, 
                           geojson=counties,
                           locations='countyfips',
                           color='percent',
                           color_continuous_scale="reds",
                           range_color=(0, 100),
                           mapbox_style="carto-positron",
                           zoom=5.5,
                           center = {"lat": 35.3, "lon": -79.2},
                           opacity=0.8,
                           hover_data={'county':True, 'latest_date':True, 'percent': False, 'percent_str':True, 'unique_samples':False, 'xylazine_count':False, 'countyfips':False},
                           labels={'percent_str':'% Samples with Xylazine', 'county':'County', 'latest_date':'Most Recent Sample Date'},
                          )

fig.update_layout(title_text='Percent of Samples Testing Positive for Xylazine')

st.plotly_chart(fig, use_container_width=True)

                        
st.markdown("We've detected xylazine in about half the places from where we received samples. We are working on better maps! Sorry this isn't perfect, but we will improve it soon.")

st.subheader("Latest xylazine detection dates by location")

def cooling_highlight(val):
    color = 'white' if val else 'white'
    return f'background-color: {color}'

st.dataframe(
    mostrecent,
    height=700,
    column_config={
        'county': st.column_config.TextColumn(
            "County",
            disabled=True
        ),
        'date_complete': st.column_config.DateColumn(
            "Most Recent Sample Date",
            format="dddd MMMM DD, YYYY",
        ),
        'sampleid': None
    },
    hide_index=True,
    use_container_width=True
)

st.markdown("---")

st.header("What substances were also detected?")
st.markdown("Xylazine was found mostly mixed with fentanyl and heroin. But cocaine and xylazine were routinely found together. Less often, we found xylazine in trace amounts with methamphetamine and other drugs. Samples containing xylazine are most often reported to feel stronger.")

col1, col2 = st.columns(2)

with col1:
    st.dataframe(
        x_subs,
        use_container_width=True
        )

with col2:
    st.altair_chart(sensations)

st.markdown("---")

st.markdown("## Where did these drug samples come from?")
st.markdown("A public service of the University of North Carolina. Data from North Carolina harm reduction programs. Full details at our [website](https://streetsafe.supply), at [UNC.edu](https://www.unc.edu/discover/drug-checking-project-cuts-overdoses/), and profiled in [_The New York Times_](https://www.nytimes.com/2022/12/24/us/politics/fentanyl-drug-testing.html))")
st.video('https://youtu.be/cWbOeo6pm8A')

st.markdown("Data documentation available [here](https://opioiddatalab.github.io/drugchecking/datasets/).")

st.markdown("---")
st.header("Why are we concerned about xylazine?")
st.video('https://www.youtube.com/watch?v=orzgwi7sxFM')
st.header("What can we do to handle xylazine skin wounds?")
st.video('https://youtu.be/MVs7ZfILCjE')
st.markdown("---")

st.subheader("Funding")
st.markdown("We are grateful to our two funders: Foundation for Opioid Response Efforts ([FORE](https://forefdn.org)) and the [NC Collaboratory via the NC General Assembly](https://collaboratory.unc.edu/news/2022/12/09/north-carolina-collaboratory-launches-research-projects-to-support-local-opioid-abatement-and-recovery-efforts/) using opioid litigation settlement funds.")

st.markdown("---")
st.markdown("_fin._")
# deleted code\n# commit 90661c07dd69631efb2b960bd6f846c91c3d5191

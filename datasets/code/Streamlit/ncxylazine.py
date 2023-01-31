# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import numpy as np

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
@st.cache(suppress_st_warning=True)
def get_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_analysis_dataset.csv"
    return pd.read_csv(url)
df = get_data()
df = pd.DataFrame(df)
df.set_index('sampleid', inplace=True)

# Jitter locations where sample collected for mapping
sigma = 0.08
df['lat'] = df['lat'].apply(lambda x: np.random.normal(x, sigma))
df['lon'] = df['lon'].apply(lambda x: np.random.normal(x, sigma))

# Set date format
## Retains seconds unfortunately and NaT
df['date_complete'] = pd.to_datetime(df['date_complete'], format='%d%b%Y', errors = 'coerce')

# Limit to samples with any xylazine detected
dfxyl = df[['date_complete', 'lab_xylazine_any', 'lab_cocaine', 'lab_cocaine', 'lab_meth', 'lab_fentanyl', 'expect_fentanyl', 'county', 'sen_strength', 'sen_strength', 'color', 'texture','lat', 'lon']]
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
latestreport = dfxyl.groupby(by=["county"]).max()
latestreport["date_complete"] = latestreport["date_complete"].dt.strftime('%B %d, %Y')
mostrecent = latestreport[['date_complete']].copy()
mostrecent.rename(columns={'date_complete': 'Most_Recent'}, inplace=True)

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
st.markdown("[Our lab in Chapel Hill](https://streetsafe.supply) tests street drugs from 19 North Carolina harm reduction programs. We analyze the samples using GCMS (mass spec). Part of the multi-disciplinary [Opioid Data Lab](https://www.opioiddata.org).")
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
    
st.markdown(":label: Our samples do not represent the entrire drug supply. People may send us samples because they suspect xylazine or have unexpected reactions.")

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
st.markdown("Xylazine (sigh-la-scene) is a cut mixed in with other street drugs. It can cause horrific skin ulcers, beyond the site of injection. If treated early, we can prevent amputation. Drugs with xylazine in it can cause heavy unpleasant sedation that make it *seem* like naloxone isn't working. But naloxone can still help with the fentanyl, so keep it on hand.")

st.markdown("---")
st.header("Where has xylzine been detected?")
st.markdown("The map shows where we have detected xylazine in street drugs.")
st.markdown(":label: Keep in mind we have more programs and samples from the center of the state. Xylazine is certainly present elsewhere.")

# Render the map
st.map(dfxyl)                         
st.markdown("_Exact locations shifted to preserve anonymity. Don't bother zooming into street level._")

st.subheader("Latest xylazine detection dates by location")

st.table(mostrecent)

st.markdown("---")

st.header("What substances were also detected?")
st.markdown("Xylazine was found mostly mixed with fentanyl and heroin. But cociane and xylazine were routinely found together. Less often, we found xylazine in trace amounts with methamphetamine and other drugs. Samples containing xylazine are most often reported to feel stronger.")

col1, col2 = st.columns(2)

with col1:
    st.dataframe(x_subs)

with col2:
    st.altair_chart(sensations)

st.markdown("---")

st.markdown("## Where did these drug samples come from?")
st.markdown("A public service of the University of North Carolina. Data from North Carolina harm reduction programs. Full details at our [website](https://streetsafe.supply) and program profile in [_The New York Times_](https://www.nytimes.com/2022/12/24/us/politics/fentanyl-drug-testing.html))")
st.video('https://youtu.be/cWbOeo6pm8A')

st.markdown("Data documentation available [here](https://opioiddatalab.github.io/drugchecking/datasets/).")

st.markdown("---")
st.header("Why are we concerned about xylazine?")
st.video('https://www.youtube.com/watch?v=orzgwi7sxFM')

st.markdown("---")

st.subheader("Funding")
st.markdown("We are grateful to our two funders: Foundation for Opioid Response Efforts ([FORE](https://forefdn.org)) and the [UNC Collaboratory via the NC General Assembly](https://collaboratory.unc.edu/news/2022/12/09/north-carolina-collaboratory-launches-research-projects-to-support-local-opioid-abatement-and-recovery-efforts/) using opioid litigation settlement funds.")

st.markdown("---")
st.markdown("_fin._")



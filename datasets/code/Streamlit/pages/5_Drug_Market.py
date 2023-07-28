from load_css import local_css
local_css("datasets/code/Streamlit/style.css")
import streamlit as st
import pandas as pd
import json

def get_nc_most_recent():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_most_recent.csv"
    return pd.read_csv(url)
nc_most_recent = get_nc_most_recent()

def get_nc_locations():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_county_list.csv"
    return pd.read_csv(url)
nc_market_locs = get_nc_locations()
nc_market_locs_df = pd.DataFrame(nc_market_locs)
nc_market_locs_df.set_index('county', inplace=True)

def get_nc_ds_sub_count():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_substances_count.csv"
    return pd.read_csv(url)
nc_market_sub_count = get_nc_ds_sub_count()

# get the value from the substances_detected col in the nc_substances_count csv
nc_market_sub_count_number = nc_market_sub_count.iloc[0]['substances_detected']

def get_nc_ds_substances():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_substances_list.csv"
    return pd.read_csv(url)
nc_market_substances = get_nc_ds_substances()
nc_market_substances_df = pd.DataFrame(nc_market_substances)
nc_market_substances_df.set_index('substance', inplace=True)


# get the value from the date_complete col in the nc_most_recent csv
nc_mr = nc_most_recent.iloc[0]
# convert this into a human readable date
nc_mr['date_complete'] = pd.to_datetime(nc_mr['date_complete']).strftime('%B %d, %Y')

# print the json to the screen
# Streamlit
st.title("North Carolina Drug Market")
st.subheader("Real-time results from UNC Drug Analysis Lab")

st.markdown("[Our lab in Chapel Hill](https://streetsafe.supply) tests street drugs from 30+ North Carolina harm reduction programs, hospitals, clinics, and health departments. We analyze the samples using GCMS (mass spec). Part of the multi-disciplinary [Opioid Data Lab](https://www.opioiddata.org).")
st.markdown("---")
html_str = f"""
<h2 class="a">Most Recent Sample: {nc_mr['date_complete']}</h2>
"""
st.markdown(html_str, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Samples", value=712)
with col2:
    st.metric(label="Programs & Clinics", value=26)
with col3:
    st.metric(label="Counties", value=20)
with col4:
    st.metric(label="Substances Detected", value=104)

st.markdown("## Locations")
st.dataframe(
    nc_market_locs_df,
    height=300,
    column_config={
        'county': st.column_config.TextColumn(
            "County",
            disabled=True
        ),
        'samples': st.column_config.NumberColumn(
            "Samples",
            disabled=True
        ),
        'latest_date': st.column_config.DateColumn(
            "Most Recent Sample Date",
            format="dddd MMMM DD, YYYY",
        ),
    },
    hide_index=True,
    use_container_width=True
)
st.markdown("---")

st.markdown("## How pure is the NC drug supply?")
st.markdown("**the number of substances detected is a measurement of how contaminated the drug supply is*")
# @NAB - do you want this listed in a table? or just the substances printed onto screen in columns?
st.dataframe(
    nc_market_substances,
    height=300,
    column_config={
        'substance': st.column_config.TextColumn(
            "Substance",
            disabled=True
        ),
        'pubchemcid': st.column_config.TextColumn(
            "PubChem CID",
            disabled=True
        ),
        'total': st.column_config.NumberColumn(
          "Total",
          disabled=True
        ),
        'primary': st.column_config.NumberColumn(
          "Primary",
          disabled=True
        ),
        'trace': st.column_config.NumberColumn(
          "Trace",
          disabled=True
        ),
        'latest_detected': st.column_config.DateColumn(
            "Most Recent Detection Date",
            format="dddd MMMM DD, YYYY",
        ),
    },
    hide_index=True,
    use_container_width=True
)


html_str = f"""
<h4 class="">Number of Substances Detected: {nc_market_sub_count_number}</h4>
"""
st.markdown(html_str, unsafe_allow_html=True)
st.markdown("**the number of substances detected by GCMS. GCMS is tuned to pick up small molecules that are likely to be psychoactive. Does not include cuts and fillers.*")



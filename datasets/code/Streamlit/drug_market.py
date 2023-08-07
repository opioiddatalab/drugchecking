from load_init import local_css, create_sidebar, convert_df, add_county_group
import streamlit as st
st.set_page_config(
    page_title="NC Drug Market",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
)
local_css("datasets/code/Streamlit/style.css")
import pandas as pd
import json
import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re
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
nc_market_substances = pd.DataFrame(nc_market_substances)
# map over the latest_dected col and convert to human readable date
nc_market_substances['latest_detected'] = pd.to_datetime(nc_market_substances['latest_detected']).dt.strftime('%b %d, %Y')
# map over the pubchemcid col and if there is no value, add "none" to the cel
nc_market_substances['pubchemcid'] = nc_market_substances['pubchemcid'].apply(lambda x: x if x != 'nan' else 'none')
# make it categorical, otherwise the commas get inserted and it treats them as floats
nc_market_substances['pubchemcid'] = nc_market_substances['pubchemcid'].astype({'pubchemcid': 'category'})
# add 6 columns to nc_market_substances named 'West', 'Triad', 'Trangle', 'Charlotte', 'ENC', 'Faeyettville' and randomly assign each cell in the row a value between 1 and 100
# set the index to the substance col
nc_market_substances.set_index('substance', inplace=True)
# sort the df by the latest_detected col
nc_market_substances.sort_values(by=['latest_detected'], inplace=True, ascending=False)
# convert the latest_detected col to a human readable date
nc_market_substances['latest_detected'] = pd.to_datetime(nc_market_substances['latest_detected']).dt.strftime('%B %d, %Y')







def get_nc_analysis_ds():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_analysis_dataset.csv"
    return pd.read_csv(url)
def get_nc_lab_detail_ds():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_lab_detail.csv"
    return pd.read_csv(url)

def get_nc_ds_purity():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_purity.csv"
    return pd.read_csv(url)
nc_ds_purity = get_nc_ds_purity()
nc_ds_purity_df = pd.DataFrame(nc_ds_purity)
nc_ds_purity_df.set_index('drug', inplace=True)


# get the value from the date_complete col in the nc_most_recent csv
nc_mr = nc_most_recent.iloc[0]
# convert this into a human readable date
nc_mr['date_complete'] = pd.to_datetime(nc_mr['date_complete']).strftime('%B %d, %Y')

#streamlit
create_sidebar()
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
st.markdown("## What substances are in the NC drug Supply?")
# st.dataframe(nc_market_substances, use_container_width=True)
nc_market_substances_top_15 = nc_market_substances.nlargest(15, 'total')
nc_market_substances_top_15 = nc_market_substances_top_15.drop('pubchemcid', axis=1)
nc_market_substances_top_15 = nc_market_substances_top_15.drop('primary', axis=1)
nc_market_substances_top_15 = nc_market_substances_top_15.drop('trace', axis=1)
nc_analysis = get_nc_analysis_ds()
nc_lab_detail = get_nc_lab_detail_ds()

def get_substances_list():
    return nc_market_substances_top_15.index.tolist()
def county_substance_count(substance, cg, df):
  # get a count of how many times a substance is found in a county_group in the df
  val = df[(df['substance'] == substance) & (df['county_group'] == cg)].shape[0]
  return str(val)

def get_substance_county_df(nc_df):
  # merge the nc_lab_detail and nc_analysis dfs on the sampleid col
  df = pd.merge(nc_lab_detail, nc_analysis, on='sampleid')
  df = df[['sampleid',  'substance', 'county', 'date_collect']]
  df = df[df['substance'].isin(get_substances_list())]
  df['county_group'] = ''
  df['county_group'] = df['county'].apply(lambda x: add_county_group(x))
  df = df[df['county'].str.len() >= 2]
  df['sub_counter'] = ''
# find out how many times a row's substance occurs in the df for each county_group
  df['sub_counter'] = df.groupby(['substance', 'county_group'])['substance'].transform('count')
# sort the df by the sub_counter col
  df.sort_values(by=['sub_counter'], inplace=True, ascending=False)
  # I want to know how often a substnace is found in a given county
  # remove the sample id col
  df = df.drop('sampleid', axis=1)
  return df

with st.expander("View raw data table", ):
  with st.container():
    df_1 = get_substance_county_df(nc_market_substances_top_15)
    # create a new df that has the nc_market_substances_top_15
    df_2 = pd.DataFrame(nc_market_substances_top_15)
    # drop all cols except the substance col
    df_2 = df_2.drop('latest_detected', axis=1)
    # get the count for how many times a substance is found in a county_group
    df_2['county_group_1'] = ''
    df_2['county_group_2'] = ''
    df_2['county_group_3'] = ''
    df_2['county_group_4'] = ''
    df_2['county_group_5'] = ''
    df_2['county_group_6'] = ''
    # map over each row in df_2 and get the substance name, then get the county_group and count how many times that substance is found in that county_group
    for index, row in df_2.iterrows():
        df_2.at[index, 'county_group_1'] = county_substance_count(index, 1, df_1)
        df_2.at[index, 'county_group_2'] = county_substance_count(index, 2, df_1)
        df_2.at[index, 'county_group_3'] = county_substance_count(index, 3, df_1)
        df_2.at[index, 'county_group_4'] = county_substance_count(index, 4, df_1)
        df_2.at[index, 'county_group_5'] = county_substance_count(index, 5, df_1)
        df_2.at[index, 'county_group_6'] = county_substance_count(index, 6, df_1)

    st.dataframe(df_2)

    csv = convert_df(nc_market_substances_top_15)
    st.download_button(
      "Download csv",
      csv,
      "file.csv",
      "text/csv",
      key='download-csv'
    )

st.markdown("---")
st.markdown("## How pure is the NC drug supply?")
st.markdown("**the number of substances detected is a measurement of how contaminated the drug supply is*")
with st.container():
    st.dataframe(
      nc_ds_purity_df,
      height=200,
      column_config={
          'drug': st.column_config.TextColumn(
              "Drug",
              disabled=True
          ),
          'average': st.column_config.NumberColumn(
              "Average",
              disabled=True
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



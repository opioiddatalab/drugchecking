from load_init import local_css, create_sidebar, convert_df
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
def generate_random_number(x):
    return random.uniform(0.09, 0.991)
columns_to_map = ['West', 'Triad', 'Triangle', 'Charlotte', 'ENC', 'Fayetteville']
for column in columns_to_map:
  nc_market_substances[column] = 0
nc_market_substances[columns_to_map] = nc_market_substances[columns_to_map].applymap(generate_random_number)

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
# create a new df that merges in the
with st.expander("Show tabular data (exportable)"):
  st.dataframe(nc_market_substances_top_15, use_container_width=True)
  csv = convert_df(nc_market_substances_top_15)
  st.download_button(
    "Download csv",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
  )
nc_analysis = get_nc_analysis_ds()
nc_lab_detail = get_nc_lab_detail_ds()

# fn to return all the substances from nc_market_substances_top_15 in a list format
def get_substances_list():
    return nc_market_substances_top_15.index.tolist()

# create a new dataframe with the following columns: county group, substance, latest_detected, and percentage samples testing positive
def get_substance_county_df():
    # create a new df with the following columns: county group, substance, latest_detected, and percentage samples testing positive
    nc_substance_county_df = pd.DataFrame(columns=['county_group', 'substance', 'latest_detected', '% samples_testing_positive'])
    # loop over each substance in the list of substances
    for substance in get_substances_list():
        # loop over each row in the nc_analysis df
        for index, row in nc_analysis.iterrows():
            # if the substance in the list matches the substance in the nc_analysis df
            if substance == row['substance']:
                # loop over each row in the nc_lab_detail df
                for index, row in nc_lab_detail.iterrows():
                    # if the substance in the list matches the substance in the nc_lab_detail df
                    if substance == row['substance']:
                        # create a new row in the nc_substance_county_df df with the following values
                        nc_substance_county_df = nc_substance_county_df.append({
                            'county_group': row['county_group'],
                            'substance': row['substance'],
                            'latest_detected': row['latest_detected'],
                            'percentage_samples_testing_positive': row['percentage_samples_testing_positive']
                        }, ignore_index=True)
    return nc_substance_county_df

st.markdown("---")
st.markdown("## How pure is the NC drug supply?")
st.markdown("**the number of substances detected is a measurement of how contaminated the drug supply is*")
# @NAB - do you want this listed in a table? or just the substances printed onto screen in columns?
st.dataframe(
    nc_ds_purity_df,
    height=300,
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



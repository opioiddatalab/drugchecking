from load_css import local_css
local_css("datasets/code/Streamlit/style.css")
import streamlit as st
import pandas as pd
import json
import random
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
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
nc_market_substances['latest_detected'] = pd.to_datetime(nc_market_substances['latest_detected'])
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
st.markdown("## What substances are in the NC drug Supply?")
# use streamlit to display the df and allow whole width
st.dataframe(nc_market_substances, use_container_width=True)
nc_market_substances_top_10 = nc_market_substances.nlargest(10, 'total')
# remove the pubchemcid col
nc_market_substances_top_10 = nc_market_substances_top_10.drop('pubchemcid', axis=1)
nc_market_substances_top_10 = nc_market_substances_top_10.drop('latest_detected', axis=1)
fig, ax = plt.subplots()
sns.heatmap(nc_market_substances_top_10.corr(), annot=True,fmt=".2f",mask=np.triu(np.ones_like(nc_market_substances_top_10.corr(),dtype=bool)))
st.write(fig)

# def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Adds a UI on top of a dataframe to let viewers filter columns

#     Args:
#         df (pd.DataFrame): Original dataframe

#     Returns:
#         pd.DataFrame: Filtered dataframe
#     """
#     modify = st.checkbox("Add filters")

#     if not modify:
#         return df

#     df = df.copy()

#     # Try to convert datetimes into format="dddd MMMM DD, YYYY",

#     for col in df.columns:
#       if col == 'pubchemcid':
#          pass
#       if col == 'latest_detected':
#         try:
#           df[col] = pd.to_datetime(df[col], format='%Y-%m-%d')
#         except Exception:
#           pass
#       if is_object_dtype(df[col]):
#         try:
#           df[col] = pd.to_datetime(df[col], format='%Y-%m-%d')
#         except Exception:
#           pass

#       if is_datetime64_any_dtype(df[col]):
#         df[col] = pd.to_datetime(df[col], format='%Y-%m-%d ')

#     modification_container = st.container()
#     with modification_container:
#         # @Nab - having an issue here because of the empty pubchemcid col values
#         # make a copy of df.columns but remove pubchemcid
#         copy_df_columns = df.columns
#         copy_df_columns = copy_df_columns.drop('pubchemcid')
#         to_filter_columns = st.multiselect("Filter dataframe on", copy_df_columns)
#         # remove pubchemcid from to_filter_columns
#         for column in to_filter_columns:
#             left, right = st.columns((1, 20))
#             # Treat columns with < 10 unique values as categorical
#             if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
#                 user_cat_input = right.multiselect(
#                     f"Values for {column}",
#                     df[column].unique(),
#                     default=list(df[column].unique()),
#                 )
#                 df = df[df[column].isin(user_cat_input)]
#             elif is_numeric_dtype(df[column]):
#                 _min = float(df[column].min())
#                 _max = float(df[column].max())
#                 step = (_max - _min) / 100
#                 user_num_input = right.slider(
#                     f"Values for {column}",
#                     min_value=_min,
#                     max_value=_max,
#                     value=(_min, _max),
#                     step=step,
#                 )
#                 df = df[df[column].between(*user_num_input)]
#             elif is_datetime64_any_dtype(df[column]):
#                 user_date_input = right.date_input(
#                     f"Select a date range",
#                     value=(
#                 #  today's date minus 90 days
#                   pd.to_datetime("today") - pd.Timedelta(days=90),
#                   # make max the current date + the number of days remaining in the current month
#                   pd.to_datetime("today") + pd.offsets.MonthEnd(0)
#                     ),
#                     help="Use the date picker to select a date range. Defaults to previous 90 days. "
#                 )
#                 if len(user_date_input) == 2:
#                     user_date_input = tuple(map(pd.to_datetime, user_date_input))
#                     start_date, end_date = user_date_input
#                     df = df.loc[df[column].between(start_date, end_date)]
#             else:
#                 user_text_input = right.text_input(
#                     f"Substring or regex in {column}",
#                 )
#                 if user_text_input:
#                     df = df[df[column].astype(str).str.contains(user_text_input)]

#     return df
# data_url = "https://raw.githubusercontent.com/mcnakhaee/palmerpenguins/master/palmerpenguins/data/penguins.csv"

# st.dataframe(filter_dataframe(nc_market_substances))

# st.dataframe(nc_market_substances_df.style.highlight_max(axis=0), height=300, width=800)
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



from load_css import local_css
local_css("datasets/code/Streamlit/style.css")
local_css("datasets/code/Streamlit/pages/psychedelics.css")
from streamlit_elements import elements, mui, html, dashboard
import streamlit as st
from persist import persist, load_widget_state
import webbrowser
import pandas as pd
import random


def get_nc_ds_substances():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_substances_list.csv"
    return pd.read_csv(url)
nc_psychedelics_et_al = get_nc_ds_substances()
# map over the latest_detected col and convert to human readable date
nc_psychedelics_et_al['latest_detected'] = pd.to_datetime(nc_psychedelics_et_al['latest_detected'], format='%d%b%Y').dt.strftime('%B %d, %Y')

nc_psychedelics_et_al = pd.DataFrame(nc_psychedelics_et_al)

# def generate_random_number(x):
#     return random.uniform(0.09, 0.991)
# columns_to_map = ['West', 'Triad', 'Triangle', 'Charlotte', 'ENC', 'Fayetteville']
# for column in columns_to_map:
#   nc_psychedelics_et_al[column] = 0
# nc_psychedelics_et_al[columns_to_map] = nc_psychedelics_et_al[columns_to_map].applymap(generate_random_number)

# set the index to the substance col
nc_psychedelics_et_al_cpy = nc_psychedelics_et_al
nc_psychedelics_et_al.set_index('substance', inplace=True)
# sort the df by the latest_detected col
nc_psychedelics_et_al.sort_values(by=['latest_detected'], inplace=True, ascending=False)
# convert the latest_detected col to a human readable date
nc_psychedelics_et_al['latest_detected'] = pd.to_datetime(nc_psychedelics_et_al['latest_detected']).dt.strftime('%B %d, %Y')
nc_psychedelics_et_al_list =[
  "metonitazene",
  "isotonitazene",
  "protonitazene",
  "N-noramidopyrine Etodesnitazene",
  "N-Pyrrolidino Isotonitazene",
  "N-Pyrrolidino Etonitazene",
  "N-Piperidinyl Etonitazene",
  "ketamine",
  "phencyclidine (PCP)",
  "3-methoxy-PCP",
  "2C-B",
  "2C-H",
  "mescaline",
  "psilocin",
  "N,N-dimethyltryptamine (DMT)",
  "5/6-MeO-DMT",
  "metonitazene",
  "N-piperidinyl etonitazene",
  "isotonitazene",
  "2-Fluoro-2-oxo PCE",
  "3,4-methylenedioxy-N-benzylcathinone (BMDP)",
  "eutylone",
  "N,N-dimethylpentylone",
  "N-ethylpentylone",
  "4-Methylmethcathinone",
  "α-Ethylaminopentiophenone",
  "α-Pyrrolidinoisohexanophenone",
  "methylone",
  "3,4-Methylenedioxy-α-Cyclohexylaminopropiophenone",
  "4-fluoro-alpha-PHP",
  "MDMA",
  "MDA",
  "5/6-APB",
  "LSD",
  "Synthetic cannabinoids",
  "MDMB-4en-PINACA",
  "ADB-INACA",
  "ADB-4en-PINACA",
  "ADB-BUTINACA",
]
# map of the nc_psychedelics_et_al df and remove any rows where the substance is not in the nc_psychedelics_et_all_list

nc_psychedelics_et_al = nc_psychedelics_et_al[nc_psychedelics_et_al.index.isin(nc_psychedelics_et_al_list)]
nc_psychedelics_et_al_count = len(nc_psychedelics_et_al.index)

nc_psychedelics_et_al = nc_psychedelics_et_al.drop('pubchemcid', axis=1)
nc_psychedelics_et_al = nc_psychedelics_et_al.drop('primary', axis=1)
nc_psychedelics_et_al = nc_psychedelics_et_al.drop('trace', axis=1)


def get_nc_county_count():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_countycount.csv"
    return pd.read_csv(url)
nc_countycount = get_nc_county_count()
nc_countycount_int = nc_countycount.iloc[0]['nc_countycount']

def get_nc_program_count():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_prorgams.csv"
    return pd.read_csv(url)
nc_program_count = get_nc_program_count()
nc_program_count_int = nc_program_count.iloc[0]['nc_programs']


def get_nc_sample_count():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_samples.csv"
    return pd.read_csv(url)
nc_sample_count = get_nc_sample_count()
nc_sample_count_int = nc_sample_count.iloc[0]['nc_samples']


st.title("Psychedelics and Other Drugs in NC")
st.write("We are watching a number of different kinds of psychedelics and other drugs in North Carolina right now....")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Samples", value=nc_sample_count_int)
with col2:
    st.metric(label="Programs & Clinics", value=nc_program_count_int)
with col3:
    st.metric(label="Counties", value=nc_countycount_int)
with col4:
    st.metric(label="+Psychedelics or similar subs", value=nc_psychedelics_et_al_count)
st.dataframe(
      nc_psychedelics_et_al,
      height=350,
      column_config={
          'latest_detected': st.column_config.TextColumn(
              "Latest Detected",
              disabled=True
          ),
          'total': st.column_config.NumberColumn(
              "Total",
              disabled=True,
          ),
          'substance': st.column_config.TextColumn(
              "Substance",
              disabled=True
          ),
      })
st.markdown("---")
# write a function that accepts a dataframe as its first param and a list as its second param. the function should map over the df and only return rows where the value in the 'substance' col matches one of the values in the list

def generate_container_with_rows(items):
    with st.container():
      col1, col2, col3 = st.columns(3)
      list_length = len(items)
      list_length_divided_by_three = round(list_length / 3)
      first_column_items = items[:list_length_divided_by_three]
      second_column_items = items[list_length_divided_by_three:list_length_divided_by_three * 2]
      third_column_items = items[list_length_divided_by_three * 2:]
      #  fill each col with corresponding list
      with col1:
          for item in first_column_items:
            label1 = list(item.keys())[0]
            value1 = list(item.values())[0]
            st.metric(label=label1, value=value1)
      with col2:
          for item in second_column_items:
              label = list(item.keys())[0]
              value = list(item.values())[0]
              st.metric(label=label, value=value)
      with col3:
          for item in third_column_items:
              label = list(item.keys())[0]
              value = list(item.values())[0]
              st.metric(label=label, value=value)


    return st.container()

lsd_list = ['lysergic acid diethylamide (LSD)']
mdma_list = [
  "MDMA",
  "MDA",
  "5/6-APB",
  "ketamine",
]
syncan_list = [
  "MDMB-4en-PINACA",
  "ADB-INACA",
  "ADB-4en-PINACA",
  "ADB-BUTINACA    ",
]
subcath_list = [
  "3,4-methylenedioxy-N-benzylcathinone (BMDP)",
  "eutylone",
  "N,N-dimethylpentylone",
  "N-ethylpentylone",
  "4-Methylmethcathinone",
  "α-Ethylaminopentiophenone",
  "α-Pyrrolidinoisohexanophenone",
  "methylone",
  "3,4-Methylenedioxy-α-Cyclohexylaminopropiophenone",
  "4-fluoro-alpha-PHP",
]
nitaz_list = [
  "metonitazene",
  "N-piperidinyl etonitazene",
  "isotonitazene",
  "2-Fluoro-2-oxo PCE",
]
other_list = [
  "phencyclidine (PCP)",
  "3-methoxy-PCP",
  "2C-B",
  "2C-H",
  "mescaline",
  "psilocin",
  "N,N-dimethyltryptamine (DMT)",
  "5/6-MeO-DMT",
]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['LSD','MDMA', 'Synthetic Cannabinoids', 'Substituted Cathinones', 'Nitazines', 'Other'])
with tab1:
    # rpint the name of the first column in nc_psychedelics_et_al_cpy

    filtered_df = nc_psychedelics_et_al_cpy[nc_psychedelics_et_al_cpy.index.isin(mdma_list)]
    # drop all columns except 'substance' and 'total'
    filtered_df = filtered_df.drop(['latest_detected', 'pubchemcid', 'trace', 'primary'], axis=1)
    # map over filtered_df index and create a list of objects. Use the index col as the key and the 'total' col as the vaue
    filtered_df = filtered_df.to_dict('records')

    st.markdown("### Drugs commonly sold as LSD")
    st.markdown("*2-3 sentence description.")
    generate_container_with_rows(filtered_df)
with tab2:
    # cpy_ = filter_df_by_list(nc_psychedelics_et_al, mdma_list)
    st.markdown("### Drugs commonly sold as MDMA")
    st.markdown("*(dimethylpentylone, MDA + other methylated amphetamines besides MDMA)*")
    generate_container_with_rows([{"metonitazene":14}, {"aspirin":14}, {"shit":14}])
with tab3:
    # cpy_ = filter_df_by_list(nc_psychedelics_et_al, syncan_list)
    st.markdown("### Substances found with Synthetic Cannabinoids")
    st.markdown('These are commonly sold as "K2" or "spice" in North Carolina.')
    # generate_container_with_rows(['this thing', 'that thing', 'the other thing', 'some more things', 'even more things'])
with tab4:
    # cpy_ = filter_df_by_list(nc_psychedelics_et_al, subcath_list)
    st.markdown("### Substances known as Substituted Cathinones")
    st.markdown("2-3 sentence description.")
    # generate_container_with_rows(['this thing', 'that thing', 'the other thing', 'some more things', 'even more things'])
with tab5:
    # cpy_ = filter_df_by_list(nc_psychedelics_et_al, nitaz_list)
    st.markdown("### Emergening Nitazines")
    st.markdown("2-3 sentence description.")
    # generate_container_with_rows(['this thing', 'that thing', 'the other thing', 'some more things', 'even more things'])
with tab6:
    cpy_ = nc_psychedelics_et_al
    # st.markdown("### Other Emerging Drugs/Substances", other_list)
    st.markdown("2-3 sentence description.")
    # generate_container_with_rows(['this thing', 'that thing', 'the other thing', 'some more things', 'even more things'])

#  LSD (do we have enough?)
# Ketamime
# Synthetic cannabinoids
# Substituted cathinones
st.markdown("---")

with st.container():
    st.subheader("Does this represent the entire NC Drug Supply?")
    st.write("We have analyzed a limited number of these drugs. People may send us samples because the drugs caused unexpected effects. Our data don't represent the entire drug supply in North Carolina.")
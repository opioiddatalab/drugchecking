from load_init import local_css, create_sidebar, convert_df, get_nc_intro_metrics, get_nc_merged_df, get_nc_county_count, get_nc_program_count, get_nc_sample_count, generate_container_with_rows, generate_adulterant_df, generate_drug_supply_table
from streamlit_elements import elements, mui, html, dashboard
import streamlit as st
st.set_page_config(
    page_title="NC Psychedelics & Others",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="collapsed",
)
local_css("datasets/code/Streamlit/pages/psychedelics.css")
local_css("datasets/code/Streamlit/style.css")
from persist import persist, load_widget_state
import webbrowser
import pandas as pd
import random
import math
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode


def get_hnc_lab_detail():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/selfservice/hnc/lab_detail.csv"
    return pd.read_csv(url)
lab_detail = get_hnc_lab_detail()
def get_nc_ds_substances():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_substances_list.csv"
    return pd.read_csv(url)
# update this function to return a json object instead of a df or csv
def get_nc_ds_substances_json():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_substances_list.csv"
    return pd.read_csv(url).to_json()
nc_psychedelics_et_al = get_nc_ds_substances()
nc_psychedelics_et_al_j = get_nc_ds_substances_json()
# map over the latest_detected col and convert to human readable date
nc_psychedelics_et_al['latest_detected'] = pd.to_datetime(nc_psychedelics_et_al['latest_detected'], format='%d%b%Y').dt.strftime('%B %d, %Y')

nc_psychedelics_et_al = pd.DataFrame(nc_psychedelics_et_al)

nc_psychedelics_et_al.set_index('substance', inplace=True)
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

nc_psychedelics_et_al = nc_psychedelics_et_al[nc_psychedelics_et_al.index.isin(nc_psychedelics_et_al_list)]
nc_psychedelics_et_al_count = len(nc_psychedelics_et_al.index)



nc_main_dataset = get_nc_merged_df(nc_psychedelics_et_al_list)
nc_main_cpy = nc_main_dataset.copy()
create_sidebar()
st.markdown("# Psychedelics and Other Drugs in NC")
st.write("We are watching a number of different kinds of psychedelics and other drugs in North Carolina right now....")
get_nc_intro_metrics({
  "All Samples": get_nc_sample_count(),
  "Programs & Clinics": get_nc_program_count(),
  "Counties": get_nc_county_count(),
  "Psychedelics & Others": nc_psychedelics_et_al_count
}, len(nc_main_dataset['sampleid']), nc_psychedelics_et_al_list, nc_psychedelics_et_al)



st.markdown("---")

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
def build_dict_from_json(json_obj):
    # convert the json obj to a df
    df = pd.read_json(json_obj)
    # set the index to the substance col
    df.set_index('substance', inplace=False)
    # sort the df by the latest_detected col
    return df.to_dict('records')

df = build_dict_from_json(nc_psychedelics_et_al_j)
# add an index int col to the df
df = pd.DataFrame(df)
df['index'] = df.index
# set the index to the index col
df.set_index('index', inplace=True)
st.subheader("View substances by category")
#  metrics for counts by category
with st.container():
  col1, col2, col3 = st.columns(3)
  with col1:
    lsd_count = df[df['substance'].isin(lsd_list)]
    total_count = lsd_count['total'].sum()
    st.metric(label="LSD", value=total_count)
  with col2:
     mdma_count = df[df['substance'].isin(mdma_list)]
     total_count = mdma_count['total'].sum()
     st.metric(label="MDMA", value=total_count)
  with col3:
     syncan_count = df[df['substance'].isin(syncan_list)]
     total_count = syncan_count['total'].sum()
     st.metric(label="Synthetic Cannabinoids", value=total_count)
  col1, col2, col3 = st.columns(3)
  with col1:
     subcath_count = df[df['substance'].isin(subcath_list)]
     total_count = subcath_count['total'].sum()
     st.metric(label="Substituted Cathiones", value=total_count)
  with col2:
     nitaz_count = df[df['substance'].isin(nitaz_list)]
     total_count = nitaz_count['total'].sum()
     st.metric(label="Nitazines", value=total_count)
  with col3:
    #  calculate the total of all the values from the 'total' column
    other_count = df[df['substance'].isin(other_list)]
    total_count = other_count['total'].sum()
    st.metric(label="Other", value=total_count)
st.subheader("What else is found in these samples?")
st.write("This is the list of chemicals and drugs we have found in samples from North Carolina.")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['LSD','MDMA', 'Synthetic Cannabinoids', 'Substituted Cathinones', 'Nitazines', 'Other'])
with st.container():
  with tab1:
      # filter the df to remove any entries that are not included in the lsd_list
      filtered_df = df[df['substance'].isin(lsd_list)]
      st.write("Drugs commonly sold as LSD")
      generate_adulterant_df(filtered_df)
  with tab2:
      filtered_df = df[df['substance'].isin(mdma_list)]
      st.write("Drugs commonly sold as MDMA")
      generate_adulterant_df(filtered_df)
  with tab3:
      filtered_df = df[df['substance'].isin(syncan_list)]
      st.write("Substances found with Synthetic Cannabinoids")
      generate_adulterant_df(filtered_df)
  with tab4:
      filtered_df = df[df['substance'].isin(subcath_list)]
      st.write("Substances known as Substituted Cathinones")
      generate_adulterant_df(filtered_df)
  with tab5:
      filtered_df = df[df['substance'].isin(nitaz_list)]
      st.write("### Emerging Nitazines")
      generate_adulterant_df(filtered_df)
  with tab6:
      filtered_df = df[df['substance'].isin(other_list)]
      st.write("### Other Emerging Drugs/Substances"   )
      generate_adulterant_df(filtered_df)

st.write("We are working on a simple chemical dictionary to help make sense of these. Stay tuned!")

st.markdown("---")

generate_drug_supply_table(nc_psychedelics_et_al_list)

st.markdown("---")
st.markdown("## Resources for party drug users")
tab1, tab2 = st.tabs(['DanceSafe info' ,'DanceSafe kits?'])
with tab1:
  st.write("Dance Safe")
with tab2:
  st.write("Dance Safe kits")



# THIS IS CODE FOR THE CARDS, HOLDING OFF ON THIS FOR NOW:

# from load_css import local_css
# local_css("datasets/code/Streamlit/style.css")
# local_css("datasets/code/Streamlit/pages/psychedelics.css")
# from streamlit_elements import elements, mui, html, dashboard
# import streamlit as st
# from persist import persist, load_widget_state
# import webbrowser

# def main():
#     if "alpha_PERSIST" not in st.session_state:
#         # Initialize session state.
#         st.session_state.update({
#             # Default page.
#             "checkbox": False,
#         })
#     else:
#         st.session_state.update({
#             # Default page.
#             "checkbox": True,
#         })

# if __name__ == "__main__":
#     load_widget_state()
#     main()

# if 'first_PERSIST' not in st.session_state:
#    st.session_state['first_PERSIST'] = False
# if 'second_PERSIST' not in st.session_state:
#    st.session_state['second_PERSIST'] = False
# if 'third_PERSIST' not in st.session_state:
#    st.session_state['third_PERSIST'] = False


# def form_callback():
#     st.session_state.first_PERSIST = not st.session_state.first_PERSIST
# def form_callback2():
#     st.session_state.second_PERSIST = not st.session_state.second_PERSIST
# def form_callback3():
#     st.session_state.third_PERSIST = not st.session_state.third_PERSIST
# def safeSupplyResults():
#   js = 'https://www.streetsafe.supply/results/p/801908'
#   webbrowser.open(js)


# with elements("dashboard"):
#   if st.session_state['first_PERSIST'] == False:
#     layout = [
#           # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
#           dashboard.Item("first_item", 0, 0, 2.75, 2.15),
#           dashboard.Item("second_item", 3, 0, 2.75, 6.15),
#           dashboard.Item("third_item", 6, 0, 2.75, 6.15),
#     ]
#   if st.session_state['second_PERSIST'] == False:
#     layout = [
#           # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
#           dashboard.Item("first_item", 0, 0, 2.75, 6.15),
#           dashboard.Item("second_item", 3, 0, 2.75, 2.15),
#           dashboard.Item("third_item", 6, 0, 2.75, 6.15),
#     ]
#   if st.session_state['third_PERSIST'] == False:
#     layout = [
#           # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
#           dashboard.Item("first_item", 0, 0, 2.75, 6.15),
#           dashboard.Item("second_item", 3, 0, 2.75, 6.15),
#           dashboard.Item("third_item", 6, 0, 2.75, 2.15),
#     ]
#   else:
#     layout = [
#           # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
#           dashboard.Item("first_item", 0, 0, 2.75, 6.15),
#           dashboard.Item("second_item", 3, 0, 2.75, 6.15),
#           dashboard.Item("third_item", 6, 0, 2.75, 6.15),
#     ]

#   with dashboard.Grid(layout):
#     with mui.Paper(key="first_item"):
#       with elements("nested_children3"):
#             with elements("properties"):
#               with elements("style_mui_sx"):
#                 with mui.Paper(elevation=12, variant="outlined", sx={
#                     "padding": "0 1rem 0",
#                     "background-color": "#e39b33",
#                     "text-align": "center",
#                   }):
#                     html.h5("Sample ID: 456789")
#                     with mui.Paper(elevation=12, variant="outlined", sx={
#                                   "padding": ".1rem .5rem",
#                                   "text-align": "left",
#                                   "font-size": ".95rem",
#                                   "background-color": "white"
#                                 }):
#                         with mui.Grid(container=True):
#                               with mui.Grid(item=True, xs=5, sx={"text-align": "left"}):
#                                 html.p("Durham County, NC")
#                                 html.p("Medicaid Region #6")
#                               with mui.Grid(item=True, xs=7, sx={"text-align": "right"}):
#                                 html.p("Aug 1, 2023")
#                         html.hr()
#                         html.h5("Expected Substances")
#                         html.p("heroin")
#                         html.p("fentanyl")
#                         with mui.FormControlLabel(label="Show/Hide Lab Data", control=mui.Checkbox(key=persist('first'), onChange=form_callback)):
#                           html.hr()
#                         html.hr()
#                         if st.session_state['first_PERSIST'] == True:
#                             st.container()
#                             # with mui.Container():
#                               # with mui.Grid(container=True"):
#                                 # with mui.Grid(item=True, xs=3):
#                             mui.Typography("Lab Results")
#                                 # with mui.Grid(item=True, xs=9):
#                                 #   mui.icon.Science()
#                             with mui.Grid(container=True):
#                                 with mui.Grid(item=True, xs=6):
#                                   # mui.icon.VerticalAlignTopRounded()
#                                   html.p("Primary")
#                                   mui.Chip(label="fentanyl", variant="filled")
#                                 with mui.Grid(item=True, xs=6):
#                                   # mui.icon.VerticalAlignBottomRounded()
#                                   html.p("Trace")
#                                   mui.Chip(label="quinine", variant="outlined")
#                                   mui.Chip(label="4-ANPP", variant="outlined")
#                                   mui.Chip(label="lidocaine", variant="outlined")
#                                   mui.Chip(label="ethyl-4-ANPP", variant="outlined")
#                                   mui.Chip(label="phenethyl 4-ANPP", variant="outlined")
#                             html.h5("Description")
#                             html.p("Click a tagged substance to learn more: ")
#                             with mui.Paper(elevation=24, variant="outlined", sx={
#                                 "padding": ".1rem",
#                                 "text-align": "left",
#                                 "font-size": ".95rem",
#                                 "background-color": "lightgray",
#                                 "margin": "0 auto",
#                                 "width": "100%"
#                               }):
#                                 html.p("Fentanyl common potent opioid")
#                             html.hr()
#                             with mui.Paper(elevation=24, variant="outlined", sx={
#                                   "padding": ".25rem",
#                                   "margin": "0 .25rem",
#                                   "font-size": ".95rem",
#                                   "background-color": "lightblue"
#                                 }):
#                               html.h5("Physical Descriptions:")
#                               html.ul([html.li("White"), html.li("Green"), html.li("Crystals; Powder")])
#                             mui.icon.Share()
#                             html.h5("Share this sample's result")
#                             html.hr()
#                             # with mui.Grid(container=True, spacing=4):
#                               # with mui.Grid(item=True, xs=6):
#                             # add space between buttons in the ButtonGroup
#                             with mui.ButtonGroup(fullWidth=True, sx={"width": "100%"}):
#                                 mui.Button("Hide Lab Data", variant="contained", color="info", size="small", sx={"width": "50%", "margin": "10px"}, onClick=form_callback)
#                               # with mui.Grid(item=True, xs=6):
#                                 mui.Button("View More Info", variant="contained", color="info", size="small", sx={"width": "50%",  "margin": "10px", "backgroundColor": "#1E2C4A"}, onClick=safeSupplyResults)
#                                 mui.Collapse(in_=True)
#                         else:
#                           st.echo('')
#     with mui.Paper(key="second_item"):
#       with elements("nested_children3"):
#             with elements("properties"):
#               with elements("style_mui_sx"):
#                 with mui.Paper(elevation=12, variant="outlined", sx={
#                     "padding": "0 1rem 0",
#                     "background-color": "#e39b33",
#                     "text-align": "center",
#                   }):
#                     html.h5("Sample ID: 456789")
#                     with mui.Paper(elevation=12, variant="outlined", sx={
#                                   "padding": ".1rem .5rem",
#                                   "text-align": "left",
#                                   "font-size": ".95rem",
#                                   "background-color": "white"
#                                 }):
#                         with mui.Grid(container=True):
#                               with mui.Grid(item=True, xs=5, sx={"text-align": "left"}):
#                                 html.p("Durham County, NC")
#                                 html.p("Medicaid Region #6")
#                               with mui.Grid(item=True, xs=7, sx={"text-align": "right"}):
#                                 html.p("Aug 1, 2023")
#                         html.hr()
#                         html.h5("Expected Substances")
#                         html.p("heroin")
#                         html.p("fentanyl")
#                         with mui.FormControlLabel(label="Show/Hide Lab Data", control=mui.Checkbox(key=persist('second'), onChange=form_callback2)):
#                           html.hr()
#                         html.hr()
#                         if st.session_state['second_PERSIST'] == True:
#                             st.container()
#                             # with mui.Container():
#                               # with mui.Grid(container=True"):
#                                 # with mui.Grid(item=True, xs=3):
#                             mui.Typography("Lab Results")
#                                 # with mui.Grid(item=True, xs=9):
#                                 #   mui.icon.Science()
#                             with mui.Grid(container=True):
#                                 with mui.Grid(item=True, xs=6):
#                                   # mui.icon.VerticalAlignTopRounded()
#                                   html.p("Primary")
#                                   mui.Chip(label="fentanyl", variant="filled")
#                                 with mui.Grid(item=True, xs=6):
#                                   # mui.icon.VerticalAlignBottomRounded()
#                                   html.p("Trace")
#                                   mui.Chip(label="quinine", variant="outlined")
#                                   mui.Chip(label="4-ANPP", variant="outlined")
#                                   mui.Chip(label="lidocaine", variant="outlined")
#                                   mui.Chip(label="ethyl-4-ANPP", variant="outlined")
#                                   mui.Chip(label="phenethyl 4-ANPP", variant="outlined")
#                             html.h5("Description")
#                             html.p("Click a tagged substance to learn more: ")
#                             with mui.Paper(elevation=24, variant="outlined", sx={
#                                 "padding": ".1rem",
#                                 "text-align": "left",
#                                 "font-size": ".95rem",
#                                 "background-color": "lightgray",
#                                 "margin": "0 auto",
#                                 "width": "100%"
#                               }):
#                                 html.p("Fentanyl common potent opioid")
#                             html.hr()
#                             with mui.Paper(elevation=24, variant="outlined", sx={
#                                   "padding": ".25rem",
#                                   "margin": "0 .25rem",
#                                   "font-size": ".95rem",
#                                   "background-color": "lightblue"
#                                 }):
#                               html.h5("Physical Descriptions:")
#                               html.ul([html.li("White"), html.li("Green"), html.li("Crystals; Powder")])
#                             mui.icon.Share()
#                             html.h5("Share this sample's result")
#                             html.hr()
#                             # with mui.Grid(container=True, spacing=4):
#                               # with mui.Grid(item=True, xs=6):
#                             # add space between buttons in the ButtonGroup
#                             with mui.ButtonGroup(fullWidth=True, sx={"width": "100%"}):
#                                 mui.Button("Hide Lab Data", variant="contained", color="info", size="small", sx={"width": "50%", "margin": "10px"}, onClick=form_callback)
#                               # with mui.Grid(item=True, xs=6):
#                                 mui.Button("View More Info", variant="contained", color="info", size="small", sx={"width": "50%",  "margin": "10px", "backgroundColor": "#1E2C4A"}, onClick=safeSupplyResults)
#                                 mui.Collapse(in_=True)
#                         else:
#                           st.echo('')
#     with mui.Paper(key="third_item"):
#       with elements("nested_children3"):
#             with elements("properties"):
#               with elements("style_mui_sx"):
#                 with mui.Paper(elevation=12, variant="outlined", sx={
#                     "padding": "0 1rem 0",
#                     "background-color": "#e39b33",
#                     "text-align": "center",
#                   }):
#                     html.h5("Sample ID: 456789")
#                     with mui.Paper(elevation=12, variant="outlined", sx={
#                                   "padding": ".1rem .5rem",
#                                   "text-align": "left",
#                                   "font-size": ".95rem",
#                                   "background-color": "white"
#                                 }):
#                         with mui.Grid(container=True):
#                               with mui.Grid(item=True, xs=5, sx={"text-align": "left"}):
#                                 html.p("Durham County, NC")
#                                 html.p("Medicaid Region #6")
#                               with mui.Grid(item=True, xs=7, sx={"text-align": "right"}):
#                                 html.p("Aug 1, 2023")
#                         html.hr()
#                         html.h5("Expected Substances")
#                         html.p("heroin")
#                         html.p("fentanyl")
#                         with mui.FormControlLabel(label="Show/Hide Lab Data", control=mui.Checkbox(key=persist('third'), onChange=form_callback3)):
#                           html.hr()
#                         html.hr()
#                         if st.session_state['third_PERSIST'] == True:
#                             st.container()
#                             # with mui.Container():
#                               # with mui.Grid(container=True"):
#                                 # with mui.Grid(item=True, xs=3):
#                             mui.Typography("Lab Results")
#                                 # with mui.Grid(item=True, xs=9):
#                                 #   mui.icon.Science()
#                             with mui.Grid(container=True):
#                                 with mui.Grid(item=True, xs=6):
#                                   # mui.icon.VerticalAlignTopRounded()
#                                   html.p("Primary")
#                                   mui.Chip(label="fentanyl", variant="filled")
#                                 with mui.Grid(item=True, xs=6):
#                                   # mui.icon.VerticalAlignBottomRounded()
#                                   html.p("Trace")
#                                   mui.Chip(label="quinine", variant="outlined")
#                                   mui.Chip(label="4-ANPP", variant="outlined")
#                                   mui.Chip(label="lidocaine", variant="outlined")
#                                   mui.Chip(label="ethyl-4-ANPP", variant="outlined")
#                                   mui.Chip(label="phenethyl 4-ANPP", variant="outlined")
#                             html.h5("Description")
#                             html.p("Click a tagged substance to learn more: ")
#                             with mui.Paper(elevation=24, variant="outlined", sx={
#                                 "padding": ".1rem",
#                                 "text-align": "left",
#                                 "font-size": ".95rem",
#                                 "background-color": "lightgray",
#                                 "margin": "0 auto",
#                                 "width": "100%"
#                               }):
#                                 html.p("Fentanyl common potent opioid")
#                             html.hr()
#                             with mui.Paper(elevation=24, variant="outlined", sx={
#                                   "padding": ".25rem",
#                                   "margin": "0 .25rem",
#                                   "font-size": ".95rem",
#                                   "background-color": "lightblue"
#                                 }):
#                               html.h5("Physical Descriptions:")
#                               html.ul([html.li("White"), html.li("Green"), html.li("Crystals; Powder")])
#                             mui.icon.Share()
#                             html.h5("Share this sample's result")
#                             html.hr()
#                             # with mui.Grid(container=True, spacing=4):
#                               # with mui.Grid(item=True, xs=6):
#                             # add space between buttons in the ButtonGroup
#                             with mui.ButtonGroup(fullWidth=True, sx={"width": "100%"}):
#                                 mui.Button("Hide Lab Data", variant="contained", color="info", size="small", sx={"width": "50%", "margin": "10px"}, onClick=form_callback)
#                               # with mui.Grid(item=True, xs=6):
#                                 mui.Button("View More Info", variant="contained", color="info", size="small", sx={"width": "50%",  "margin": "10px", "backgroundColor": "#1E2C4A"}, onClick=safeSupplyResults)
#                                 mui.Collapse(in_=True)
#                         else:
#                           st.echo('')

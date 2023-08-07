from load_init import local_css, create_sidebar, convert_df
from streamlit_elements import elements, mui, html, dashboard
import streamlit as st
st.set_page_config(
    page_title="NC Psychedelics & Others",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
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


create_sidebar()
st.markdown("# Psychedelics and Other Drugs in NC")
st.write("We are watching a number of different kinds of psychedelics and other drugs in North Carolina right now....")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Samples", value=nc_sample_count_int)
with col2:
    st.metric(label="Programs & Clinics", value=nc_program_count_int)
with col3:
    st.metric(label="Counties", value=nc_countycount_int)
with col4:
    label_="Psychedelics & Others"
    st.metric(label=label_, value=nc_psychedelics_et_al_count)
with st.expander("View raw data table", ):
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
      list_length_divided_by_three = math.ceil(list_length / 3)
      first_column_items = items[:list_length_divided_by_three]
      second_column_items = items[list_length_divided_by_three:list_length_divided_by_three * 2]
      third_column_items = items[list_length_divided_by_three * 2:]
      #  fill each col with corresponding list
      if list_length == 0:
        st.write("No items found")
      else :
        with col1:
          for index, row in first_column_items.iterrows():
            substance = row['substance']
            latest_detected = row['total']
            st.metric(label=substance, value=latest_detected, help=substance)
        with col2:
          for index, row in second_column_items.iterrows():
            substance = row['substance']
            latest_detected = row['total']
            st.metric(label=substance, value=latest_detected, help=substance)
        with col3:
          for index, row in third_column_items.iterrows():
            substance = row['substance']
            latest_detected = row['total']
            st.metric(label=substance, value=latest_detected, help=substance)
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['LSD','MDMA', 'Synthetic Cannabinoids', 'Substituted Cathinones', 'Nitazines', 'Other'])
with tab1:
    # filter the df to remove any entries that are not included in the lsd_list
    filtered_df = df[df['substance'].isin(lsd_list)]
    st.markdown("### D  rugs commonly sold as LSD")
    st.markdown("*2-3 sentence description.")
    generate_container_with_rows(filtered_df)
with tab2:
    filtered_df = df[df['substance'].isin(mdma_list)]
    st.markdown("### Drugs commonly sold as MDMA")
    st.markdown("*(dimethylpentylone, MDA + other methylated amphetamines besides MDMA)*")
    generate_container_with_rows(filtered_df)
with tab3:
    filtered_df = df[df['substance'].isin(syncan_list)]
    st.markdown("### Substances found with Synthetic Cannabinoids")
    st.markdown('These are commonly sold as "K2" or "spice" in North Carolina.')
    generate_container_with_rows(filtered_df)
with tab4:
    filtered_df = df[df['substance'].isin(subcath_list)]
    st.markdown("### Substances known as Substituted Cathinones")
    st.markdown("2-3 sentence description.")
    generate_container_with_rows(filtered_df)
with tab5:
    filtered_df = df[df['substance'].isin(nitaz_list)]
    st.markdown("### Emergening Nitazines")
    st.markdown("2-3 sentence description.")
    generate_container_with_rows(filtered_df)
with tab6:
    filtered_df = df[df['substance'].isin(other_list)]
    st.markdown("### Other Emerging Drugs/Substances"   )
    st.markdown("2-3 sentence description.")
    generate_container_with_rows(filtered_df)

#  LSD (do we have enough?)
# Ketamime
# Synthetic cannabinoids
# Substituted cathinones
st.markdown("---")

with st.container():
    st.subheader("Does this represent the entire NC Drug Supply?")
    st.write("We have analyzed a limited number of these drugs. People may send us samples because the drugs caused unexpected effects. Our data don't represent the entire drug supply in North Carolina.")
    st.expander("View raw data table", )
    # drop all columns except sample_id and substance from the df
    lab_detail = lab_detail.drop(columns=[col for col in lab_detail.columns if col not in ['substance', 'sampleid', 'date_complete']])
    nc_psychedelics_et_al_cpy = nc_psychedelics_et_al_cpy.drop(columns=['latest_detected'])
    merged_df = pd.merge(nc_psychedelics_et_al_cpy, lab_detail, on='substance')
    # sort the merged_df by sampleid greatest to least then set the col type to Category
    merged_df = merged_df.sort_values(by=['sampleid'], ascending=False)
    merged_df['sampleid'] = merged_df['sampleid'].astype('category')
    merged_df['date_complete'] = pd.to_datetime(merged_df['date_complete'])

    # st.dataframe(
    #     merged_df,
    #     height=350,
    # )

    # Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(merged_df)

    #customize gridOptions
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
    gb.configure_column("date_complete", type=["dateColumnFilter","customDateTimeFormat"], pivot=True)
    fit_columns_on_grid_load = True
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    gb.configure_grid_options(domLayout='single')
    gb.configure_grid_options(
        enableCellTextSelection=True,
        ensureDomOrder=True,
    )
    gridOptions = gb.build()
    # generate js code to use cell content as link to pubchem site
    LinkCellRenderer_pubchem = JsCode('''
      class LinkCellRenderer {
          init(params) {
              this.params = params;
              this.eGui = document.createElement('div');
              this.eGui.innerHTML = `
              <span>
                  <a id='click-button'
                      class='btn-simple'
                      href='https://pubchem.ncbi.nlm.nih.gov/compound/${this.params.getValue()}'
                      target='_blank'
                      style='color: ${this.params.color};}'>${this.params.getValue()}</a>
              </span>
            `;

              this.eButton = this.eGui.querySelector('#click-button');

              this.btnClickedHandler = this.btnClickedHandler.bind(this);
              this.eButton.addEventListener('click', this.btnClickedHandler);

          }

          getGui() {
              return this.eGui;
          }

          refresh() {
              return true;
          }

          destroy() {
              if (this.eButton) {
                  this.eGui.removeEventListener('click', this.btnClickedHandler);
              }
          }

          btnClickedHandler(event) {

                      this.refreshTable('clicked');
              }

          refreshTable(value) {
              this.params.setValue(value);
          }
      };
    ''')
    # generate js code to use cell content as link to streetsafe.supply result page
    LinkCellRenderer = JsCode('''
      class LinkCellRenderer {
          init(params) {
              this.params = params;
              this.eGui = document.createElement('div');
              this.eGui.innerHTML = `
              <span>
                  <a id='click-button'
                      class='btn-simple'
                      href='https://www.streetsafe.supply/results/p/${this.params.getValue()}'
                      target='_blank'
                      style='color: ${this.params.color};}'>${this.params.getValue()}</a>
              </span>
            `;

              this.eButton = this.eGui.querySelector('#click-button');

              this.btnClickedHandler = this.btnClickedHandler.bind(this);
              this.eButton.addEventListener('click', this.btnClickedHandler);

          }

          getGui() {
              return this.eGui;
          }

          refresh() {
              return true;
          }

          destroy() {
              if (this.eButton) {
                  this.eGui.removeEventListener('click', this.btnClickedHandler);
              }
          }

          btnClickedHandler(event) {

                      this.refreshTable('clicked');
              }

          refreshTable(value) {
              this.params.setValue(value);
          }
      };
    ''')

    gridOptions['columnDefs'] = [
        {
        "field": "sampleid",
        "headerName": "Sample Ids",
        "cellRenderer": LinkCellRenderer,
        "cellRendererParams": {
          "color": "blue",
          "data": "sampleid",
        },
        "maxWidth": 120,
      },
      {
        "field": "substance",
        "headerName": "Substance",
        "maxWidth": 120,
      },
      {
        "field": "pubchemcid",
        "headerName": "PubChem CID",
        "cellRenderer":LinkCellRenderer_pubchem,
        "cellRendererParams": {
          "color": "green",
          "data": "pubchemcid"
        },
        "maxWidth": 120,
      },
      {
        "field": "total",
        "headerName": "total",
        "maxWidth": 120,
      },
      {
        "field": "date_complete",
        "headerName": "Sample Collection Date",
        "type": ["dateColumnFilter","customDateTimeFormat"],
        "custom_format_string":"yyyy-MM-dd",
        "pivot": True,
        "maxWidth": 200,
      },
    ]
    with st.container():
        custom_css = {
          ".ag-root-wrapper": {
            "max-width": "650px !important",
            "margin": "0 auto",
            },
        }
        grid_response = AgGrid(
            merged_df,
            custom_css=custom_css,
            gridOptions=gridOptions,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=False
            )



        csv = convert_df(df)

        st.download_button(
          "Download csv",
          csv,
          "file.csv",
          "text/csv",
          key='download-csv'
        )
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

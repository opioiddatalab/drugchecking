import streamlit as st
import webbrowser
import re
import pandas as pd
import math
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def button_as_page_link(url):
  webbrowser.open(url)

def create_sidebar():
    pages = {
      "Home": "https://ncdrugchecking.streamlit.app/",
      "NC Xylazine": "https://ncxylazine.streamlit.app/",
      "NC Overdoses": "https://ncoverdoses.streamlit.app/",
      "NC Stimulants": "https://ncstimulants.streamlit.app/",
      "NC Drug Market": "https://ncdrugmarket.streamlit.app/",
      "NC Psychedelics & Others": "https://ncpsychedelics.streamlit.app/",
      "Get Help": "https://www.streetsafe.supply/contact",
    }
    with st.sidebar:
    # map over the pages dict and return a button for each page
    # the button should have the page name as the label and the url as the param for the button_as_page_link function in the on_click param
     for page in pages:
        # create a markdown string that is an anchor tag with the url as the href value and the page name as the text
        # the anchor tag should open in a new tab
        html= "<a class='click-button' class='btn-simple' href="+pages[page]+" target='_blank'>"+page+"</a>"
        st.markdown(html, unsafe_allow_html=True)

def convert_df(df):
  return df.to_csv(index=False).encode('utf-8')

county_groups = {
     "Cherokee": 1,
     "Graham": 1,
     "Clay": 1,
     "Macon": 1,
     "Jackson": 1,
     "Swain": 1,
     "Haywood": 1,
      "Madison": 1,
      "Buncombe": 1,
      "Henderson": 1,
      "Transylvania": 1,
      "Polk": 1,
      "Rutherford": 1,
      "McDowell": 1,
      "Yancey": 1,
      "Mitchell": 1,
      "Avery": 1,
      "Burke": 1,
      "Caldwell": 1,
         "Watauga":2,
    "Ashe":2,
    "Alleghany":2,
    "Wilkes":2,
    "Yadkin":2,
    "Surry":2,
    "Stokes":2,
    "Forsyth":2,
    "Davie":2,
    "Davidson":2,
    "Rockingham":2,
    "Guilford":2,
    "Randolph":2,
    "Cleveland": 3,
    "Lincoln": 3,
    "Gaston": 3,
    "Mecklenburg": 3,
    "Catawba": 3,
    "Cabarrus": 3,
    "Union": 3,
    "Stanly": 3,
    "Anson": 3,
    "Alexander": 3,
    "Iredell": 3,
    "Rowan": 3,
    "Caswell": 4,
    "Person": 4,
    "Granville": 4,
    "Vance": 4,
    "Warren": 4,
    "Franklin": 4,
    "Wake": 4,
    "Durham": 4,
    "Orange": 4,
    "Chatham": 4,
    "Alamance": 4,
    "Wilson": 4,
    "Johnston": 4,
    "Nash": 4,
    "Montgomery": 5,
    "Moore": 5,
    "Richmond": 5,
    "Scotland": 5,
    "Hoke": 5,
    "Robeson": 5,
    "Cumberland": 5,
    "Bladen": 5,
    "Sampson": 5,
    "Pender": 5,
    "Lee": 5,
    "Harnett": 5,
    "Cumberland": 5,
    "New Hanover": 5,
    "Brunswick": 5,
    "Onslow": 6,
    "Duplin": 6,
    "Wayne": 6,
    "Greene": 6,
    "Lenoir": 6,
    "Jones": 6,
    "Pitt": 6,
    "Beaufort": 6,
    "Craven": 6,
    "Pamlico": 6,
    "Carteret": 6,
    "Hyde": 6,
    "Tyrrell": 6,
    "Washington": 6,
    "Martin": 6,
    "Bertie": 6,
    "Dare": 6,
    "Currituck": 6,
    "Camden": 6,
    "Pasquotank": 6,
    "Perquimans": 6,
    "Chowan": 6,
    "Gates": 6,
    "Halifax": 6,
    "Northampton": 6,
    "Hertford": 6,
     "Cherokee County": 1,
     "Graham County": 1,
     "Clay County": 1,
     "Macon County": 1,
     "Jackson County": 1,
     "Swain County": 1,
     "Haywood County": 1,
      "Madison County": 1,
      "Buncombe County": 1,
      "Henderson County": 1,
      "Transylvania County": 1,
      "Polk County": 1,
      "Rutherford County": 1,
      "McDowell County": 1,
      "Yancey County": 1,
      "Mitchell County": 1,
      "Avery County": 1,
      "Burke County": 1,
      "Caldwell County": 1,
         "Watauga County": 2,
    "Ashe County": 2,
    "Alleghany County": 2,
    "Wilkes County": 2,
    "Yadkin County": 2,
    "Surry County": 2,
    "Stokes County": 2,
    "Forsyth County": 2,
    "Davie County": 2,
    "Davidson County": 2,
    "Rockingham County": 2,
    "Guilford County": 2,
    "Randolph County": 2,
    "Cleveland County": 3,
    "Lincoln County": 3,
    "Gaston County": 3,
    "Catawba County": 3,
    "Mecklenburg County": 3,
    "Cabarrus County": 3,
    "Union County": 3,
    "Stanly County": 3,
    "Anson County": 3,
    "Alexander County": 3,
    "Iredell County": 3,
    "Rowan County": 3,
    "Caswell County": 4,
    "Person County": 4,
    "Granville County": 4,
    "Vance County": 4,
    "Warren County": 4,
    "Franklin County": 4,
    "Wake County": 4,
    "Durham County": 4,
    "Orange County": 4,
    "Chatham County": 4,
    "Alamance County": 4,
    "Wilson County": 4,
    "Johnston County": 4,
    "Nash County": 4,
    "Montgomery County": 5,
    "Moore County": 5,
    "Richmond County": 5,
    "Scotland County": 5,
    "Hoke County": 5,
    "Robeson County": 5,
    "Cumberland County": 5,
    "Bladen County": 5,
    "Sampson County": 5,
    "Pender County": 5,
    "Lee County": 5,
    "Harnett County": 5,
    "Cumberland County": 5,
    "New Hanover County": 5,
    "Brunswick County": 5,
    "Onslow County": 6,
    "Duplin County": 6,
    "Wayne County": 6,
    "Greene County": 6,
    "Lenoir County": 6,
    "Jones County": 6,
    "Pitt County": 6,
    "Beaufort County": 6,
    "Craven County": 6,
    "Pamlico County": 6,
    "Carteret County": 6,
    "Hyde County": 6,
    "Tyrrell County": 6,
    "Washington County": 6,
    "Martin County": 6,
    "Bertie County": 6,
    "Dare County": 6,
    "Currituck County": 6,
    "Camden County": 6,
    "Pasquotank County": 6,
    "Perquimans County": 6,
    "Chowan County": 6,
    "Gates County": 6,
    "Halifax County": 6,
    "Northampton County": 6,
    "Hertford County": 6,
}
# remove any duplicates from county_groups dict
county_groups = {k: v for k, v in county_groups.items() if v is not None}

def add_county_group(county):
  return county_groups.get(county, None)

def get_nc_analysis_ds():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_analysis_dataset.csv"
    return pd.read_csv(url)
def get_nc_lab_detail_ds():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_lab_detail.csv"
    return pd.read_csv(url)
def get_nc_merged_df(substance_list):
  nc_lab_detail = get_nc_lab_detail_ds()
  nc_analysis = get_nc_analysis_ds()
  df = pd.merge(nc_lab_detail, nc_analysis, on='sampleid')
  df = df[['sampleid',  'substance', 'county', 'date_collect', 'expectedsubstance', 'lab_meth_any_y', 'lab_cocaine_any_y', 'crystals', 'lab_fentanyl_y' ]]
  return df[df['substance'].isin(substance_list)]

def get_nc_intro_metrics(metrics, count, sub_list, df_2):
   col1, col2, col3, col4 = st.columns(4)
   with col1:
    label = list(metrics.keys())[0]
    value = list(metrics.values())[0]
    st.metric(label=label, value=value)
   with col2:
    label = list(metrics.keys())[1]
    value = list(metrics.values())[1]
    st.metric(label=label, value=value)
   with col3:
    label = list(metrics.keys())[2]
    value = list(metrics.values())[2]
    st.metric(label=label, value=value)
   with col4:
        #  count the number of unique sampleids in the nc_main_dataset
        label_="Stimulant Samples"
        st.metric(label=label_, value=count)
   for s_ in sub_list:
      # check to see if s_ is in the df_2
      if s_ in df_2.index:
        latest = df_2.loc[s_]['latest_detected']
        text = "<div style='display: flex; flex-direction: row; align-items: center; justify-content: space-between;'><p>Most recent detection of "+s_+": </p><p>"+latest+"</p></div>"
        st.markdown(text, unsafe_allow_html=True)

def get_nc_county_count():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_countycount.csv"
    df = pd.read_csv(url)
    return df.iloc[0]['nc_countycount']

def get_nc_program_count():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_prorgams.csv"
    df = pd.read_csv(url)
    return df.iloc[0]['nc_programs']


def get_nc_sample_count():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_samples.csv"
    df = pd.read_csv(url)
    return df.iloc[0]['nc_samples']

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
            # check to see if the substance column exists
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

def generate_adulterant_df(items):
    return st.dataframe(items,
                     use_container_width=True,
                     column_config={
                        'substance': st.column_config.TextColumn(
                          "Substance",
                          width='medium'
                        ),
                        'total': st.column_config.NumberColumn(
                          "Count",
                          width='medium'
                        ),
                        'latest_detected': st.column_config.DateColumn(
                          "Most Recent Sample Date",
                          format="dddd MMMM DD, YYYY",
                        ),
                        'pubchemcid': None,
                        'primary': None,
                        'trace': None,
                      },
                     hide_index=True,
                  )
def generate_drug_supply_table(df):
   with st.container():
    st.subheader("Does this represent the entire NC drug supply?")
    st.write("We have analyzed a limited number of these drugs. People may send us samples because the drugs caused unexpected effects. Our data don't represent the entire drug supply in North Carolina.")
    st.expander("View raw data table", )

    merged_df = get_nc_merged_df(df)

    merged_df = merged_df.sort_values(by=['sampleid'], ascending=False)
    merged_df['sampleid'] = merged_df['sampleid'].astype('category')
    merged_df['date_collect'] = pd.to_datetime(merged_df['date_collect'], format='mixed')
    gb = GridOptionsBuilder.from_dataframe(merged_df)

    #customize gridOptions
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
    gb.configure_column("date_collect", type=["dateColumnFilter","customDateTimeFormat"], pivot=True)
    fit_columns_on_grid_load = True
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    gb.configure_grid_options(domLayout='single')
    gb.configure_grid_options(
        enableCellTextSelection=True,
        ensureDomOrder=True,
    )
    # sort the df by the date_collect col with most recent first
    merged_df = merged_df.sort_values(by=['date_collect'], ascending=False)
    gridOptions = gb.build()
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
  # ADD IN COUNTY COLUMN + EXPECTED SUBSTANCE (VERBATIM FROM COL) COL + TEXTURE/COLOR COLS + COUNTY REGION COL
  # LINK TO COUUNTY REGION MAP

    gridOptions['columnDefs'] = [
        {
        "field": "sampleid",
        "headerName": "Sample IDS",
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
         "field": "county",
         "headerName": "County",
      },
      {
        "field": "date_collect",
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



        csv = convert_df(merged_df)

        st.download_button(
          "Download csv",
          csv,
          "file.csv",
          "text/csv",
          key='download-csv'
        )


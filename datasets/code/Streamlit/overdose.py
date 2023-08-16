from load_init import local_css, create_sidebar, convert_df, display_funding, generate_filtering_tips, generate_substance_od_table, generate_container_with_rows, pull_top_od_subs
import streamlit as st
st.set_page_config(
    page_title="NC Overdoses",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
)
local_css("datasets/code/Streamlit/style.css")
local_css("datasets/code/Streamlit/pages/overdose.css")
import pandas as pd
import numpy as np
import altair as alt
from st_aggrid import GridOptionsBuilder, AgGrid, JsCode
from PIL import Image


def get_nc_od_color():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_od_color.csv"
    return pd.read_csv(url)
nc_od_color = get_nc_od_color()
nc_od_color_df = pd.DataFrame(nc_od_color)
nc_od_color_df['date_collect'] = pd.to_datetime(nc_od_color_df['date_collect'])
create_sidebar()
# create a title for the app
st.title('Overdoses in NC')
st.markdown("---")
nc_od_count = len(nc_od_color_df.index)


with st.container():
  st.subheader("View Overdoses by County", anchor="county", help=None)
data_url = "https://raw.githubusercontent.com/mcnakhaee/palmerpenguins/master/palmerpenguins/data/penguins.csv"

LinkCellRenderer = JsCode('''
  class LinkCellRenderer {
      init(params) {
          this.params = params;
          this.eGui = document.createElement('div');
          this.eGui.innerHTML = `
          <span>
              <a id='click-button'
                  class='btn-simple'
                  href='https://streetsafe.supply/results/p/${this.params.getValue()}'
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

# Infer basic colDefs from dataframe types
gb = GridOptionsBuilder.from_dataframe(nc_od_color_df)

#customize gridOptions
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)
gb.configure_column("date_collect", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd', pivot=True)

gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
fit_columns_on_grid_load = True
gb.configure_grid_options(domLayout='normal')
gridOptions = gb.build()

#Display the grid

gridOptions['columnDefs'] = [
    #  rename the sampleid column to Sample ID
    {
    "field": "sampleid",
    "headerName": "ID",
    "cellRenderer": LinkCellRenderer,
    "cellRendererParams": {
      "color": "blue",
      "data": "sampleid"
    },
    "maxWidth": 90,
  },
  {
    "field": "date_collect",
    "headerName": "Date Collected",
    "type": ["dateColumnFilter","customDateTimeFormat"],
    "custom_format_string": "MM-dd-yyyy",
    "pivot": True,
    "maxWidth": 120,
  },
  {
    "field": "county",
    "headerName": "County"
  },
  {
    "field": "color",
    "headerName": "Color"
  },
  {
    "field": "texture",
    "headerName": "Textures"
  }
]
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

st.write("We monitor a number of different drugs and new psychoactive substances (NPS) in North Carolina right now....")
col1, col2, col3, col4 = st.columns(4)
st.markdown(
    """
    <style>
        div[data-testid="metric-container"] div[data-testid="stMetricValue"]
        {
            text-align: center !important;
        }
    </style>
    """,unsafe_allow_html=True
)
with col1:
    st.metric(label="Samples", value=nc_sample_count_int)
with col2:
    st.metric(label="Programs & Clinics", value=nc_program_count_int)
with col3:
    st.metric(label="Counties", value=nc_countycount_int)
with col4:
    label_="Samples involved in OD"
    st.metric(label=label_, value=nc_od_count)
with st.expander("View raw data table", ):
  with st.container():
    generate_filtering_tips()
    grid_response = AgGrid(
        nc_od_color_df,
        gridOptions=gridOptions,
        width='100%',
        fit_columns_on_grid_load=fit_columns_on_grid_load,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        enable_enterprise_modules=False
        )
    csv = convert_df(nc_od_color_df)

    st.download_button(
            "Download csv",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
          )

st.markdown("---")
st.header("Top 15 substances involved in overdoses")

generate_container_with_rows(pull_top_od_subs())

with st.expander("View all substances involved in overdoses", expanded=False):
  generate_substance_od_table()

st.header("Naloxone in NC and the US")
tab1, tab2, tab3 = st.tabs(['What is Naloxone?', 'How to Get Naloxone in NC', 'More naloxone resources'])
with tab1:
  st.markdown(
    """
    <style>
        div[data-testid="column"]
        {
            text-align: left !important;
        }
    </style>
    """,unsafe_allow_html=True
)
  col1, col2 = st.columns(2)
  with col1:
    st.write('Naloxone is a “rescue” drug that quickly and safely reverses opioid overdose. It is available as an injectable solution and as a nasal spray. Naloxone works by blocking the effects of opioids in the body. Virtually all opioid overdose deaths are preventable if naloxone is administered in time.')
    st.write('All states but one (Nebraska) allow pharmacists to prescribe or dispense naloxone to anyone.')
  with col2:
    st.write('A person who has overdosed cannot administer naloxone to themselves — it must be administered by someone else nearby. The most effective way to prevent fatal opioid overdose with naloxone is to prioritize naloxone distribution to people who use drugs (for example, through harm reduction and syringe services programs) as this group is the most likely to witness an overdose.')
  col1, col2 = st.columns(2)
  with col1:
    nalox_img = Image.open('datasets/code/Streamlit/images/naloxone.png')
    st.image(nalox_img, width=600)
with tab2:
  outerCol1, outerCol2 = st.columns(2)
  with outerCol1:
        # make sure the text is left aligned
        text1 = "<div style='text-align: left'>Naloxone is available under the statewide standing order through participating pharmacies. It is up to each individual pharmacy to decide whether to dispense naloxone under the statewide standing order or under a separate standing order. You can contact your local pharmacy to determine whether it is currently dispensing naloxone under a standing order.</div><br/>"
        st.markdown(text1, unsafe_allow_html=True)
  with outerCol2:
        st.markdown("""
                    <ul>
                      <li style='text-align: left'><a href="https://www.ncdhhs.gov/divisions/public-health/north-carolina-safer-syringe-initiative/syringe-services-program-north-carolina">NC Syringe Exchange Programs</a></li>
                      <li style='text-align: left'><a href="https://naloxonesaves.org/2019/02/13/n-c-pharmacies-that-offer-naloxone-under-a-standing-order">Naloxone Saves - NC Pharmacy Locations</a></li>
                      <li style='text-align: left'><a href="https://naloxonesaves.org/naloxone-available-through-syringe-exchange-programs">Syringe services programs that offer naloxone</a></li>
                      <li style='text-align: left'><a href="https://naloxonesaves.org/where-can-i-get-naloxone/north-carolina-health-departments-that-offer-naloxone">NC health departments that offer naloxone</a></li>
                      <li style='text-align: left'><a href="https://naloxonesaves.org/north-carolina-pharmacies-that-offer-naloxone">North Carolina pharmacies that offer naloxone</a></li>
                      <li style='text-align: left'>Talk to your medical care provider about getting naloxone"</li>
                    </ul>
                    """, unsafe_allow_html=True)
  text2 = "<div style='text-align: left'>If you are not able to obtain naloxone through a standing order at a pharmacy, you have other options to obtain naloxone. You may seek a prescription for naloxone from a health care provider. You may also get naloxone at some local health departments or syringe exchange programs. Use the above links to find a syringe exchange program in your area or a participating local health department.</div>"
  st.markdown(text2, unsafe_allow_html=True)


with tab3:
    st.markdown("### Resources for support on Technical Assistance or for scaling up Naloxone to reverse opioid overdoses in your county:")
    st.markdown("* [Remedy Alliance for the People](https://remedyallianceftp.org/) is a non-profit organization that negotiates with pharmaceutical companies for lower prices on generic injectable naloxone. Remedy Alliance also offers technical assistance for establishing and scaling up a naloxone distribution program. Technical assistance may be requested directly through their website.")
    st.markdown("* [The NHRTAC](https://harmreductionhelp.cdc.gov/s/) was established by the U.S. Centers for Disease Control and Prevention and the U.S. Substance Abuse and Mental Health Services Administration to provide free assistance to those implementing harm reduction services in their community. Technical assistance for implementing naloxone distribution programs may be requested through the NHRTAC website.")
    st.markdown("* [NASTAD](https://nastad.org/issues/syringe-services-programs) provides technical assistance for the implementation of naloxone distribution programs to health departments and community-based organizations. They also provide regional harm reduction support through a network of professional consultants working across the United States.")


st.markdown("---")
display_funding()
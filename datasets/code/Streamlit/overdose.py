from load_init import local_css
import streamlit as st
st.set_page_config(
    page_title="NC Overdoses",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
)
local_css("datasets/code/Streamlit/style.css")
import pandas as pd
import numpy as np
import altair as alt
from itertools import cycle
import streamlit.components.v1 as components
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode


def get_nc_od_color():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_od_color.csv"
    return pd.read_csv(url)
nc_od_color = get_nc_od_color()
nc_od_color_df = pd.DataFrame(nc_od_color)
nc_od_color_df['date_collect'] = pd.to_datetime(nc_od_color_df['date_collect'])

# create a title for the app
st.title('Overdoses in NC')
st.markdown("---")


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
    "field": "texture",
    "headerName": "Textures"
  }
]
grid_response = AgGrid(
    nc_od_color_df,
    gridOptions=gridOptions,
    width='100%',
    fit_columns_on_grid_load=fit_columns_on_grid_load,
    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
    enable_enterprise_modules=False
    )
df = grid_response['data']
selected = grid_response['selected_rows']
selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')


outerCol1, outerCol2 = st.columns(2)
with outerCol1:
        st.header("How to Get Naloxone in NC")
        # make sure the text is left aligned
        text1 = "<div style='text-align: left'>Naloxone is available under the statewide standing order through participating pharmacies. It is up to each individual pharmacy to decide whether to dispense naloxone under the statewide standing order or under a separate standing order. You can contact your local pharmacy to determine whether it is currently dispensing naloxone under a standing order.</div><br/>"
        st.markdown(text1, unsafe_allow_html=True)
        text2 = "<div style='text-align: left'>If you are not able to obtain naloxone through a standing order at a pharmacy, you have other options to obtain naloxone. You may seek a prescription for naloxone from a health care provider. You may also get naloxone at some local health departments or syringe exchange programs. See links below to find a syringe exchange program in your area or a participating local health department.</div>"
        st.markdown(text2, unsafe_allow_html=True)



with outerCol2:
        st.markdown("<br/><br/>", unsafe_allow_html=True)
        st.markdown("""
                    <ul>
                      <li style='text-align: left'><a href="https://www.ncdhhs.gov/divisions/public-health/north-carolina-safer-syringe-initiative/syringe-services-program-north-carolina">NC Syringe Exchange Programs</a></li>
                      <li style='text-align: left'><a href="https://naloxonesaves.org/2019/02/13/n-c-pharmacies-that-offer-naloxone-under-a-standing-order">Naloxone Saves - NC Pharmacy Locations</a></li>
                      <li style='text-align: left'><a href="https://naloxonesaves.org/naloxone-available-through-syringe-exchange-programs">Syringe services programs that offer naloxone</a></li>
                      <li style='text-align: left'><a href="https://naloxonesaves.org/where-can-i-get-naloxone/north-carolina-health-departments-that-offer-naloxone">NC health departments that offer naloxone</a></li>
                      <li style='text-align: left'><a href="https://naloxonesaves.org/north-carolina-pharmacies-that-offer-naloxone">North Carolina pharmacies that offer naloxone</a></li>
                      <li style='text-align: left'>Talk to your medical care provider about getting naloxone")</li>
                    </ul>
                    """, unsafe_allow_html=True)

st.markdown("---")
body = "this is a container for the data"

with st.container():
    st.subheader(body, anchor="data", help=None)
    st.write("Information about Overdoses in general")

    col1, col2, col3 = st.columns(3)
    col1.metric("Pill/Powder Reported ODs w/ our Drug Checking", "70% of samples", "-1", "normal", help="this is a help string")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    st.write("comparing opioid and stimulant overdoses in a bar chart")
    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

    st.bar_chart(chart_data)


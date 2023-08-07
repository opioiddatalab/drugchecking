from load_init import local_css, create_sidebar, convert_df
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="NC Stimulants",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
)

local_css("datasets/code/Streamlit/style.css")
local_css("datasets/code/Streamlit/pages/stimulants.css")
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
nc_stimulants = get_nc_ds_substances()
nc_stimulants_j = get_nc_ds_substances_json()
# map over the latest_detected col and convert to human readable date
nc_stimulants['latest_detected'] = pd.to_datetime(nc_stimulants['latest_detected'], format='%d%b%Y').dt.strftime('%B %d, %Y')

nc_stimulants = pd.DataFrame(nc_stimulants)

# set the index to the substance col

nc_stimulants.set_index('substance', inplace=True)
# sort the df by the latest_detected col
nc_stimulants.sort_values(by=['latest_detected'], inplace=True, ascending=False)
# convert the latest_detected col to a human readable date
nc_stimulants['latest_detected'] = pd.to_datetime(nc_stimulants['latest_detected']).dt.strftime('%B %d, %Y')
nc_stimulants_list =[
  "methamphetamine",
  "cocaine"
]
# map of the nc_psychedelics_et_al df and remove any rows where the substance is not in the nc_psychedelics_et_all_list
nc_stimulants = nc_stimulants[nc_stimulants.index.isin(nc_stimulants_list)]
nc_stimulants_cpy = nc_stimulants
nc_stimulants_count = len(nc_stimulants.index)

nc_stimulants = nc_stimulants.drop('pubchemcid', axis=1)
nc_stimulants = nc_stimulants.drop('primary', axis=1)
nc_stimulants = nc_stimulants.drop('trace', axis=1)


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
st.markdown("# Stimulants in NC")
html_str = f"""
<p>Currently in North Carolina, the primary stimulants found in street drugs are methamphetamine and cocaine. These can be in crystal (crystal meth or crack) or in powder form. Methamphetamine and amphetamine can <a href="https://ncpsychedelics.streamlit.app/" _target="blank">also be found in</a> in MDMA (aka Ecstasy, molly). Stimulants may also show up pre-mixed with fentanyl in "speedballs."'</p>
"""
st.markdown(html_str, unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Samples", value=nc_sample_count_int)
with col2:
    st.metric(label="Programs & Clinics", value=nc_program_count_int)
with col3:
    st.metric(label="Counties", value=nc_countycount_int)
with col4:
    label_="Stimulants Count"
    st.metric(label=label_, value=nc_stimulants_count)
with st.expander("View raw data table", ):
  st.dataframe(
        nc_stimulants,
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

def build_dict_from_json(json_obj):
    # convert the json obj to a df
    df = pd.read_json(json_obj)
    # set the index to the substance col
    df.set_index('substance', inplace=False)
    # sort the df by the latest_detected col
    return df.to_dict('records')

df = build_dict_from_json(nc_stimulants_j)
# add an index int col to the df
df = pd.DataFrame(df)
df['index'] = df.index
# set the index to the index col
df.set_index('index', inplace=True)
st.subheader("View substances by category")
with st.container():
    # filter the df to remove any entries that are not included in the lsd_list
    filtered_df = df[df['substance'].isin(nc_stimulants_list)]
    st.markdown("### Common Stimulants in Drug Supply")
    st.markdown("*2-3 sentence description.")
    generate_container_with_rows(filtered_df)
st.markdown("---")

with st.container():
    st.subheader("Does this represent the entire NC Drug Supply?")
    st.write("We have analyzed a limited number of these drugs. People may send us samples because the drugs caused unexpected effects. Our data don't represent the entire drug supply in North Carolina.")
    st.expander("View raw data table", )

    lab_detail = lab_detail.drop(columns=[col for col in lab_detail.columns if col not in ['substance', 'sampleid', 'date_complete']])
    nc_stimulants_cpy = nc_stimulants_cpy.drop(columns=['latest_detected'])
    merged_df = pd.merge(nc_stimulants_cpy, lab_detail, on='substance')

    merged_df = merged_df.sort_values(by=['sampleid'], ascending=False)
    merged_df['sampleid'] = merged_df['sampleid'].astype('category')
    merged_df['date_complete'] = pd.to_datetime(merged_df['date_complete'])

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
st.markdown("## Fentanyl in Stimulants in NC")
st.write("There is concern that fentanyl is showing up in stimulants. We find fentanyl in crystal meth or crack rarely. However, fentanyl occurs more frequently in powder forms of cocaine and methamphetamine.")
stimulant_substance_list = [
   "powder meth",
  "crystal meth",
  "powder coke",
  "crack"
]
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Powder meth", value="coming soon")
    st.write('Crystal meth: substance=="methamphetamine" & texture!=(regexm, "crystal")')

with col2:
    st.metric(label="Crystal Meth", value="coming soon")
    st.write('Crystal meth: substance=="methamphetamine" & texture==(regexm, "crystal")')
with col3:
    st.metric(label="Powder coke", value="coming soon")
    st.write('Powder cocaine: substance=="cocaine" & expectedsubstance!="crack"')
with col4:
    st.metric(label="Crack", value="coming soon")
    st.write('Crack: expectedsubstance=="crack')
with st.expander("View raw data table", ):
  st.dataframe(
        nc_stimulants,
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

st.markdown("This doesn't mean that crack is impervious to fentanyl, [as in this case](https://www.justice.gov/usao-ednc/pr/drug-dealer-who-sold-fentanyl-laced-crack-sentenced-more-16-years-after-four-people). Also, keep in mind that people may send us samples because they caused unexpected effects, so these percents may be higher than in the normal drug supply.")
st.markdown("---")
st.markdown("## Resources for overamping and stimulant OD prevention:")
st.markdown("* [What is overamping?](https://harmreduction.org/issues/overdose-prevention/overview/stimulant-overamping-basics/what-is-overamping/)")
st.markdown("* [Overamping prevention](https://harmreduction.org/issues/overdose-prevention/overview/stimulant-overamping-basics/overamping-prevention/)")
st.markdown("* [Recognizing stimulant overdose](https://harmreduction.org/issues/overdose-prevention/overview/stimulant-overamping-basics/recognizing-stimulant-overamping/)")
st.markdown("* [Responding to stimulant overdose](https://harmreduction.org/issues/overdose-prevention/overview/stimulant-overamping-basics/responding-to-stimulant-overamping/)")

st.markdown("---")
st.markdown("## How do stimulants affect the body?")
tab1, tab2, tab3 = st.tabs(["Stimulants + Body Temperature", "Overdoses: Stimulants vs Opioids", "Responding to Overdoses"])
st.markdown(
    """
    <style>
        div[data-testid="column"]
        {
            text-align: left !important;
        }
        div[data-testid="column"] img {
          margin-left: 50px;
        }
    </style>
    """,unsafe_allow_html=True
)
with tab1:
  col1, col2 = st.columns(2)
  with col1:
    st.write("Outdoor temperatures above 88F are associated with a lot more stimulant overdoses. Drink water, don't use as much, stay in cool places, and drink more water.")
    st.write("Stimulants can increase the body’s temperature and reduce the body’s ability to dissipate that excess heat. Central nervous system stimulants promote the release of dopamine, serotonin, and norepinephrine and block the re-uptake of dopamine.Increased levels of these neurotransmitters in the central nervous system can produce effects like increased energy, alertness, feelings of euphoria.")
  with col2:
    water_img = Image.open('datasets/code/Streamlit/images/water.png')
    st.image(water_img, width=300)
with tab2:
  st.write("Stimulants and opioids both work on the body by speeding up or slowing down some of the body’s natural processes. These two classes of drugs induce different effects in people, because they interact with different bodily processes.")
  st.write("To a bystander, a stimulant overdose may look very different from an opioid overdose. Stimulant overdose is commonly characterized by dangerous overheating, and often the individual experiencing the overdose remains conscious. Opioid overdose is typically characterized by severe difficulty breathing or not breathing at all; the person is nonresponsive and unconscious. Both types of overdose can result in physical harms, neurological harms, or death.")
  st.markdown("**How are the effect of opioids different from the effects of stimulants?**")
  st.write("Opioids also interact with the central nervous system and other parts of the body, and they do so in very different ways from stimulants. Specifically, opioids interact with neurotransmitter receptors that regulate analgesia (pain relief), sedation, and respiratory depression. Opioids can promote these processes, which is why they are effective at treating pain, making people feel sleepy, or, if they overdose, dangerously slowing down or stopping breathing all together.")

with tab3:
  st.write("Given the variable nature of stimulant overdose, it is important to seek medical help to assess the safety of the individual. In most states, Good Samaritan laws provide some immunity, which varies by jurisdiction, for those who provide assistance to people who are in danger, including as a result of illicit drug use.")
  st.markdown("### When responding to a stimulant overdose, any person may be able to:")
  st.markdown("* Call 911")
  st.markdown("* Administer naloxone if opioids could be involved")
  st.markdown("* Monitor the person carefully and stay with the individual until help arrives")
  st.markdown("* De-escalate the situation, by creating a safe place for observation and monitoring of the person in crisis and reducing external stimulation—like excessive noises and touching–to promote calm and recovery. Help the individual avoid becoming overheated. Some ways this can be done is by providing water, a sports drink, or a cool washcloth.")
  st.write("Stimulant overdose can also produce varied and concerning mental health symptoms like extreme panic, paranoia, anxiety, hallucinations, or psychosis, which can be upsetting or frightening to the individual who consumed the stimulant and to bystanders.")
  st.write("When responding to an opioid overdose, helping the individual breathe is key—through the administration of naloxone and rescue breathing.")

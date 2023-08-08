from load_init import local_css, create_sidebar, convert_df, get_nc_merged_df
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
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_lab_detail.csv"
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
nc_stimulants_list =[
  "methamphetamine",
  "cocaine",
]
nc_main_dataset = get_nc_merged_df(nc_stimulants_list)

nc_main_dataset_crack = nc_main_dataset[nc_main_dataset['expectedsubstance'].str.contains("crack") & nc_main_dataset['lab_cocaine_any_x'] == 1]
nc_main_dataset_powder_coke = nc_main_dataset[nc_main_dataset['expectedsubstance'].str.contains("crack") & nc_main_dataset['lab_cocaine_any_x'] == 1]
nc_main_dataset_crystal_meth = nc_main_dataset[(nc_main_dataset['lab_meth_any_x'] == 1) & (nc_main_dataset['crystals'] == 1)]
nc_main_dataset_powder_meth = nc_main_dataset[(nc_main_dataset['lab_meth_any_x'] == 1) & (nc_main_dataset['crystals'] != 1)]
# count how many samples are in nc_main_dataset_powder_meth




nc_stimulants.set_index('substance', inplace=True)
# sort the df by the latest_detected col
nc_stimulants.sort_values(by=['latest_detected'], inplace=True, ascending=False)
nc_stimulants['latest_detected'] = pd.to_datetime(nc_stimulants['latest_detected']).dt.strftime('%B %d, %Y')

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
def get_crystal_found_with():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/crystal_lab.csv"
    return pd.read_csv(url)
def get_coke_found_with():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/coke_lab.csv"
    return pd.read_csv(url)
def get_crack_found_with():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/crack_lab.csv"
    return pd.read_csv(url)
def get_powder_meth_found_with():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/powdermeth_lab.csv"
    return pd.read_csv(url)


create_sidebar()
st.markdown("# Stimulants in NC")
html_str = f"""
<p>Currently in North Carolina, the primary stimulants found in street drugs are methamphetamine and cocaine. These can be in crystal (crystal meth or crack) or in powder form. Methamphetamine and amphetamine can <a href="https://ncpsychedelics.streamlit.app/" _target="blank">also be found in</a> in MDMA (aka Ecstasy, molly). Stimulants may also show up pre-mixed with fentanyl in "speedballs."'</p>
"""
st.markdown(html_str, unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="All Samples", value=nc_sample_count_int)
with col2:
    st.metric(label="Programs & Clinics", value=nc_program_count_int)
with col3:
    st.metric(label="Counties", value=nc_countycount_int)
with col4:
    #  count the number of unique sampleids in the nc_main_dataset
    nc_main_dataset_sampleid_count = len(nc_main_dataset['sampleid'])
    label_="Stimulant Samples"
    st.metric(label=label_, value=nc_main_dataset_sampleid_count)
for s_ in nc_stimulants_list:
  latest = nc_stimulants.loc[s_]['latest_detected']
  text = "<div style='display: flex; flex-direction: row; align-items: center; justify-content: space-between;'><h4>Most recent detection of "+s_+": </h4><h4>"+latest+"</h4></div>"
  st.markdown(text, unsafe_allow_html=True)

st.markdown("---")

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

nc_stimulants_categories = ['Powder meth', 'Crystal meth', 'Powder coke', 'Crack']
# UPDATES:
st.subheader("View substances by category")
with st.container():
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    powder_coke_count = len(nc_main_dataset_powder_coke.index)
    st.metric(label="Powder coke", value=powder_coke_count)
  with col2:
     crack_count = len(nc_main_dataset_crack.index)
     st.metric(label="Crack", value=crack_count)
  with col3:
     powder_meth_count = len(nc_main_dataset_powder_meth.index)
     st.metric(label="Powder Meth", value=powder_meth_count)
  with col4:
     crystal_meth_count = len(nc_main_dataset_crystal_meth.index)
     st.metric(label="Crystal Meth", value=crystal_meth_count)

  crystal_adulterants = get_crystal_found_with()
  crystal_adulterants['init_substance'] = 'Crystal'
  crystal_adulterants = crystal_adulterants.set_index('init_substance', append=True).swaplevel(0,1)
  crystal_adulterants = crystal_adulterants.drop('pubchemcid', axis=1)

  coke_adulterants = get_coke_found_with()
  coke_adulterants['init_substance'] = 'Cocaine'
  coke_adulterants = coke_adulterants.set_index('init_substance', append=True).swaplevel(0,1)
  coke_adulterants = coke_adulterants.drop('pubchemcid', axis=1)

  crack_adulterants = get_crack_found_with()
  crack_adulterants['init_substance'] = 'Crack'
  crack_adulterants = crack_adulterants.set_index('init_substance', append=True).swaplevel(0,1)
  crack_adulterants = crack_adulterants.drop('pubchemcid', axis=1)

  powder_meth_adulterants = get_powder_meth_found_with()
  powder_meth_adulterants['init_substance'] = 'Powder Meth'
  powder_meth_adulterants = powder_meth_adulterants.set_index('init_substance', append=True).swaplevel(0,1)
  powder_meth_adulterants = powder_meth_adulterants.drop('pubchemcid', axis=1)
  # make the latest col a human readable date
  crystal_adulterants['latest'] = pd.to_datetime(crystal_adulterants['latest']).dt.strftime('%B %d, %Y')
  coke_adulterants['latest'] = pd.to_datetime(coke_adulterants['latest']).dt.strftime('%B %d, %Y')
  crack_adulterants['latest'] = pd.to_datetime(crack_adulterants['latest']).dt.strftime('%B %d, %Y')
  powder_meth_adulterants['latest'] = pd.to_datetime(powder_meth_adulterants['latest']).dt.strftime('%B %d, %Y')

tab1, tab2, tab3, tab4 = st.tabs(["Powder cocaine", "Crack", "Powder meth", "Crystal meth"])
st.markdown(
    """<style>
        .dataframe {text-align: left !important}
    </style>
    """, unsafe_allow_html=True)
with tab1:
    st.dataframe(
      coke_adulterants,
      hide_index=True,
      column_config={
          'substance': st.column_config.TextColumn(
             "Adulterants",
             width='medium'
          ),
          'samples': st.column_config.NumberColumn(
             "Count",
              width='medium'
          ),
          'latest': st.column_config.DateColumn(
            "Most Recent Sample Date",
            format="dddd MMMM DD, YYYY",
        ),
        }
    )
with tab2:
    st.dataframe(
      crack_adulterants,
      hide_index=True,
      column_config={
          'substance': st.column_config.TextColumn(
             "Adulterants",
             width='medium'
          ),
          'samples': st.column_config.NumberColumn(
             "Count",
              width='medium'
          ),
          'latest': st.column_config.DateColumn(
            "Most Recent Sample Date",
            format="dddd MMMM DD, YYYY",
        ),
        }
    )
with tab3:
    st.dataframe(
      powder_meth_adulterants,
      hide_index=True,
            column_config={
          'substance': st.column_config.TextColumn(
             "Adulterants",
             width='medium'
          ),

          'samples': st.column_config.NumberColumn(
             "Count",
             width='medium'
          ),
          'latest': st.column_config.DateColumn(
            "Most Recent Sample Date",
            format="dddd MMMM DD, YYYY",
        ),
        }
    )
with tab4:
    st.dataframe(
      crystal_adulterants,
      hide_index=True,
            column_config={
          'substance': st.column_config.TextColumn(
             "Adulterants",
             width='medium'
          ),
          'samples': st.column_config.NumberColumn(
             "Count",
             width='medium'
          ),
          'latest': st.column_config.DateColumn(
            "Most Recent Sample Date",
            format="dddd MMMM DD, YYYY",
        ),
        }
    )
st.markdown("---")

with st.container():
    st.subheader("Does this represent the entire NC Drug Supply?")
    st.write("We have analyzed a limited number of these drugs. People may send us samples because the drugs caused unexpected effects. Our data don't represent the entire drug supply in North Carolina.")
    st.expander("View raw data table", )

    merged_df = get_nc_merged_df(nc_stimulants_list)

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

st.markdown("---")
st.subheader("Fentanyl in stimulants")
st.markdown("There is concern that fentanyl is showing up in stimulants. [Our recent study](https://cdr.lib.unc.edu/concern/articles/zg64tx33c?locale=en) found that fentanyl mostly shows up in powder forms of methamphetamine and cocaine, and in crystal meth and or crack rarely.")
st.markdown("This doesn't mean that crack is impervious to fentanyl, [as in this NC case](https://www.justice.gov/usao-ednc/pr/drug-dealer-who-sold-fentanyl-laced-crack-sentenced-more-16-years-after-four-people). Also, keep in mind that people may send us samples because they caused unexpected effects, so these percents may be higher than in the normal drug supply.")
st.markdown("### Percentage of stimulant samples testing positive for fentanyl:")
stimulant_substance_list = [
   "powder meth",
  "crystal meth",
  "powder coke",
  "crack"
]
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
nc_stimulants_with_fent = nc_main_dataset[nc_main_dataset['lab_fentanyl_y'] == 1]
nc_stimulants_with_fent = nc_stimulants_with_fent.sort_values(by=['date_collect'], ascending=False)
nc_stimulants_with_fent = nc_stimulants_with_fent.drop_duplicates(subset=['sampleid'])

total_stimulant_fent_samples = len(nc_stimulants_with_fent.index)
nc_main_dataset_crack_w_fent = len(nc_stimulants_with_fent[nc_stimulants_with_fent['expectedsubstance'].str.contains("crack") & nc_stimulants_with_fent['lab_cocaine_any_x'] == 1].index)
nc_main_dataset_powder_coke_w_fent = len(nc_stimulants_with_fent[nc_stimulants_with_fent['expectedsubstance'].str.contains("crack") & nc_stimulants_with_fent['lab_cocaine_any_x'] == 1].index)
nc_main_dataset_crystal_meth_w_fent = len(nc_stimulants_with_fent[(nc_stimulants_with_fent['lab_meth_any_x'] == 1) & (nc_stimulants_with_fent['crystals'] == 1)].index)
nc_main_dataset_powder_meth_w_fent = len(nc_stimulants_with_fent[(nc_stimulants_with_fent['lab_meth_any_x'] == 1) & (nc_stimulants_with_fent['crystals'] != 1)].index)

with col1:
    total_powder_meth = len(nc_main_dataset_powder_meth.index)
    st.metric(label="Powder meth", value=str(math.ceil((nc_main_dataset_powder_meth_w_fent/total_stimulant_fent_samples)*100))+"%")
with col2:
    total_crystal_meth = len(nc_main_dataset_crystal_meth.index)
    st.metric(label="Crystal Meth", value=str(math.ceil((nc_main_dataset_crystal_meth_w_fent/total_stimulant_fent_samples)*100))+"%")
with col3:
    total_powder_coke = len(nc_main_dataset_powder_coke.index)
    st.metric(label="Powder coke", value=str(math.ceil((nc_main_dataset_powder_coke_w_fent/total_stimulant_fent_samples)*100))+"%")
with col4:
    total_crack_samples = len(nc_main_dataset_crack.index)
    st.metric(label="Crack", value=str(math.ceil((nc_main_dataset_crack_w_fent/total_stimulant_fent_samples)*100))+"%")

# remove the expectedsubstance, lab_meth_any_x, lab_cocaine_any_x, crystals, lab_fentanyl_y cols
nc_stimulants_with_fent = nc_stimulants_with_fent.drop('expectedsubstance', axis=1)
nc_stimulants_with_fent = nc_stimulants_with_fent.drop('lab_meth_any_x', axis=1)
nc_stimulants_with_fent = nc_stimulants_with_fent.drop('lab_cocaine_any_x', axis=1)
nc_stimulants_with_fent = nc_stimulants_with_fent.drop('crystals', axis=1)
nc_stimulants_with_fent = nc_stimulants_with_fent.drop('lab_fentanyl_y', axis=1)
with st.expander("View full data table", ):
  st.dataframe(
    nc_stimulants_with_fent,
    height=500,
    column_config={
          'sampleid': st.column_config.TextColumn(
              "Sample ID",
              disabled=True
          ),
          'substance': st.column_config.TextColumn(
              "Substance",
              disabled=True
          ),
          'county': st.column_config.TextColumn(
              "County",
              disabled=True
          ),
          'countygroup': st.column_config.TextColumn(
              "County Group",
              disabled=True
          ),
          'date_collect': st.column_config.DateColumn(
              "Sample Date",
              format="dddd MMMM DD, YYYY",
          )

      },
      hide_index=True,
      use_container_width=True,
    )

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

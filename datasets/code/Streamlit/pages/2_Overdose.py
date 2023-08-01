from load_css import local_css
local_css("datasets/code/Streamlit/style.css")
import streamlit as st
import pandas as pd
import numpy as np
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import altair as alt
from itertools import cycle

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode


def get_nc_od_color():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/program_dashboards/elements/nc_od_color.csv"
    return pd.read_csv(url)
nc_od_color = get_nc_od_color()
nc_od_color_df = pd.DataFrame(nc_od_color)
nc_od_color_df['date_collect'] = pd.to_datetime(nc_od_color_df['date_collect']).dt.strftime('%b %d, %Y')

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into format="dddd MMMM DD, YYYY",
    for col in df.columns:
      if col == 'date_collect':
        try:
          df[col] = pd.to_datetime(df[col], format='%Y-%m-%d').strftime('%M %d, %Y')
        except Exception:
          pass
      if is_object_dtype(df[col]):
        try:
          df[col] = pd.to_datetime(df[col], format='%Y-%m-%d').strftime('%M %d, %Y')
        except Exception:
          pass

      if is_datetime64_any_dtype(df[col]):
        df[col] = pd.to_datetime(df[col], format='%Y-%m-%d ').strftime('%M %d, %Y')

    modification_container = st.container()
    with modification_container:
        copy_df_columns = df.columns
        copy_df_columns = copy_df_columns.drop('sampleid')
        copy_df_columns = copy_df_columns.drop('date_collect')
        to_filter_columns = st.multiselect("Filter dataframe on", copy_df_columns)
        # remove pubchemcid from to_filter_columns
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Select a date range",
                    value=(
                #  today's date minus 90 days
                  pd.to_datetime("today") - pd.Timedelta(days=90),
                  # make max the current date + the number of days remaining in the current month
                  pd.to_datetime("today") + pd.offsets.MonthEnd(0)
                    ),
                    help="Use the date picker to select a date range. Defaults to previous 90 days. "
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


# create a title for the app
st.title('Overdose Dashboard Title')
st.markdown("---")


with st.container():
  st.subheader("View Overdoses to filter by County or Drug Color")
data_url = "https://raw.githubusercontent.com/mcnakhaee/palmerpenguins/master/palmerpenguins/data/penguins.csv"


cellRenderer=JsCode('''
                    function(params) {
                      return "<a href='www.streetsafe.supply/results/p/'" + params.value + " target='_blank'>"+ params.value + "</a>"
                    }
                  ''')

#Infer basic colDefs from dataframe types
gb = GridOptionsBuilder.from_dataframe(nc_od_color_df)

#customize gridOptions
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gb.configure_column("date_collect", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd', pivot=True)

# gb.configure_column("sampleid", cellStyle=cellRenderer)

gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)

gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
return_mode_value = 'Filtered'
fit_columns_on_grid_load = True
gb.configure_grid_options(domLayout='normal')
gridOptions = gb.build()

#Display the grid

grid_response = AgGrid(
    nc_od_color_df,
    gridOptions=gridOptions,
    width='100%',
    data_return_mode=return_mode_value,
    update_mode='GRID_CHANGED',
    fit_columns_on_grid_load=fit_columns_on_grid_load,
    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
    enable_enterprise_modules=False
    )

df = grid_response['data']
selected = grid_response['selected_rows']
selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')


st.dataframe(filter_dataframe(nc_od_color_df), use_container_width=True)


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


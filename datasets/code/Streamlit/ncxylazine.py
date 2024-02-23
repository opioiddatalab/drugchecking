# -*- coding: utf-8 -*-
import streamlit as st
st.set_page_config(
    page_title="NC Xylazine",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
)
from load_init import local_css, display_funding, create_sidebar
local_css("datasets/code/Streamlit/style.css")
import streamlit_analytics
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen
import json
from PIL import Image
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

def get_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/code/Streamlit/x_subs.csv"
    return pd.read_csv(url)
x_subs = get_data()
x_subs = pd.DataFrame(x_subs)
x_subs.set_index('rank', inplace=True)

def get_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/code/Streamlit/x_strength.csv"
    return pd.read_csv(url)
x_strength = get_data()
x_strength = pd.DataFrame(x_strength)
x_strength.set_index('order', inplace=True)

# Import public NC sample data and cache for Streamlit
@st.cache_data()
def get_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/nc/nc_analysis_dataset.csv"
    return pd.read_csv(url)
df = get_data()
df = pd.DataFrame(df)
df.set_index('sampleid', inplace=True)


# Set date format
## Retains seconds unfortunately and NaT
df['date_complete'] = pd.to_datetime(df['date_complete'], format='%d%b%Y', errors = 'coerce')

# Limit to samples with any xylazine detected
dfxyl = df[['date_complete', 'lab_xylazine_any', 'lab_cocaine', 'lab_cocaine', 'lab_meth', 'lab_fentanyl', 'expect_fentanyl', 'county', 'sen_strength', 'sen_strength', 'color', 'texture']]
dfxyl = dfxyl[dfxyl.lab_xylazine_any==1]

# Count total number of samples processed
rows_count = len(df.index)

# Count number of xylazine samples
xyl_count = len(dfxyl.index)

# Count total number of counties with any samples
counties_sampled = df['county'].nunique()

# Count number of counties samples
xyl_counties = dfxyl['county'].nunique()

# Latest date xylazine was detected
latest = dfxyl['date_complete'].max()
latest = latest.strftime('%A %B %d, %Y')


# Latest xylazine reports by county
def update_entries(grp):
    # update date_complete to most recent date
    grp['date_complete'] = grp['date_complete'].max()
    # if length of county is less than 1, then replace with "County not specified"
    if len(grp['county']) < 1:
        grp['county'] = "County not specified"
    return grp
# remove all columns except date_complete and county
dfxyl = dfxyl[['county', 'date_complete']]
# only keep the first instance of each county
dfxyl = dfxyl.groupby(by=["county"]).apply(update_entries)
mostrecent = dfxyl.drop_duplicates(subset=['county'])

# Sensations Graph
import altair as alt

url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/code/Streamlit/x_strength.csv"

sensations = alt.Chart(url).mark_bar(size=40).encode(
    x=alt.X('sensations:N',
            sort=['weaker', 'normal', 'stronger'],
            axis=alt.Axis(title="Relative to Typical Current Supply")),
    y=alt.Y('samples:Q',
            axis=alt.Axis(title="Number of Samples")),
).properties(
    width=alt.Step(80),
    title="Sensations of Drugs Containing Xylazine"
).configure_axis(
   labelFontSize=13,
   titleFontSize=15,
   labelAngle=0
).configure_title(
   fontSize=16
)



# Streamlit
streamlit_analytics.start_tracking()
create_sidebar()
st.title("North Carolina Xylazine Report")
st.subheader("Real-time results from UNC Drug Analysis Lab")

st.markdown("[Our lab in Chapel Hill](https://streetsafe.supply) tests street drugs from 30+ North Carolina harm reduction programs, hospitals, clinics, and health departments. We analyze the samples using GCMS (mass spec). Part of the multi-disciplinary [Opioid Data Lab](https://www.opioiddata.org).")
st.markdown("---")
st.markdown("There is a new cut in street drugs (primarily fentanyl, heroin, and other opioids) and it causes terrible skin problems. But we didn't have a way to track it in North Carolina. Therefore, we are making data available from our street drug testing lab to prevent public health harms.")

st.markdown("---")

# Layout 2 headline data boxes
col1, col2 = st.columns(2)

with col1:
    st.metric(
    label="Total NC drug samples analayzed",
    value=rows_count
    )

with col2:
    st.metric(
    label="Counties with any drug samples",
    value=counties_sampled
    )



# Layout 2 headline data boxes
col1, col2 = st.columns(2)

with col1:
    st.metric(
    label="Samples with xylazine",
    value=xyl_count
    )

with col2:
    st.metric(
    label="Counties with xylazine",
    value=xyl_counties
    )

st.markdown(":label: Our samples do not represent the entire drug supply. People may send us samples because they suspect xylazine or have unexpected reactions.")

st.markdown("---")

st.write(
    label="Xylazine most recently detected",
    value=latest
    )


# Latest late of xylazine detection
st.header("Xylazine last detected on:")
st.subheader(latest)
st.markdown("---")


st.subheader(":hospital: [More info on xylazine](https://harmreduction.org/wp-content/uploads/2022/11/Xylazine-in-the-Drug-Supply-one-pager.pdf) in the street drug supply")
st.markdown("Xylazine (zie-la-zine) is a cut mixed in with other street drugs. It can cause bad skin ulcers beyond the site of injection. Treated early, we can prevent amputation. Drugs with xylazine in it can cause heavy sedation that make it *seem* like naloxone isn't working. But naloxone can still help with the fentanyl, so keep it on hand.")

st.markdown("---")
st.header("Where has xylazine been detected?")
st.markdown(":label: Keep in mind we have more samples from the center of the state. Xylazine is certainly present elsewhere.")

# Chloropeth map
## Load public NC data
df = pd.read_csv("https://github.com/opioiddatalab/drugchecking/raw/main/datasets/nc/nc_analysis_dataset.csv")

## Create new variable that calculates the total samples by county for denominator
df["total_samples"] = df.groupby("county")["sampleid"].transform("nunique")

## Create a new dataframe that aggregates the data by county
## Create a new dataframe that aggregates the data by 'county' and 'fips'
agg_df = df.groupby(["county", "countyfips"]).agg(
    xylazine_count=("lab_xylazine_any", "sum"),
    latest_date=("date_complete", "max"),
    unique_samples=("sampleid", "nunique"),
)

## Reset the index of the aggregated dataframe
agg_df = agg_df.reset_index()

## Create percent of samples that are xylazine positive by dividing xylazine_countys by unique_samples
agg_df["percent"] = agg_df["xylazine_count"] / agg_df["unique_samples"] *100

## Add the percent symbol to the 'percent' column
agg_df["percent_str"] = agg_df["percent"].astype(str) + "%"

## Round the 'percent' column to one decimal place
agg_df["percent_str"] = np.round(agg_df["percent"], 1)

## Generate map
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig = px.choropleth_mapbox(agg_df,
                           geojson=counties,
                           locations='countyfips',
                           color='percent',
                           color_continuous_scale="reds",
                           range_color=(0, 100),
                           mapbox_style="carto-positron",
                           zoom=5.5,
                           center = {"lat": 35.3, "lon": -79.2},
                           opacity=0.8,
                           hover_data={'county':True, 'latest_date':True, 'percent': False, 'percent_str':True, 'unique_samples':False, 'xylazine_count':False, 'countyfips':False},
                           labels={'percent_str':'% Samples with Xylazine', 'county':'County', 'latest_date':'Most Recent Sample Date'},
                          )

fig.update_layout(title_text='Percent of Samples Testing Positive for Xylazine in NC')

st.plotly_chart(fig, use_container_width=True)


st.markdown("We've detected xylazine in about half the places from where we received samples. We are working on better maps! Sorry this isn't perfect, but we will improve it soon.")

st.subheader("Latest xylazine detection dates by location")

def cooling_highlight(val):
    color = 'white' if val else 'white'
    return f'background-color: {color}'

st.dataframe(
    mostrecent,
    height=700,
    column_config={
        'county': st.column_config.TextColumn(
            "County",
            disabled=True
        ),
        'date_complete': st.column_config.DateColumn(
            "Most Recent Sample Date",
            format="dddd MMMM DD, YYYY",
        ),
        'sampleid': None
    },
    hide_index=True,
    use_container_width=True
)

st.markdown("---")

st.header("What substances were also detected?")
st.markdown("Xylazine was found mostly mixed with fentanyl and heroin. But cocaine and xylazine were routinely found together. Less often, we found xylazine in trace amounts with methamphetamine and other drugs. Samples containing xylazine are most often reported to feel stronger.")

col1, col2 = st.columns(2)

with col1:
    st.dataframe(
        x_subs,
        use_container_width=True
        )

with col2:
    st.altair_chart(sensations)

st.markdown("---")


st.header("Why are we concerned about xylazine?")
st.video('https://www.youtube.com/watch?v=orzgwi7sxFM')

st.markdown("---")

with st.container():
    st.header("Skin Wounds and Xylazine")
    tab1, tab2 = st.tabs(["Xylazine Info (English)", "Xylazine Info (Español)"])
    with tab1:
        st.markdown("[Download PDF](https://www.addictiontraining.org/documents/resources/343_Xylazine_Handout_Large_size.pdf)")
        eng1 = Image.open('datasets/code/Streamlit/images/xylazine_eng_1.png')
        eng2 = Image.open('datasets/code/Streamlit/images/xylazine_eng_2.png')
        st.image(eng1)
        st.image(eng2)
    with tab2:
        st.markdown("[Descargar PDF](https://www.addictiontraining.org/documents/resources/342_Xylazine_Wounds_Handout_-_Spanish_Version_pocket_size.pdf)")
        esp1 = Image.open('datasets/code/Streamlit/images/xylazine_esp_1.png')
        esp2 = Image.open('datasets/code/Streamlit/images/xylazine_esp_2.png')
        st.image(esp1)
        st.image(esp2)
    st.subheader("Practical Guidance for Responding to Xylazine")
    st.video('https://youtu.be/MVs7ZfILCjE')

st.markdown("---")

st.markdown("## Where did these drug samples come from?")
st.markdown("A public service of the University of North Carolina. Data from North Carolina harm reduction programs. Full details at our [website](https://streetsafe.supply), at [UNC.edu](https://www.unc.edu/discover/drug-checking-project-cuts-overdoses/), and profiled in [_The New York Times_](https://www.nytimes.com/2022/12/24/us/politics/fentanyl-drug-testing.html))")
st.video('https://youtu.be/_TnbruaCljM?t', start_time=304)

st.markdown("Data documentation available [here](https://opioiddatalab.github.io/drugchecking/datasets/).")

st.markdown("---")

display_funding()

st.markdown("---")
streamlit_analytics.stop_tracking(unsafe_password="streetsafe")
# deleted code
# commit 90661c07dd69631efb2b960bd6f846c91c3d5191
# commit f7ff9cd6021d4680380a483db4957decd15fa39f
# commit 28ac30685a5a32c6b71b935056308df6a587ce43
# commit 6ee39e2c3fea3788af2f53516ad78ace23a5b835
# commit 006bdbf7ba477dcc7039cba008f62289bc27f777
# commit 6fc254a01691f565bd0be3c94e282900e7a6a48e
# commit 5518c5205abe3852e28700c6dbdf89cf055f951f
# commit e2d56631f559d5d68a2e88a524d3f11574998106
# commit 739e3453227b8998225d27042e20f409fbf109d3
# commit a778b0a0ee8e03f7540a8ef4d35ba64e29867394
# commit 52f19c11ae5a2c6046c909b784e3dfacf26d7624
# commit f5821c2b743f7e74c988b6a30435019a9342928a
# commit 8c27d62cf3b5096be298874cb3749977ea8cf008
# commit e8992a1a5f7c195d9b66cee56d8b091dd6fa4a14
# commit a5d8096f69ce44418cf854c74b317cd0b1f64e4f
# commit 5035a97faa8d57179bef1ad82b592df8f311941c
# commit 657a3285a07003169a6d335bb0840489fbe5cd2e
# commit 165d7cb78c695cca42683eefec17bdad1b3a6170
# commit 67537a6ff6a9e6c309b376885091ef8561f82f4a
# commit 1b32d8f7a1c36685d269f1f9568c226be890634c
# commit 93c7b26baa88ed0fc51880c2c63c245fa061158d
# commit f177cc2f2b7ef169fdc75322ed9c5084e04b6552
# commit d2b7d64515f138a7545e7ac136fd35232b5ab4f6
# commit 0777db9e8e8b5d84602f05aa8b2bd451fa22d4cd
# commit 65a27034be2a1191cad86e1f014e7d34a3693f71
# commit 8018931e815a42f3fa5e3d00a4c200247ab49b5d
# commit d6151cffb4deba2ba5c8e6741ba8a89e53928807
# commit 2f8ac5f381268a2c8f6488d915788de1619aa43f
# commit 122d9345958f35caabddecf85c33558ee74f34e7
# commit 834c3794451cada1f9bbfbb6b2ebaeac3dde3c4b
# commit 1b6cb47695a9829626b858176074980599e41a2c
# commit e662da332a801c50db81db77e44fb4ba80cf7795
# commit 1722502de82978fe8cab7a09236656360db1b8ba
# commit 49509de4bb3315594375e55fc929ea44f0290256
# commit c351454aa1446278d42f7d9644ecb3045ad2c143
# commit 05ce8683cbb2d13f0dda7e8f98b8677bdca610d2
# commit a2bf95bdf747a19d0c7952e533313f4faab537cf
# commit 76d4098dc3488a0be35de5d2c108763b7751559f
# commit 4260c5f2fb15257b55a20954355a497de86c002b
# commit 5f549b446e0766dbc23bce4a0d77ac3a92c514a7
# commit 76c42f6c0d48783856e2c18f16c19d253da675df
# commit 9563db6498dabf527b1e9dd6c6c22c362ab30aa9
# commit 10200531ee2ef131fbe866e16718dcb210006bce
# commit 5e0524bb314d87e69c47d1dd915bac9100989bee
# commit 603e98e4c3060c097b1dd39260ad006ad4fb4424
# commit c3c3e0e9fffdff28d80ddf78fada2522acf025c5
# commit 22f40ee8cd698d0406b8188b92a37ab2502c24c1
# commit 64e37f3d671534d6fe8ca72ce1d9ae454549d071
# commit d45293c135bd1fd051a68501e46340d7f9f81f84
# commit e6f0d9e8647cfd3b514aff5bb266a25ee5e7a3af
# commit e190bf6f482a33ccf9ac596355de4289a4604665
# commit 956ee8aebee119e4c60f0f68909a8f9ab51785f4
# commit 03deecc7431600dcf3af0843e6ad0df84cbff335
# commit b84c53e571260028ad36d13a349912afd9b5a6a3
# commit d23270c0d7b84f811c3f33b58e827ce5f0b223b5
# commit ab2b960e9edac80ad56ddbd993820848e3055683
# commit 9c2b94c191a15f178a281a1beff85eceecc6dd6f
# commit 8f171e5e20bc5fe7a91195da33e8c168dfa86715
# commit 218ac74bc55987c1ed5f23366dec9eeca5494b26
# commit 40d4a6007b646bb1cbc509fd89043d4634a232cc
# commit bc84a3c566b798adcd77894788c777e4ffbbabe2
# commit d4ed9e2d801f8f5376ea3cc49f5eb840cfb296a3
# commit 1348f51d84f97039e5c0d489af8799d151a75109
# commit 1809e3d97c3349e1fc8a73208d08a330668567f3
# commit 5963708eafadfd5dcca82ade0e811ae223286f3d
# commit d3e552b8a7872b7c0a3d1fdbcb8114a5911b2417
# commit 39a9477465e099af175dec45584fc6d3275068cb
# commit 80c9b040f3154baf0877d1ae37a8192ccc96d968
# commit a998457a36cf22a62a28fbc65ae38c2574dffb42
# commit 2689201008e6ac1c01c50dbc972521402664eace
# commit da84e2e2048b8984ec437d28d93a219642e32e33
# commit e2979705ca7d7244320c4939ec1483398a5519b6
# commit ec0f609b1b1bf1d3cbf82161f4f9d07171779dd8
# commit f61eae90f5db05825b8ffc31f595b4e00600afd1
# commit e5774474c769da51c42470577ed2ac2bfca1859e
# commit 0a44cb4153fe2d215e6fb9c255c2fdd3a6a2df24
# commit dfd3e5a5270f041d906a04036a0bf49e20497cb3
# commit b2d47ab507fddfd658eefc8be8afffaddc2176fc
# commit 20b36acb9958878c9db8095a86ce9c95705f032b
# commit 2099ebd23b21439268008b8408248d175c5078e9
# commit 67eb7dcd57c0f3e117c372d215fd07646a7c9d91
# commit a8618e9686f48009ee9869916f464d9e9f05dd25
# commit a23a942f51787b399b37185e50b6ba771713922a
# commit 95a02154a6c869c77e123b9abed4edb23cbfafa0
# commit a51ae8aa6be00ec2eb416eb3640742a78d7c4333
# commit e5604aaca4798d36b2e0b590922e21effb65438d
# commit 69f4b7490f79196f09b49d68702ab777b282f629
# commit 26a8c5a114ef92302678cfcb87969c155672571a
# commit 4f6f36fb043be47491dedb82f15dfc22523e9d58
# commit de5a9b1d3f02dec49fb4e9ca513670a91cf69c43
# commit aca5d924ac6e797166c71d54c98e8c0475382a49
# commit a17e0ddf6eb8a7df6a508c2acdb0d968b823c8f0
# commit d6cf875c28a442b1a34c1b4ffb280c0b7b9fcee7
# commit 59684e553885fe3de4d27a77d2e8d711bb181485
# commit c5f6f6321a3b6a28237af4daa563338015273df1
# commit caa5bfe29b4423ded6a8217fce60879bfa32a7c9
# commit 0760c21d8c7a060049b03a0be4a9bb8585a53e62
# commit c882018cc0d3d1e13dc184cc5f0b45871b141fad
# commit dc12854606a90f145fe4089ff85d02ef6879cc71
# commit 35e67f928bd51da6aea873bb80a63447b9f3f2dc
# commit d64e7472582f63739ddb2b723e1d484dfb6012ad
# commit f19baabbc7f8033531f0650ee5ebafa7f4318ab0
# commit 1ff16fc13d1ba9783f1014bbfe00ffd28c049430
# commit 10a39667e6ae53f1c6784390dc3602a1932b67b7
# commit 43ae269e8fa4f03e8c468bf4ff30a10117b109c0
# commit 8af991edba88d75deeecb76ec63da7b132ac1301
# commit 86d43ea9ef592ee9bc6d66f9eac2defbd631c4de
# commit 80eff1980c1e62a81a5cc732ee3c74cf3828ec31
# commit b1cf6ff44629a1c367dafe5d3e490e4810660c65
# commit 616135e12811d2900a6ef27aaa91bee24b8c8b51
# commit 38dde2a80c8c41c4e82cd4827b686a126b3573cb
# commit 30f81f11067f39503298118f78eda0da92f28f93
# commit 0c619b122dfe5c976b340492c34da93a40c41ba4
# commit 5f9da58931f45eb61d53debd73bdb653947bb667
# commit f8ce14f8cb553a784266b0b3224e7e7f3ba22de9
# commit ca4c5ba1f1200801f872996a59dca583362f2274
# commit cd15518e7599948fd8cf3928a9c19c93bff392a3
# commit bd7678ac884393a05c417de583b20883d1ec3bc9
# commit ce8fc2118ebfd1511484430f93f90772bff15bda
# commit e3c23603b5a063d54cdd86432bf80de146a98a97
# commit 2b20b04f8c61e4796aef182efba6e5f180831abb
# commit e8e3713a24e0228265a750415afdfdddc45ec729
# commit 650c2ec26b0400c7302dcae028a4b895b8cb393c
# commit 34e2f6c7cd0089f2025c20dfaca98e1354392820
# commit babafb4c553ddb35cf764cdd9e08eb9c07cc668d
# commit 01711b1b0c91b0bf2d7058e4b550b2d7ab2935ba
# commit a78ec6b6c4b8621aa929c49505d21e628aed44ca
# commit 8e2100349446eba3d3c21f9a1c7432b203cebbfe
# commit 0aeed1c8c2eeba17676fb10c73c28c3f264aa7f1
# commit c486f92e1d4247da8246e357cfd1a5419829c966
# commit c2639cedaa7e399dbed08f5458a6f714b3707f18
# commit a23679bf7a4f4d783fe984232a390096a3e7cd3f
# commit 66b18a33d341c7b0138347b4ee333be11d970fd7
# commit e8611c1b792b3f2583cbe82520730b0ac7bc4f04

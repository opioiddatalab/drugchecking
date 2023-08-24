from load_init import local_css, create_sidebar, convert_df, get_nc_intro_metrics, get_nc_merged_df, get_nc_county_count, get_nc_program_count, get_nc_sample_count, generate_container_with_rows, generate_adulterant_df, generate_drug_supply_table, display_funding
from streamlit_elements import elements, mui, html, dashboard
import streamlit as st
st.set_page_config(
    page_title="NC Psychedelics & Emerging Drugs",
    # make the page_icon the lab_coat emoji
    page_icon="🥽",
    initial_sidebar_state="expanded",
)
local_css("datasets/code/Streamlit/pages/psychedelics.css")
local_css("datasets/code/Streamlit/style.css")
import pandas as pd
from PIL import Image
from persist import persist, load_widget_state

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
st.markdown(" ")
col1, col2 = st.columns(2)
with col1:
  st.markdown("""
              <div style='text-align: left;'>
                As with all psychedelics, “set” and “setting” are important factors in determining whether someone has a positive or difficult experience. “Set” is a person’s mental state (their thoughts, mood, and expectations), while “setting” is the physical and social environment in which the drug is consumed. Being in a good mental state, with trusted people in a supportive environment, reduces the risk of having a difficult trip.
              </div>
              """, unsafe_allow_html=True)
with col2:
  set_setting = Image.open('datasets/code/Streamlit/images/set_setting.png')
  st.image(set_setting)
tab1, tab2, tab3, tab4, tab5 = st.tabs(['MDMA' ,'Ketamine', 'LSD', 'DMT', 'DanceSafe Kits'])
with tab1:
  st.markdown("""
                    <ul>
                      <li style='text-align: left'>Since MDMA increases core body temperature, overheating is a serious risk. This risk is compounded by being in a hot environment, taking a large dose, mixing with other temperature-raising drugs like cocaine or amphetamine, and/or lots of physical exertion.</li>
                      <li style='text-align: left'>Severe headache on any stimulant may be a sign of dangerously high blood pressure. Seek medical attention for a severe, splitting headache.</li>
                      <li style='text-align: left'>The feeling of being dehydrated due to dry mouth and high body temperature can lead people to drink way too much water. Drinking too much or too little water on MDMA can be deadly due to hypernatremia (dehydration) or hyponatremia (over hydration).</li>
                      <li style='text-align: left'>MDMA is not physically dependence-forming, but it can take on great importance in people’s lives, and some people start compulsively using it every weekend.</li>
                      <li style='text-align: left'>While it’s commonly believed that taking SSRIs with MDMA is very dangerous, it’s much more likely that the MDMA simply won’t work at all. Taking lots of MDMA to try and “break through” the blunting effects of SSRIs could become dangerous. Note: Some people may indeed react poorly to this combination, but it usually leads to letdowns as opposed to medical emergencies.</li>
                    </ul>
                    """, unsafe_allow_html=True)
  text = "<div style='text-align: left'>Additional resources for party drugs such as MDMA can be found at <a href='https://dancesafe.org/ecstasy/' target=_blank>DanceSafe.org</a></div>"
  st.markdown(text, unsafe_allow_html=True)
with tab2:
  st.markdown("""
                    <ul>
                      <li style='text-align: left'>Ketamine belongs to a class of drugs called “dissociative anesthetics” that separate perception from sensation. Other drugs in this category include PCP, DXM, and nitrous oxide.</li>
                      <li style='text-align: left'>The effects of ketamine last about 45-60 minutes. Most people return completely to baseline within 1.5-2 hours.</li>
                      <li style='text-align: left'>Although ketamine itself doesn’t slow down heart rate or breathing, it’s still risky to combine with depressants like alcohol, benzos, or GHB. These mixtures can lead to blackouts, spins, vomiting, erratic body temperature, and loss of consciousness.</li>
                      <li style='text-align: left'>Try not to use high doses of ketamine alone. People have died after taking high doses of ketamine and choking on vomit or falling forward on pillows.</li>
                      <li style='text-align: left'>“Racemic” ketamine is a mixture of r- and s-ketamine. All ketamine on the streets is racemic unless it’s made for a specific clinical purpose. There is no way to test whether ketamine is one isomer or another without the most advanced lab equipment available.</li>
                    </ul>
                    """, unsafe_allow_html=True)
  text = "<div style='text-align: left'>Additional resources for party drugs such as ketamine can be found at <a href='https://dancesafe.org/ketamine/' target=_blank>DanceSafe.org</a></div>"
  st.markdown(text, unsafe_allow_html=True)
with tab3:
  st.markdown("""
                    <ul>
                      <li style='text-align: left'>Acid should not have any strong taste. Metallic, bitter taste is a sign that you might have a different drug.</li>
                      <li style='text-align: left'>LSD produces visuals for most (but not all!) people that range from slight color and shape distortions to full-blown changes to how a space or person appears. </li>
                      <li style='text-align: left'>While many people think of psychedelics as being all about the visuals, perhaps the more significant defining factor is the change that occurs in perception of self and environment.</li>
                      <li style='text-align: left'>Only an overseas lab like Energy Control can tell you how much LSD is in a given tab. Dealers might approximate, but no one can know for sure unless they laid the blotter themselves. Start with small doses of any new batch.</li>
                      <li style='text-align: left'>As with other psychedelics (and emotionally intense drugs in general), people who have personal or family histories of mood or psychotic disorders may be at increased risk of psychological upset after taking LSD.</li>
                    </ul>
                    """, unsafe_allow_html=True)
  text = "<div style='text-align: left'>Additional resources for party drugs such as LSD can be found at <a href='https://dancesafe.org/lsd/' target=_blank>DanceSafe.org</a></div>"
  st.markdown(text, unsafe_allow_html=True)
with tab4:
  st.markdown("""
                    <p>DMT</p>
                    <ul>
                      <li style='text-align: left'>DMT, or N,N-dimethyltryptamine, is a psychedelic chemical found naturally in many plants and animals. It is the main ingredient in ayahuasca, the centuries-old South American brew used by many indigenous communities for medical and spiritual purposes.</li>
                      <li style='text-align: left'>Depending on how it is manufactured or extracted, DMT can come as crystals, powder, or a soft clumpy material. It often has a yellow-orange or brownish color, and a distinctive odor similar to mothballs or shoe leather.</li>
                      <li style='text-align: left'>Be Careful! The rapid onset and extreme intensity from smoking DMT can be overwhelming. Do not be fooled by the short duration! DMT is one of the most powerful psychedelics on the planet.</li>
                      <li style='text-align: left'>Injecting DMT is not typically advised, since improper drug sourcing or injection methods can be catastrophic.</li>
                    </ul>
                    <p>5-MeO-DMT</p>
                    <ul>
                      <li style='text-align: left'>The 5 experience is unique and cannot be directly compared to any other drug, including DMT. Its effects are not similar to those of other psychedelics like LSD or mushrooms.</li>
                      <li style='text-align: left'>Bufo-harvested 5-MeO-DMT is generally crystalline, flake-like, and clear to golden brown in color, but may also contain other organic compounds or adulterants resulting from the collection, or “milking,” of the toad.</li>
                      <li style='text-align: left'>Combining 5-MeO-DMT with other drugs, particularly stimulants (even one after the other), has resulted in deaths as well. Even on its own 5-MeO-DMT (and particularly the bufo extract) has occasionally caused seizures in some people.</li>
                      <li style='text-align: left'>WARNING: 5-MeO-DMT should never be combined with monoamine oxidase inhibitors (MAOIs). MAOIs can be found naturally in plants like harmine, harmaline, and Syrian rue, or in prescription antidepressant medications. MAOI is also a critical ingredient in ayahuasca. This combination can cause serious adverse reactions including death.</li>

                    </ul>
                    """, unsafe_allow_html=True)
  text = "<div style='text-align: left'>Additional resources for party drugs such as DMT / 5-meo-DMT can be found <a href='https://dancesafe.org/dmt/' target=_blank>here</a> or <a href='https://dancesafe.org/5-meo-dmt/' target=_blank>here</a> using DanceSafe.org</div>"
  st.markdown(text, unsafe_allow_html=True)
with tab5:
  text = "<div style='text-align: left'>Resources for accessing testing drugs, kits, and more can be found at <a href='https://dancesafe.org/shop/' target=_blank>DanceSafe.org</a></div>"
  st.markdown(text, unsafe_allow_html=  True)

st.markdown("---")
display_funding()# commit 5f549b446e0766dbc23bce4a0d77ac3a92c514a7
# commit 76c42f6c0d48783856e2c18f16c19d253da675df
# commit c3c3e0e9fffdff28d80ddf78fada2522acf025c5

# -*- coding: utf-8 -*-
# from load_css import local_css
# local_css("datasets/code/Streamlit/style.css")
import streamlit as st
# import streamlit_analytics

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# import numpy as np
# import plotly.express as px
# from urllib.request import urlopen
# import json
# from PIL import Image

# write a fn to import a csv from https://github.com/opioiddatalab/drugchecking/blob/main/datasets/selfservice/TN/analysis_dataset.csv
def load_data():
    url = "https://raw.githubusercontent.com/opioiddatalab/drugchecking/main/datasets/selfservice/TN/analysis_dataset.csv"
    return pd.read_csv(url)

tn_data_all= load_data()
tn_df = pd.DataFrame(tn_data_all)
tn_df.set_index('sampleid', inplace=True)

st.markdown("## Samples From Program XXXXX")

st.markdown("## All Samples")

st.dataframe(
        tn_df,
        use_container_width=True
        )
st.markdown("---")
st.markdown("## We expected it to test positive for fentanyl")
# filter the tn_df to only show rows where the expectedsubstance column has a value that matches a regex including fentanyl
st.markdown('*possibly hiding the table in a container to focus on the other visuals?')
tn_df_fent = tn_df[tn_df['expectedsubstance'].str.contains("fentanyl", na=False, case=False)]
st.dataframe(
        tn_df_fent,
        use_container_width=True
        )


st.markdown("### What other substances were found in the samples that were expected to test positive for fentanyl?")
xylazine_count = len(tn_df_fent[(tn_df_fent['lab_xylazine_any'] > 0) | (tn_df_fent['lab_xylazine'] > 0)])
st.metric(label="Xylazine", value=xylazine_count)
meth_count = len(tn_df_fent[(tn_df_fent['lab_meth_any'] > 0) | (tn_df_fent['lab_meth'] > 0)])
st.metric(label="Methamphetamine", value=meth_count)
meth_count = len(tn_df_fent[(tn_df_fent['lab_cocaine_any'] > 0) | (tn_df_fent['lab_cocaine'] > 0)])
st.metric(label="Methamphetamine", value=meth_count)
st.markdown("*we can continue this list with other substances that are commonly found in fentanyl samples*")
st.markdown("---")
st.markdown("### What colors and textures were reported?")
# get a list of all the values from the 'color' column of the filtered dataframe
colors = list(tn_df_fent['color'].unique())
# create a dict that uses all the colors as keys and counts the number of times each color appears in the filtered dataframe
color_counts = {}
for color in colors:
    color_counts[color] = len(tn_df_fent[tn_df_fent['color'] == color])
# create a dataframe from the color_counts dict
color_counts_df = pd.DataFrame.from_dict(color_counts, orient='index')
# create a bar chart from the color_counts_df dataframe
st.bar_chart(color_counts_df)

# get a list of all the values from the 'textures' column of the filtered dataframe
textures = list(tn_df_fent['texture'].unique())

# create a dict that uses all the textures as keys and counts the number of times each texture appears in the filtered dataframe
texture_counts = {}
for texture in textures:
    texture_counts[texture] = len(tn_df_fent[tn_df_fent['texture'] == texture])
# create a dataframe from the texture_counts dict
texture_counts_df = pd.DataFrame.from_dict(texture_counts, orient='index')
# create a wordcloud from the texture_counts_df dataframe
# convert any floats in the textures list to strings
textures = [str(texture) for texture in textures]
# remove any instances of ';' in the textures list
textures = [texture.replace(';', '') for texture in textures]
# turn the list of textures into 1 comma-separated string
textures = ', '.join(textures)
texture_wordcloud_fent = WordCloud().generate(textures)
# Display the generated image:
plt.imshow(texture_wordcloud_fent, interpolation='bilinear')
plt.axis("off")
plt.show()
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

st.markdown("---")

st.markdown("## Samples Expecting Heroin")
# filter the tn_df to only show rows where the expectedsubstance column has a value that matches a regex including fentanyl
tn_df_heroin = tn_df[tn_df['expectedsubstance'].str.contains("heroin", na=False, case=False)]
st.dataframe(
        tn_df_heroin,
        use_container_width=True
        )
st.markdown("---")

st.markdown("## Samples Expecting methamphetamine")
# filter the tn_df to only show rows where the expectedsubstance column has a value that matches a regex including fentanyl
tn_df_meth = tn_df[tn_df['expectedsubstance'].str.contains("methamphetamine", na=False, case=False)]

st.dataframe(
        tn_df_meth,
        use_container_width=True
        )

st.markdown("---")
st.markdown("## Samples Expecting amphetamine")
# filter the tn_df to only show rows where the expectedsubstance column has a value that matches a regex including fentanyl
tn_df_amph = tn_df[tn_df['expectedsubstance'].str.contains("amphetamine", na=False, case=False)]

st.dataframe(
        tn_df_amph,
        use_container_width=True
        )

st.markdown("---")

st.markdown("## Samples Expecting cocaine")
# filter the tn_df to only show rows where the expectedsubstance column has a value that matches a regex including fentanyl
tn_df_cocaine = tn_df[tn_df['expectedsubstance'].str.contains("cocaine", na=False, case=False)]

st.dataframe(
        tn_df_cocaine,
        use_container_width=True
        )
st.markdown("## Samples Expecting xylazine")
# filter the tn_df to only show rows where the expectedsubstance column has a value that matches a regex including fentanyl
tn_df_cocaine = tn_df[tn_df['expectedsubstance'].str.contains("cocaine", na=False, case=False)]

st.dataframe(
        tn_df_cocaine,
        use_container_width=True
        )

st.markdown("---")


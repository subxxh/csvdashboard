import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Farmers Market Dashboard",
    page_icon="🧺",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("quartz")

#dataset from website link
filecsv = "/Users/subah/Downloads/streamlit/dohmh-farmers-markets-1.csv"
df = pd.read_csv(filecsv)

with st.sidebar:
    st.title('🧺 Farmers Market Dashboard')

    boroughs = df["Borough"].dropna().unique().tolist()
    selected_borough = st.selectbox("Select a borough", ["All"] + boroughs)

    weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    selected_day = st.selectbox("Select a day of the week", ["All"] + weekday)

    ebt_filter = st.checkbox("Accepts EBT")
    kid_filter = st.checkbox("Food Activities for Kids")

    colors = {
    "Pastel Pink & Blue": ["#F4B6C2", "#B5EAD7", "#C7CEEA"],
    "Green & Peach": ["#C1DAD6", "#F9D5A7", "#F7A072"],
    "Lavender & Mint": ["#E0BBE4", "#957DAD", "#D291BC", "#FEC8D8", "#FFDFD3"],
    "Surprise color": ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]
}
    selected_color_theme = st.selectbox('Select a color theme', colors)


df_filter = df.copy()

if selected_borough != "All":
    df_filter = df_filter[df_filter["Borough"] == selected_borough]

if ebt_filter:
    df_filter = df_filter[df_filter["Accepts EBT"].str.strip().str.lower() == "yes"]

if kid_filter:
    df_filter = df_filter[df_filter["Food Activities for Kids"].str.strip().str.lower() == "yes"]

if selected_day != "All":
    df_filter = df_filter[df_filter["Days of Operation"].str.contains(selected_day[:3], case=False, na=False)]


st.header("NYC Farmers Markets")

st.subheader("Dataset Preview")
st.dataframe(df_filter.head())

col1, col2, col3 = st.columns(3)
col1.metric("Markets Shown", len(df_filter))
col2.metric("Boroughs Covered", df_filter["Borough"].nunique())
col3.metric("Days Available", df_filter["Days of Operation"].nunique())

borough_counts = df_filter["Borough"].value_counts().reset_index()
borough_counts.columns = ["Borough", "Count"]

fig_bar = px.bar(
    borough_counts,
    x="Borough",
    y="Count",
    color="Borough",
    color_discrete_sequence=colors[selected_color_theme],
    title="Number of Farmers Markets by Borough"
)
st.plotly_chart(fig_bar, use_container_width=True)


def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    import altair as alt
    heatmap = alt.Chart(input_df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title=input_y, titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title=input_x, titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'{input_color}:Q',
                        legend=None,
                        scale=alt.Scale(scheme=input_color_theme)),
                        stroke=alt.value('black'), 
                        strokeWidth=alt.value(0.25),
                        ).properties(width=900)
    return heatmap

df_heat = df_filter.copy()
df_heat['Days'] = df_heat['Days of Operation'].fillna('')
heat_data = []
for borough in df_heat['Borough'].unique():
    for day in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]:
        count = df_heat[df_heat['Days'].str.contains(day)].shape[0]
        heat_data.append({"Borough": borough, "Day": day, "Count": count})

df_heatmap = pd.DataFrame(heat_data)
st.subheader("Markets per Borough by Day")
st.altair_chart(make_heatmap(df_heatmap, input_y='Borough', input_x='Day', input_color='Count', input_color_theme='reds'))



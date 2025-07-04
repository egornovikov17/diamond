#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 13:11:50 2025

@author: dina
"""
# imports
import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st

# setting up the page
st.set_page_config(page_title="Diamond Dashboard", page_icon="💎", layout="wide")
st.title("💎 Diamond Analytics Dashboard 💎")

# loading the data and caching it for spead
@st.cache_data
def load_data():
     return sns.load_dataset("diamonds")

df = load_data()

# adding a pandas dataframe head with a title
st.header("Sample of Raw Data")
st.dataframe(df.head())

# adding side bar with filters
st.sidebar.header("Filter Diamonds 🔍")
# filter by cut 
selected_cuts = st.sidebar.multiselect("Select cut:", df["cut"].unique(), default=df["cut"].unique())
# filter by color
selected_colors = st.sidebar.multiselect("Select color:", df["color"].unique(), default=df["color"].unique())
# filter by clarity
selected_clarity = st.sidebar.multiselect("Select clarity:", df["clarity"].unique(), default=df["clarity"].unique())
# filtered data
filtered = df.loc[ df["cut"].isin(selected_cuts) & df["color"].isin(selected_colors) & df["clarity"].isin(selected_clarity)]


# Calculate and Display metrics
num_diamonds = len(filtered)
avg_price = filtered["price"].mean()
avg_carat = filtered["carat"].mean()
max_price = filtered["price"].max()

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Diamonds", value=f"{num_diamonds:,}")
col2.metric(label="Avg. Price", value=f"${avg_price:,.0f}")
col3.metric(label="Avg. Carat", value=f"{avg_carat:.2f}")
col4.metric(label="Max Price", value=f"${max_price:,.0f}")

# figure 1: Heatmap
# Group by cut and color, and calculate the mean price and create a pivot table
pivot_table = filtered.pivot_table(values='price', index='cut', columns='color', aggfunc='mean')
fig_heatmap = px.imshow(
    pivot_table,  # Set 'cut' as the index,  
    # Axis and color labels
    title="Heatmap of Mean Price by Cut and Color",
    labels= {'x': 'Color', 'y': 'Cut', 'color': 'Average Price in US $'},
    text_auto="1.0f",  # Show text with 2 decimal places
    color_continuous_scale=px.colors.sequential.Purples,
    width=1000,
    height=700,
    aspect='auto' # allows the aspect ratio to be not equal to one, i.e. the heatmap will not be a square
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# figure2: price by cut bar plot
avg_by_cut = (filtered.groupby("cut")["price"].agg("mean").reset_index())
fig_cut = px.bar(avg_by_cut, x="cut", y="price", title="Average Diamond Price by Cut", 
                 labels={"price": "Avg Price ($)"}, color_discrete_sequence=px.colors.qualitative.Prism)
#st.plotly_chart(fig_cut, use_container_width=True)

# figure 3: Clarity Breakdown Donut chart
clarity_counts = filtered["clarity"].value_counts().reset_index()
fig_clarity = px.pie( clarity_counts, names="clarity", values="count", hole=0.4,
                     title="Diamond Clarity Distribution", color_discrete_sequence=px.colors.qualitative.Prism)

#st.plotly_chart(fig_clarity, use_container_width=True)

#figure 4: price histogram
fig_hist_price = px.histogram(
    filtered, x="price", nbins=30, title="Price Distribution", labels={"price":"Price ($)"},
    color_discrete_sequence=px.colors.qualitative.Prism)
#st.plotly_chart(fig_hist)

#figure 5: carat histogram
fig_hist_carat = px.histogram(
    filtered, x="carat", nbins=30, title="Carat Distribution", labels={"carat":"Carat"},
    color_discrete_sequence=px.colors.qualitative.Prism)


# arrange layout
left, right = st.columns(2)
with left:
    st.plotly_chart(fig_cut, use_container_width=True)
    st.plotly_chart(fig_hist_price, use_container_width=True)
with right:
    st.plotly_chart(fig_clarity, use_container_width=True)
    st.plotly_chart(fig_hist_carat, use_container_width=True)
    
   
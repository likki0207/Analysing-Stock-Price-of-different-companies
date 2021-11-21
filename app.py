import streamlit as st

st.sidebar.radio("Navigate", 
                 ["Home", "Data",
                  "Dashboard", "About", 
                  "Contribute"])
st.sidebar.selectbox("Granularity", ["Worldwide", "Country"])
import plotly.express as px

fig = px.bar(x=df["X"], 
             y=df["Y"])

st.plotly_chart(fig)

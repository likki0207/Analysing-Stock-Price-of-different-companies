#Importing the required Libraries
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
st.image(
            "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.analyticsvidhya.com%2Fblog%2F2021%2F07%2Fstock-prices-analysis-with-python%2F&psig=AOvVaw0xtsxaHUZKQOnGQKAUeMIX&ust=1637571933137000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCPCv7_2MqfQCFQAAAAAdAAAAABAD",
            width=1000, # Manually Adjust the width of the image as per requirement
        )
st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown("<h1 style='text-align: center; color: Yellow;'><u>Analysing Stock Prices for different companies</u></h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: center; color: White;'><u>Input features given by the user</u></h1>", unsafe_allow_html=True)

#Loading the data corresponding to each company
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

st.header('Displaying the Companies in the Selected Sector')
st.dataframe(df_selected_sector)

# Download S&P500 data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)


data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Security
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
  plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot()

num_company = st.sidebar.slider("Select the number of companies for which you want to see the plot",1, 10)

if st.button('Show Plots'):
    st.header('Closing Price of the stock')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)

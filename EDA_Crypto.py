import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import requests
import os

st.set_page_config(layout="wide")

# --- Logo ---
st.image(os.path.join(os.getcwd(), "static", "logo.jpg"), width=1000)

st.title("Crypto Price App")

st.write("This app retrieves cryptocurrency prices for the top 100 cryptocurrencies from **CoinGecko!**")

expander_bar = st.expander("About")
expander_bar.markdown(
    """
* **Python libraries:** base64, pandas, streamlit, matplotlib, requests, os
* **Data source:** [CoinGecko](https://www.coingecko.com/).
* **Credit:** Adapted from the CoinMarketCap scraper version.
"""
)

# Sidebar
col1 = st.sidebar
col2, col3 = st.columns((2, 1))

col1.header("Input Options")

currency_price_unit = col1.selectbox("Select currency for price", ("usd", "btc", "eth"))

@st.cache_data
def load_data(vs_currency="usd"):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d",
    }
    data = requests.get(url, params=params).json()

    df = pd.DataFrame(
        [
            {
                "coin_name": coin["name"],
                "coin_symbol": coin["symbol"].upper(),
                "price": coin["current_price"],
                "percent_change_1h": coin["price_change_percentage_1h_in_currency"],
                "percent_change_24h": coin["price_change_percentage_24h_in_currency"],
                "percent_change_7d": coin["price_change_percentage_7d_in_currency"],
                "market_cap": coin["market_cap"],
                "volume_24h": coin["total_volume"],
            }
            for coin in data
        ]
    )
    return df

df = load_data(currency_price_unit)

sorted_coin = sorted(df["coin_symbol"])
selected_coin = col1.multiselect("Cryptocurrency", sorted_coin, sorted_coin)

df_selected_coin = df[df["coin_symbol"].isin(selected_coin)]

num_coin = col1.slider("Display Top N Coins", 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

percent_timeframe = col1.selectbox("Percent change time frame", ["7d", "24h", "1h"])
percent_dict = {
    "7d": "percent_change_7d",
    "24h": "percent_change_24h",
    "1h": "percent_change_1h",
}
selected_percent_timeframe = percent_dict[percent_timeframe]

sort_values = col1.selectbox("Sort values?", ["Yes", "No"])

col2.subheader("Price Data of Selected Cryptocurrency")
col2.write(
    f"Data Dimension: {df_selected_coin.shape[0]} rows and {df_selected_coin.shape[1]} columns"
)

col2.dataframe(df_coins)

# --- File Download ---
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

# --- % Change Table ---
col2.subheader("Table for % Price Change")
df_change = pd.concat(
    [
        df_coins.coin_symbol,
        df_coins.percent_change_1h,
        df_coins.percent_change_24h,
        df_coins.percent_change_7d,
    ],
    axis=1,
)
df_change = df_change.set_index("coin_symbol")
df_change["positive_percent_change_1h"] = df_change["percent_change_1h"] > 0
df_change["positive_percent_change_24h"] = df_change["percent_change_24h"] > 0
df_change["positive_percent_change_7d"] = df_change["percent_change_7d"] > 0
col2.dataframe(df_change)

# --- Bar Plot ---
col3.subheader("Bar plot of % Price Change")

if percent_timeframe == "7d":
    if sort_values == "Yes":
        df_change = df_change.sort_values(by=["percent_change_7d"])
    col3.write("*7 days period*")
    column = "percent_change_7d"
    color_map = df_change["positive_percent_change_7d"].map({True: "g", False: "r"}).tolist()

elif percent_timeframe == "24h":
    if sort_values == "Yes":
        df_change = df_change.sort_values(by=["percent_change_24h"])
    col3.write("*24 hour period*")
    column = "percent_change_24h"
    color_map = df_change["positive_percent_change_24h"].map({True: "g", False: "r"}).tolist()

else:
    if sort_values == "Yes":
        df_change = df_change.sort_values(by=["percent_change_1h"])
    col3.write("*1 hour period*")
    column = "percent_change_1h"
    color_map = df_change["positive_percent_change_1h"].map({True: "g", False: "r"}).tolist()

if not df_change.empty:
    plt.figure(figsize=(5, len(df_change) * 0.4))
    df_change[column].plot(kind="barh", color=color_map)
    plt.tight_layout()
    col3.pyplot(plt)
else:
    col3.write("⚠️ No data available to plot.")






        





import streamlit as st
import yfinance as yf
import pandas as pd
import base64
import matplotlib.pyplot as plt
import requests 

st.title('Nifty 50 App')

st.markdown('''
This app performs simple webscraping of the **Nifty 50 (from Wikipedia) data!
* **Python libraries:** base64 , pandas , streamlit
* **Data source:** [Wikipedia](https://www.wikipedia.org/).
''')

st.sidebar.header('User Input Features')

@st.cache_resource
def load_data():
    url = "https://en.wikipedia.org/wiki/NIFTY_50"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # ensures a clean 200 response

    # Now pass the HTML content to pandas
    tables = pd.read_html(response.text)
    html = pd.read_html(response.text)
    df = html[1]

    return df   

df = load_data()
sector = df.groupby('Sector[15]')

sorted_sector_unique = sorted(df['Sector[15]'].unique())
selected_sector = st.sidebar.multiselect('Sector',sorted_sector_unique)

df_selected_sector = df[(df['Sector[15]'].isin(selected_sector))]

st.header('Display Companies in Selected Sector')
st.write(
    'Data Dimension: ' 
    + str(df_selected_sector.shape[0]) 
    + ' rows and ' 
    + str(df_selected_sector.shape[1]) 
    + ' columns.'
)
st.dataframe(df_selected_sector)

def filedownload(df):
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()
    href =f'<a href="data:file/csv;base64,{b64}" download="Nifty50.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector),unsafe_allow_html  = True)

tickers = list(df_selected_sector.Symbol)

# Add suffix if missing
tickers = [t if t.endswith(".NS") else t + ".NS" for t in tickers]

st.write("Tickers being fetched:", tickers)  # Debug print

if not tickers:
    st.error("No tickers selected! Please choose at least one.")
else:
    try:
        data = yf.download(
            tickers=tickers,
            period="ytd",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            threads=True
        )
        st.write("Data shape:", data.shape)
    except Exception as e:
        st.error(f"Error fetching data: {e}")

def price_plot(symbol):
    # Add ".NS" if missing (Yahoo Finance format for NSE stocks)
    if not symbol.endswith(".NS"):
        symbol = symbol + ".NS"

    try:
        # Case 1: data['Close']['BEL.NS']
        if ('Close', symbol) in data.columns:
            df = pd.DataFrame(data['Close'][symbol])
            df.columns = ['Close']
        
        # Case 2: data['BEL.NS']['Close']
        elif (symbol, 'Close') in data.columns:
            df = pd.DataFrame(data[symbol]['Close'])
            df.columns = ['Close']
        
        else:
            st.warning(f"❌ Symbol {symbol} not found in data")
            return

        # Add Date column
        df['Date'] = df.index

        # Plot
        plt.figure(figsize=(10, 5))
        plt.fill_between(df['Date'], df['Close'], color='skyblue', alpha=0.3)
        plt.plot(df['Date'], df['Close'], color='skyblue', alpha=0.8)
        plt.xticks(rotation=90)
        plt.title(symbol, fontweight='bold')
        plt.xlabel('Date', fontweight='bold')
        plt.ylabel('Closing Price', fontweight='bold')

        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error plotting {symbol}: {e}")

num_company = st.sidebar.slider('Number of Companies',1,50)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
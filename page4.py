import streamlit as st
import yfinance as yf
import pandas as pd

def display_page():
    st.title("Nifty 50 Stock Scanner")

    # List of Nifty 50 stock symbols
    nifty_50_symbols = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS",
        "ICICIBANK.NS", "KOTAKBANK.NS", "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS",
        "ITC.NS", "ASIANPAINT.NS", "HCLTECH.NS", "MARUTI.NS", "AXISBANK.NS",
        "LT.NS", "BAJFINANCE.NS", "TITAN.NS", "ULTRACEMCO.NS", "NESTLEIND.NS",
        "SUNPHARMA.NS", "WIPRO.NS", "POWERGRID.NS", "NTPC.NS", "M&M.NS",
        "INDUSINDBK.NS", "BAJAJFINSV.NS", "HEROMOTOCO.NS", "ADANIPORTS.NS", "ONGC.NS",
        "TECHM.NS", "GRASIM.NS", "TATASTEEL.NS", "JSWSTEEL.NS", "COALINDIA.NS",
        "BPCL.NS", "BRITANNIA.NS", "SHREECEM.NS", "CIPLA.NS", "DIVISLAB.NS",
        "DRREDDY.NS", "EICHERMOT.NS", "UPL.NS", "HINDALCO.NS", "BAJAJ-AUTO.NS",
        "TATAMOTORS.NS", "SBILIFE.NS", "ADANIGREEN.NS", "VEDL.NS", "AMBUJACEM.NS"
    ]

    # Fetch data for Nifty 50 stocks
    data = yf.download(nifty_50_symbols, period="5d", group_by='ticker')

    # Extract closing prices and volumes
    closing_prices = pd.DataFrame({symbol: data[symbol]['Close'] for symbol in nifty_50_symbols})
    volumes = pd.DataFrame({symbol: data[symbol]['Volume'] for symbol in nifty_50_symbols})

    # Calculate percentage change
    pct_change = closing_prices.pct_change().iloc[-1] * 100

    # Calculate top 5 gainers
    top_5_gainers = pct_change.nlargest(10).reset_index()
    top_5_gainers.columns = ['Scrip', '% Change']
    
    # Calculate top 10 losers
    top_10_losers = pct_change.nsmallest(10).reset_index()
    top_10_losers.columns = ['Scrip', '% Change']

    # Calculate highest volume
    highest_volume = volumes.iloc[-1].nlargest(10).reset_index()
    highest_volume.columns = ['Scrip', 'Volume']

    # Apply custom CSS to make tables compact and set colors
    st.markdown("""
        <style>
        .compact-table {
            border-collapse: collapse;
            margin: 0;
            padding: 0;
            width: 100%;
        }
        .compact-table th, .compact-table td {
            padding: 4px 8px;
            border: 1px solid #ddd;
        }
        .compact-table th {
            background-color: white;
            color: black;
            text-align: center;
        }
        .compact-table td {
            background-color: #f2f2f2;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create columns
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")

    # Display top 5 gainers
    with col1:
        st.subheader("Top 10 Gainers")
        st.markdown(top_5_gainers.to_html(classes='compact-table', index=False), unsafe_allow_html=True)

    # Display top 10 losers
    with col2:
        st.subheader("Top 10 Losers")
        st.markdown(top_10_losers.to_html(classes='compact-table', index=False), unsafe_allow_html=True)

    # Display highest volume stocks
    with col3:
        st.subheader("Stocks with Highest Volume")
        st.markdown(highest_volume.to_html(classes='compact-table', index=False), unsafe_allow_html=True)

if __name__ == "__main__":
    display_page()

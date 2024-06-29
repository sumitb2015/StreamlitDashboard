import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import asyncio

def display_page():
    st.title("US & European Stock Indices Real-Time Prices")

    # List of US and European indices
    us_indices = {
        "Dow Jones": "^DJI",
        "Nasdaq": "^IXIC",
        "S&P 500": "^GSPC"
    }

    european_indices = {
        "DAX": "^GDAXI",
        "FTSE 100": "^FTSE",
        "CAC 40": "^FCHI"
    }

    st.sidebar.header("Index Selection")

    selected_us_indices = st.sidebar.multiselect('Select US Indices', options=list(us_indices.keys()), default=list(us_indices.keys()))
    selected_european_indices = st.sidebar.multiselect('Select European Indices', options=list(european_indices.keys()), default=list(european_indices.keys()))

    all_selected_us_indices = {k: us_indices[k] for k in selected_us_indices}
    all_selected_european_indices = {k: european_indices[k] for k in selected_european_indices}

    # Placeholder for the charts
    chart_placeholder = st.empty()

    # Function to fetch 1-minute data for the selected indices
    async def fetch_data(selected_symbols):
        data = {}
        for symbol in selected_symbols:
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(interval="1m", period="1d")
                prev_close = stock.history(period="5d")['Close'][-2]
                hist['Close'] = hist['Close'].fillna(method='ffill').fillna(method='bfill')  # Fill missing data points
                data[symbol] = (hist['Close'] / prev_close - 1) * 100
            except Exception as e:
                st.error(f"Error fetching data for {symbol}: {e}")
        return data

    # Function to update the data periodically
    async def update_data():
        while True:
            selected_us_symbols = list(all_selected_us_indices.values())
            selected_european_symbols = list(all_selected_european_indices.values())
            us_data = await fetch_data(selected_us_symbols)
            european_data = await fetch_data(selected_european_symbols)

            with chart_placeholder.container():
                if us_data:
                    df_us = pd.DataFrame(us_data)
                    st.subheader('US Indices Prices')
                    fig_us = go.Figure()
                    for name, symbol in all_selected_us_indices.items():
                        fig_us.add_trace(go.Scatter(x=df_us.index, y=df_us[symbol], mode='lines', name=name))
                    fig_us.update_layout(
                        xaxis_title='Time',
                        yaxis_title='Percentage Change (%)',
                        legend_title_text='US Indices',
                        height=400,
                        width=1600,
                        margin=dict(l=0, r=0, t=30, b=0)
                    )
                    st.plotly_chart(fig_us)

                if european_data:
                    df_european = pd.DataFrame(european_data)
                    st.subheader('European Indices Prices')
                    fig_european = go.Figure()
                    for name, symbol in all_selected_european_indices.items():
                        fig_european.add_trace(go.Scatter(x=df_european.index, y=df_european[symbol], mode='lines', name=name))
                    fig_european.update_layout(
                        xaxis_title='Time',
                        yaxis_title='Percentage Change (%)',
                        legend_title_text='European Indices',
                        height=400,
                        width=1600,
                        margin=dict(l=0, r=0, t=30, b=0)
                    )
                    st.plotly_chart(fig_european)

            await asyncio.sleep(60)  # Wait for 1 minute before fetching the data again

    # Run the update data function
    asyncio.run(update_data())

# Display the page
if __name__ == "__main__":
    display_page()

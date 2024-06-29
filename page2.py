import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import asyncio
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

def display_page():
    # List of index symbols
    index_symbols = [
        "^NSEI",
        "^NSEBANK",
        "^CNXIT"
    ]

    st.title("Nifty Price Chart")

    # Sidebar for index selection, EMA period input, and data interval selection
    selected_index = st.sidebar.selectbox("Select an Index", index_symbols, index=0)
    ema_periods = [20, 50, 100]
    interval = st.sidebar.selectbox("Select Data Interval", ("1m", "5m", "15m", "30m", "1h", "1d", "1wk"))
    period = st.sidebar.selectbox("Select Period", ("1d", "5d", "1mo", "3mo", "6mo", "1y"))

    # Function to fetch data for the selected index with the chosen interval
    async def fetch_index_data(symbol, interval, period):
        data = {}
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(interval=interval, period=period)
            if interval in ["1m", "5m", "15m", "30m", "1h"]:
                hist = hist.between_time("09:15", "15:30")
            data[symbol] = hist
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {e}")
        return data

    # Function to calculate EMA and RSI
    def calculate_indicators(df, ema_periods, rsi_period=14):
        close_prices = df['Close']
        ema = {period: EMAIndicator(close_prices, window=period).ema_indicator() for period in ema_periods}
        rsi = RSIIndicator(close_prices, window=rsi_period).rsi()
        return ema, rsi

    # Function to update the data periodically
    async def update_index_data(symbol, interval, period):
        while True:
            data = await fetch_index_data(symbol, interval, period)
            if data:
                df = pd.DataFrame(data[symbol])
                df_close = df['Close']

                # Calculate the normalized value and convert it to percentage change
                df_normalized = df_close / df_close.iloc[0]
                df_percentage = (df_normalized - 1) * 100

                # Calculate indicators
                ema, rsi = calculate_indicators(df, ema_periods, rsi_period=14)
                
                # Display EMA values with background color based on the price
                current_price = df_close.iloc[-1]
                ema_display = f'**Current Price: {current_price:.2f}**'
                for period in ema_periods:
                    ema_value = ema[period].iloc[-1]
                    color = "green" if current_price > ema_value else "red"
                    ema_display += f' <span style="background-color: {color}; color: white; padding: 0.25em; margin-right: 5px;">EMA ({period}): {ema_value:.2f}</span> '

                # Display RSI value with background color based on its value
                rsi_value = rsi.iloc[-1]
                rsi_color = "green" if rsi_value > 60 else "red" if rsi_value < 40 else "white"
                rsi_text_color = "white" if rsi_color != "white" else "black"
                ema_display += f' <span style="background-color: {rsi_color}; color: {rsi_text_color}; padding: 0.25em;">RSI: {rsi_value:.2f}</span>'
                st.markdown(ema_display, unsafe_allow_html=True)

                # Plot the index data with percentage change
                st.subheader('Index Prices')
                fig = go.Figure()

                fig.add_trace(go.Scatter(x=df_percentage.index, y=df_percentage, mode='lines', name=symbol))
                for period in ema_periods:
                    fig.add_trace(go.Scatter(x=df_percentage.index, y=(ema[period] / df_close.iloc[0] - 1) * 100, mode='lines', name=f'EMA ({period})'))

                fig.update_layout(
                    xaxis_title='Time',
                    yaxis_title='Percentage Change (%)',
                    legend_title_text='Index',
                    height=750,  # Adjust the height of the figure
                    width=1600,  # Adjust the width of the figure
                    margin=dict(l=0, r=0, t=30, b=0),
                    xaxis_rangeslider_visible=False  # Hide the range slider to avoid gaps
                )
                st.plotly_chart(fig)
            else:
                st.write("Please select an index to display the chart.")
            await asyncio.sleep(60)  # Wait for 1 minute before fetching the data again

    # Run the update data function with the selected index, interval, and period
    asyncio.run(update_index_data(selected_index, interval, period))

# Display the page
if __name__ == "__main__":
    display_page()

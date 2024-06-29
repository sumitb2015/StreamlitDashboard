import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import json
import os
import asyncio

# File to store additional symbols
SYMBOLS_FILE = 'additional_symbols.json'

# Load additional symbols from the file
def load_additional_symbols():
    if os.path.exists(SYMBOLS_FILE):
        with open(SYMBOLS_FILE, 'r') as file:
            return json.load(file)
    return {"stocks": [], "indexes": []}

# Save additional symbols to the file
def save_additional_symbols(symbols):
    with open(SYMBOLS_FILE, 'w') as file:
        json.dump(symbols, file)

def display_page():
    # List of default symbols
    default_symbols = [
        "RELIANCE.NS",
        "TCS.NS",
        "HDFCBANK.NS",
        "BHARTIARTL.NS",
        "ICICIBANK.NS",
        "SBIN.NS",
        "INFY.NS",
    ]

    # List of index symbols
    index_symbols = [
        "^NSEI",
        "^NSEBANK",
        "^CNXIT"
    ]
    
    # Main content
    st.title('Stock & FNO Dashboard')
    st.divider()

    # Initialize session state for additional symbols
    if 'additional_symbols' not in st.session_state:
        st.session_state['additional_symbols'] = load_additional_symbols()
    else:
        # Ensure that additional_symbols is a dictionary with 'stocks' and 'indexes'
        if not isinstance(st.session_state['additional_symbols'], dict):
            st.session_state['additional_symbols'] = {"stocks": [], "indexes": []}
        if 'stocks' not in st.session_state['additional_symbols']:
            st.session_state['additional_symbols']['stocks'] = []
        if 'indexes' not in st.session_state['additional_symbols']:
            st.session_state['additional_symbols']['indexes'] = []

    # Sidebar for stock selection and adding more stocks
    st.sidebar.header("Stock Selection")

    # Radio button to select the group for the new symbol
    add_to_group = st.sidebar.radio("Add new stock to:", ("Stocks", "Indexes"))

    # Allow user to add more stocks
    new_symbol = st.sidebar.text_input("Add a new stock symbol (e.g., 'AAPL')")
    if st.sidebar.button("Add Stock"):
        if new_symbol:
            if add_to_group == "Stocks":
                if new_symbol not in st.session_state['additional_symbols']["stocks"] and new_symbol not in default_symbols:
                    st.session_state['additional_symbols']["stocks"].append(new_symbol)
                    save_additional_symbols(st.session_state['additional_symbols'])
                    new_symbol = ""  # Clear input field
                else:
                    st.sidebar.error(f"The stock symbol '{new_symbol}' is already in the list.")
            else:
                if new_symbol not in st.session_state['additional_symbols']["indexes"] and new_symbol not in index_symbols:
                    st.session_state['additional_symbols']["indexes"].append(new_symbol)
                    save_additional_symbols(st.session_state['additional_symbols'])
                    new_symbol = ""  # Clear input field
                else:
                    st.sidebar.error(f"The index symbol '{new_symbol}' is already in the list.")

    # Combine default symbols with additional symbols
    all_stock_symbols = default_symbols + st.session_state['additional_symbols']["stocks"]
    all_index_symbols = index_symbols + st.session_state['additional_symbols']["indexes"]

    # Initialize session state for visibility toggle
    if 'show_stocks' not in st.session_state:
        st.session_state['show_stocks'] = True

    if 'show_indexes' not in st.session_state:
        st.session_state['show_indexes'] = True

    # Initialize session state for remove dropdown visibility
    if 'show_remove_stock_dropdown' not in st.session_state:
        st.session_state['show_remove_stock_dropdown'] = False

    if 'show_remove_index_dropdown' not in st.session_state:
        st.session_state['show_remove_index_dropdown'] = False

    # Button to toggle stock selection visibility
    if st.sidebar.button("Toggle Stock Selection"):
        st.session_state['show_stocks'] = not st.session_state['show_stocks']

    # Button to toggle index selection visibility
    if st.sidebar.button("Toggle Index Selection"):
        st.session_state['show_indexes'] = not st.session_state['show_indexes']

    # Function to remove a stock
    def remove_stock(symbol, group):
        if group == "Stocks" and symbol in st.session_state['additional_symbols']["stocks"]:
            st.session_state['additional_symbols']["stocks"].remove(symbol)
        elif group == "Indexes" and symbol in st.session_state['additional_symbols']["indexes"]:
            st.session_state['additional_symbols']["indexes"].remove(symbol)
        save_additional_symbols(st.session_state['additional_symbols'])

    # Multi-select for stocks
    if st.session_state['show_stocks']:
        selected_stocks = st.sidebar.multiselect('Select Stocks', options=all_stock_symbols, default=default_symbols[:3])
    else:
        selected_stocks = []

    # Button to show remove stock dropdown
    if st.sidebar.button("Remove a Stock"):
        st.session_state['show_remove_stock_dropdown'] = not st.session_state['show_remove_stock_dropdown']

    # Dropdown and button to remove a selected stock
    if st.session_state['show_remove_stock_dropdown']:
        stock_to_remove = st.sidebar.selectbox("Select Stock to Remove", options=st.session_state['additional_symbols']["stocks"], key="remove_stock")
        if st.sidebar.button("Confirm Remove Stock"):
            remove_stock(stock_to_remove, "Stocks")

    # Multi-select for indexes
    if st.session_state['show_indexes']:
        selected_indexes = st.sidebar.multiselect('Select Indexes', options=all_index_symbols, default=index_symbols[:1])
    else:
        selected_indexes = []

    # Button to show remove index dropdown
    if st.sidebar.button("Remove an Index"):
        st.session_state['show_remove_index_dropdown'] = not st.session_state['show_remove_index_dropdown']

    # Dropdown and button to remove a selected index
    if st.session_state['show_remove_index_dropdown']:
        index_to_remove = st.sidebar.selectbox("Select Index to Remove", options=st.session_state['additional_symbols']["indexes"], key="remove_index")
        if st.sidebar.button("Confirm Remove Index"):
            remove_stock(index_to_remove, "Indexes")

    # Create placeholders for the charts
    stock_chart_placeholder = st.empty()
    index_chart_placeholder = st.empty()

    # Function to fetch 1-minute data for the selected stocks and indexes
    async def fetch_data(selected_symbols):
        data = {}
        for symbol in selected_symbols:
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(interval="1m", period="1d")
                data[symbol] = hist['Close']
            except Exception as e:
                st.error(f"Error fetching data for {symbol}: {e}")
        return data

    # Function to update the data periodically
    async def update_data():
        while True:
            selected_symbols = selected_stocks + selected_indexes
            if selected_symbols:
                data = await fetch_data(selected_symbols)
                if data:
                    df = pd.DataFrame(data)

                    # Calculate the normalized value and convert it to percentage change
                    df_normalized = df / df.iloc[0]
                    df_percentage = (df_normalized - 1) * 100

                    # Plot the stock data with percentage change
                    with stock_chart_placeholder:
                        st.subheader('Stock Prices')
                        if selected_stocks:
                            fig = go.Figure()
                            for symbol in selected_stocks:
                                fig.add_trace(go.Scatter(x=df_percentage.index, y=df_percentage[symbol], mode='lines', name=symbol))
                            fig.update_layout(
                                xaxis_title='Time',
                                yaxis_title='Percentage Change (%)',
                                legend_title_text='Stocks',
                                height=750,  # Adjust the height of the figure
                                width=1600,   # Adjust the width of the figure
                                margin=dict(l=0, r=0, t=30, b=0)
                            )
                            st.plotly_chart(fig)

                    # Plot the index data with percentage change
                    with index_chart_placeholder:
                        st.subheader('Index Prices')
                        if selected_indexes:
                            fig = go.Figure()
                            for symbol in selected_indexes:
                                fig.add_trace(go.Scatter(x=df_percentage.index, y=df_percentage[symbol], mode='lines', name=symbol))
                            fig.update_layout(
                                xaxis_title='Time',
                                yaxis_title='Percentage Change (%)',
                                legend_title_text='Indexes',
                                height=750,  # Adjust the height of the figure
                                width=1600,   # Adjust the width of the figure
                                margin=dict(l=0, r=0, t=30, b=0)
                            )
                            st.plotly_chart(fig)
            else:
                st.write("Please select at least one stock or index to display the chart.")
            await asyncio.sleep(60)  # Wait for 1 minute before fetching the data again

    # Run the update data function
    asyncio.run(update_data())

# Display the page
if __name__ == "__main__":
    display_page()

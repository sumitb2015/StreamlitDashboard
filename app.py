import streamlit as st
import page1 
import page2 
import page3 
import page4

st.set_page_config(layout="wide")

# Sidebar for page navigation
page = st.sidebar.selectbox("Select a Page", ["Stock Dashboard", "Price Chart","US & European Stock Indices","Nifty 50 Stock Scanner"])

if page == "Stock Dashboard":
    page1.display_page()
elif page == "Price Chart":
    page2.display_page()
elif page == "US & European Stock Indices":
    page3.display_page()
elif page == "Nifty 50 Stock Scanner":
    page4.display_page()




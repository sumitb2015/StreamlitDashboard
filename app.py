import streamlit as st
import page1 
import page2 
import page3 

st.set_page_config(layout="wide")

# Sidebar for page navigation
page = st.sidebar.selectbox("Select a Page", ["Stock Dashboard", "Price Chart","US & European Stock Indices"])

if page == "Stock Dashboard":
    page1.display_page()
elif page == "Price Chart":
    page2.display_page()
else:
    page3.display_page()




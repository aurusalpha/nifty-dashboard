# app.py (Streamlit dashboard for NIFTY 50 spot prices)

import streamlit as st
from utils.nse_api import fetch_ticker_data

# NIFTY 50 symbols (same as those used in nse_api.py)
nifty_symbols = [
    "RELIANCE", "INFY", "HDFCBANK", "ICICIBANK", "TCS", "KOTAKBANK", "SBIN", "LT",
    "ITC", "BHARTIARTL", "ASIANPAINT", "MARUTI", "SUNPHARMA", "AXISBANK", "ULTRACEMCO",
    "BAJFINANCE", "NTPC", "HINDUNILVR", "POWERGRID", "INDUSINDBK", "TITAN", "BAJAJFINSV",
    "GRASIM", "TATASTEEL", "ONGC", "JSWSTEEL", "TECHM", "CIPLA", "NESTLEIND", "ADANIENT",
    "ADANIPORTS", "DIVISLAB", "DRREDDY", "BRITANNIA", "HEROMOTOCO", "HCLTECH", "HDFCLIFE",
    "BPCL", "COALINDIA", "EICHERMOT", "HINDALCO", "BAJAJ-AUTO", "SBILIFE", "SHREECEM",
    "APOLLOHOSP", "TATAMOTORS", "UPL", "WIPRO"
]

# Page setup
st.set_page_config(page_title="NIFTY Dashboard", layout="wide")
st.title("📈 NIFTY 50 Live Spot Tickertape")

# Fetch and display LTPs
with st.spinner("Fetching real-time prices from NSE..."):
    ltp_data = fetch_ticker_data(nifty_symbols)
    ticker_items = " | ".join([f"{sym}: ₹{ltp_data[sym]}" for sym in ltp_data])

# Tickertape (scrolling marquee)
st.markdown(f"""
    <marquee behavior="scroll" direction="left" scrollamount="5"
             style="color: white; background: black; padding: 10px; font-size: 18px;">
        {ticker_items}
    </marquee>
""", unsafe_allow_html=True)

# Footer
st.caption("Powered by NSE India public data · Updated every ~30 seconds via cache")

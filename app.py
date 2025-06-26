# app.py (Streamlit dashboard with login + NIFTY 50 tickertape)

import streamlit as st
import streamlit_authenticator as stauth
import yaml
import json
import os
from yaml.loader import SafeLoader
from utils.nse_api import fetch_ticker_data

# Load Streamlit Auth config (admin login)
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Render login widget
name, authentication_status, username = authenticator.login(
    "Login", "main")

# Load or create users.json
USER_DB = "users.json"
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

with open(USER_DB, "r") as f:
    users = json.load(f)

ADMIN_EMAIL = list(config['credentials']['usernames'].keys())[0]

if authentication_status:
    if username == ADMIN_EMAIL:
        st.success(f"Welcome Admin {name} 👑")
        st.subheader("User Approval Panel")

        pending = {k: v for k, v in users.items() if v == "pending"}
        approved = {k: v for k, v in users.items() if v == "approved"}

        st.write("### Pending Users")
        for user in pending:
            col1, col2 = st.columns(2)
            with col1:
                st.write(user)
            with col2:
                if st.button(f"Approve {user}"):
                    users[user] = "approved"
                    with open(USER_DB, "w") as f:
                        json.dump(users, f)
                    st.experimental_rerun()

        st.write("### Approved Users")
        for user in approved:
            st.write(f"✅ {user}")

    else:
        status = users.get(username, "pending")
        if status == "approved":
            st.success(f"Welcome {name} ✨")
            st.session_state.user_email = username
            st.session_state.user_name = name
        elif status == "pending":
            st.error("Your access is pending admin approval.")
            st.stop()
        else:
            st.error("Access denied.")
            st.stop()
else:
    st.warning("Please login to continue.")
    st.stop()

# ------------------------ DASHBOARD ----------------------------

# NIFTY 50 symbols
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
st.title(f"📈 Welcome {st.session_state['user_name']} – NIFTY 50 Live Tickertape")

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

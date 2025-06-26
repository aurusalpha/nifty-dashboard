# app.py (Streamlit F&O Trade Tracker with login, admin view, and alerts)

import streamlit as st
import streamlit_authenticator as stauth
import yaml
import json
import os
import time
from yaml.loader import SafeLoader

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
name, authentication_status, username = authenticator.login("Login", "main")

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

st.set_page_config(page_title="F&O Tracker", layout="wide")

page = st.sidebar.selectbox("Select View", ["Trade Logger", "Price Alerts", "(coming soon) Position Manager"])

fno_symbols = [
    "RELIANCE", "INFY", "HDFCBANK", "ICICIBANK", "TCS", "KOTAKBANK", "SBIN", "LT",
    "ITC", "BHARTIARTL", "ASIANPAINT", "MARUTI", "SUNPHARMA", "AXISBANK", "ULTRACEMCO",
    "BAJFINANCE", "NTPC", "HINDUNILVR", "POWERGRID", "INDUSINDBK", "TITAN", "BAJAJFINSV",
    "GRASIM", "TATASTEEL", "ONGC", "JSWSTEEL", "TECHM", "CIPLA", "NESTLEIND", "ADANIENT",
    "ADANIPORTS", "DIVISLAB", "DRREDDY", "BRITANNIA", "HEROMOTOCO", "HCLTECH", "HDFCLIFE",
    "BPCL", "COALINDIA", "EICHERMOT", "HINDALCO", "BAJAJ-AUTO", "SBILIFE", "SHREECEM",
    "APOLLOHOSP", "TATAMOTORS", "UPL", "WIPRO"
]

if page == "Trade Logger":
    st.title("📝 F&O Trade Logger")
    TRADE_FILE = "trades.json"

    if not os.path.exists(TRADE_FILE):
        with open(TRADE_FILE, "w") as f:
            json.dump([], f)

    with open(TRADE_FILE, "r") as f:
        trade_data = json.load(f)

    with st.form("log_trade"):
        st.subheader("Log a new F&O Trade")
        symbol = st.selectbox("Symbol", fno_symbols)
        segment = st.radio("Segment", ["FUT", "OPT"])
        expiry = st.text_input("Expiry Date (e.g. 27JUN2025)")
        strike = st.number_input("Strike Price (for options)", value=0.0)
        option_type = st.radio("Option Type", ["CALL", "PUT"] if segment == "OPT" else ["N/A"])
        entry = st.number_input("Entry Price", min_value=0.0)
        exit = st.number_input("Exit Price (optional)", min_value=0.0, value=0.0)
        qty = st.number_input("Quantity", min_value=1)
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save Trade")

        if submitted:
            trade = {
                "user": st.session_state['user_email'],
                "symbol": symbol,
                "segment": segment,
                "expiry": expiry,
                "strike": strike if segment == "OPT" else None,
                "option_type": option_type if segment == "OPT" else None,
                "entry": entry,
                "exit": exit,
                "qty": qty,
                "notes": notes,
                "timestamp": time.time()
            }
            trade_data.append(trade)
            with open(TRADE_FILE, "w") as f:
                json.dump(trade_data, f)
            st.success("Trade saved!")

    if username == ADMIN_EMAIL:
        st.write("### All Users' Trades")
        st.dataframe(trade_data)
    else:
        st.write("### Your Trades")
        user_trades = [t for t in trade_data if t['user'] == st.session_state['user_email']]
        st.dataframe(user_trades)

elif page == "Price Alerts":
    st.title("🛎️ Price Alert Tracker")
    ALERT_FILE = "alerts.json"

    if not os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "w") as f:
            json.dump([], f)

    with open(ALERT_FILE, "r") as f:
        alert_data = json.load(f)

    with st.form("set_alert"):
        st.subheader("Set a New Price Alert")
        symbol = st.selectbox("Stock", fno_symbols)
        target_price = st.number_input("Target Price", min_value=0.0)
        direction = st.radio("Trigger When", ["Above", "Below"])
        alert_button = st.form_submit_button("Save Alert")

        if alert_button:
            alert = {
                "user": st.session_state['user_email'],
                "symbol": symbol,
                "target": target_price,
                "direction": direction,
                "triggered": False,
                "timestamp": time.time()
            }
            alert_data.append(alert)
            with open(ALERT_FILE, "w") as f:
                json.dump(alert_data, f)
            st.success("Alert saved!")

    if username == ADMIN_EMAIL:
        st.write("### All Alerts")
        st.dataframe(alert_data)
    else:
        st.write("### Your Alerts")
        user_alerts = [a for a in alert_data if a['user'] == st.session_state['user_email']]
        st.dataframe(user_alerts)

else:
    st.info("Feature coming soon ✨")

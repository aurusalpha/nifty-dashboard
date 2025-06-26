# app.py (Streamlit F&O Trade Tracker without login/auth)

import streamlit as st
import json
import os
import time

# ------------------------ DASHBOARD ----------------------------

st.set_page_config(page_title="F&O Tracker", layout="wide")

page = st.sidebar.selectbox("Select View", ["Trade Logger", "Price Alerts", "(coming soon) Position Manager"])

fno_symbols = [
    "ASHOKLEY", "BAJAJ-AUTO", "EICHERMOT", "HEROMOTOCO", "M&M", "MARUTI", "TATAMOTORS",
    "TVSMOTOR", "CUMMINSIND", "APOLLOTYRE", "AXISBANK", "HDFCBANK", "ICICIBANK", "INDUSINDBK",
    "KOTAKBANK", "SBIN", "BAJAJFINSV", "BAJFINANCE", "CHOLAFIN", "M&MFIN", "MUTHOOTFIN", "PEL",
    "SHRIRAMFIN", "HDFCLIFE", "SBILIFE", "ABCAPITAL", "MCX", "SBICARD", "BSE", "PAYTM", "BANKBARODA",
    "ACC", "AMBUJACEM", "GRASIM", "ULTRACEMCO", "AARTIIND", "DEEPAKNTR", "SRF", "TATACHEM", "UPL",
    "ASIANPAINT", "BERGEPAINT", "HAVELLS", "TITAN", "TRENT", "VOLTAS", "BRITANNIA", "GODREJCP",
    "JUBLFOOD", "TATACONSUM", "HINDUNILVR", "ITC", "BHEL", "DIXON", "INDHOTEL", "POLYCAB", "BEL",
    "HAL", "BHARTIARTL", "INDUSTOWER", "NAUKRI", "COFORGE", "HCLTECH", "INFY", "TCS", "TECHM",
    "WIPRO", "LTF", "ADANIENT", "COALINDIA", "JSWSTEEL", "TATASTEEL", "VEDL", "NMDC", "GAIL", "ONGC",
    "BPCL", "IGL", "MGL", "RELIANCE", "APOLLOHOSP", "AUROPHARMA", "DIVISLAB", "DRREDDY", "GRANULES",
    "LUPIN", "SUNPHARMA", "CIPLA", "NTPC", "POWERGRID", "TATAPOWER", "DLF", "GODREJPROP", "LT",
    "OBEROIRLTY", "ADANIPORTS", "CONCOR", "INDIGO", "ETERNAL", "NIFTY", "NIFTY BANK"
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
        from datetime import date, timedelta
import calendar

# Utility to get last Thursday of next 3 months
def get_expiry_dates():
    today = date.today()
    expiries = []
    for i in range(3):
        month = (today.month + i - 1) % 12 + 1
        year = today.year + ((today.month + i - 1) // 12)
        last_day = calendar.monthrange(year, month)[1]
        for d in range(last_day, 0, -1):
            dt = date(year, month, d)
            if dt.weekday() == 3:  # Thursday
                expiries.append(dt.strftime("%d%b%Y").upper())
                break
    return expiries

expiry_options = get_expiry_dates()
expiry = st.selectbox("Expiry Date", expiry_options)
        strike = st.number_input("Strike Price (for options)", value=0.0)
        option_type = st.radio("Option Type", ["CALL", "PUT"] if segment == "OPT" else ["N/A"])
        entry = st.number_input("Entry Price", min_value=0.0)
        exit = st.number_input("Exit Price (optional)", min_value=0.0, value=0.0)
        qty = st.number_input("Quantity", min_value=1)
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save Trade")

        if submitted:
            trade = {
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

    st.write("### All Trades")
    st.dataframe(trade_data)

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

    st.write("### All Alerts")
    st.dataframe(alert_data)

else:
    st.info("Feature coming soon ✨")

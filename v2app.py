# app.py (Streamlit F&O Trade Tracker without login/auth)

import streamlit as st
import json
import os
import time

# ------------------------ DASHBOARD ----------------------------

st.set_page_config(page_title="F&O Tracker", layout="wide")

page = st.sidebar.selectbox("Select View", ["Trade Logger", "Price Alerts", "(coming soon) Position Manager"])

fno_lot_sizes = {
    "ASHOKLEY": 3000, "BAJAJ-AUTO": 125, "EICHERMOT": 175, "HEROMOTOCO": 300, "M&M": 700, "MARUTI": 100, "TATAMOTORS": 1425,
    "TVSMOTOR": 1700, "CUMMINSIND": 600, "APOLLOTYRE": 3000, "AXISBANK": 1200, "HDFCBANK": 550, "ICICIBANK": 1375,
    "INDUSINDBK": 800, "KOTAKBANK": 400, "SBIN": 1500, "BAJAJFINSV": 200, "BAJFINANCE": 300, "CHOLAFIN": 2000,
    "M&MFIN": 3500, "MUTHOOTFIN": 425, "PEL": 500, "SHRIRAMFIN": 625, "HDFCLIFE": 1500, "SBILIFE": 900,
    "ABCAPITAL": 3900, "MCX": 400, "SBICARD": 950, "BSE": 525, "PAYTM": 800, "BANKBARODA": 5400, "ACC": 500,
    "AMBUJACEM": 1800, "GRASIM": 475, "ULTRACEMCO": 300, "AARTIIND": 1050, "DEEPAKNTR": 550, "SRF": 150,
    "TATACHEM": 900, "UPL": 1300, "ASIANPAINT": 300, "BERGEPAINT": 1800, "HAVELLS": 1000, "TITAN": 375,
    "TRENT": 700, "VOLTAS": 850, "BRITANNIA": 200, "GODREJCP": 1000, "JUBLFOOD": 500, "TATACONSUM": 850,
    "HINDUNILVR": 300, "ITC": 3200, "BHEL": 10500, "DIXON": 150, "INDHOTEL": 3000, "POLYCAB": 300, "BEL": 7600,
    "HAL": 300, "BHARTIARTL": 950, "INDUSTOWER": 2800, "NAUKRI": 150, "COFORGE": 200, "HCLTECH": 700,
    "INFY": 600, "TCS": 150, "TECHM": 700, "WIPRO": 1600, "LTF": 5000, "ADANIENT": 500, "COALINDIA": 2700,
    "JSWSTEEL": 1050, "TATASTEEL": 4250, "VEDL": 3000, "NMDC": 6700, "GAIL": 5400, "ONGC": 3850, "BPCL": 1800,
    "IGL": 1375, "MGL": 550, "RELIANCE": 250, "APOLLOHOSP": 125, "AUROPHARMA": 850, "DIVISLAB": 175,
    "DRREDDY": 125, "GRANULES": 2250, "LUPIN": 650, "SUNPHARMA": 1000, "CIPLA": 650, "NTPC": 5700,
    "POWERGRID": 2700, "TATAPOWER": 4050, "DLF": 1650, "GODREJPROP": 425, "LT": 300, "OBEROIRLTY": 700,
    "ADANIPORTS": 1250, "CONCOR": 1000, "INDIGO": 300, "ETERNAL": 900, "NIFTY": 50, "NIFTY BANK": 15
}

fno_symbols = list(fno_lot_sizes.keys())

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
        
        expiry = st.selectbox("Expiry Date", ["31JUL2025", "28AUG2025", "25SEP2025"])
        strike = st.number_input("Strike Price (for options)", value=0.0)
        option_type = st.selectbox("Option Type", ["CE", "PE"] if segment == "OPT" else ["N/A"])
        entry = st.number_input("Entry Price", min_value=0.0)
        exit = st.number_input("Exit Price (optional)", min_value=0.0, value=0.0)
        lots = st.number_input("Lots", min_value=1)
        lot_size = fno_lot_sizes.get(symbol, 1)
        final_qty = lots * lot_size
        st.number_input("Final Quantity", value=final_qty, disabled=True)
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
                "qty": lots * fno_lot_sizes.get(symbol, 1),
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

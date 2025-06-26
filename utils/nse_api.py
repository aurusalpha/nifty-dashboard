# utils/nse_api.py → NSE India spot price fetcher with caching

import requests
import time
import random
import os
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/",
}

NSE_BASE_URL = "https://www.nseindia.com/api/quote-equity?symbol={}"  # symbol in caps
CACHE_FILE = "nse_cache.json"
CACHE_EXPIRY = 30  # seconds

# NIFTY 50 stock symbols (spot)
SYMBOL_MAP = {
    "RELIANCE": "RELIANCE", "INFY": "INFY", "HDFCBANK": "HDFCBANK", "ICICIBANK": "ICICIBANK",
    "TCS": "TCS", "KOTAKBANK": "KOTAKBANK", "SBIN": "SBIN", "LT": "LT", "ITC": "ITC",
    "BHARTIARTL": "BHARTIARTL", "ASIANPAINT": "ASIANPAINT", "MARUTI": "MARUTI", "SUNPHARMA": "SUNPHARMA",
    "AXISBANK": "AXISBANK", "ULTRACEMCO": "ULTRACEMCO", "BAJFINANCE": "BAJFINANCE", "NTPC": "NTPC",
    "HINDUNILVR": "HINDUNILVR", "POWERGRID": "POWERGRID", "INDUSINDBK": "INDUSINDBK", "TITAN": "TITAN",
    "BAJAJFINSV": "BAJAJFINSV", "GRASIM": "GRASIM", "TATASTEEL": "TATASTEEL", "ONGC": "ONGC",
    "JSWSTEEL": "JSWSTEEL", "TECHM": "TECHM", "CIPLA": "CIPLA", "NESTLEIND": "NESTLEIND",
    "ADANIENT": "ADANIENT", "ADANIPORTS": "ADANIPORTS", "DIVISLAB": "DIVISLAB", "DRREDDY": "DRREDDY",
    "BRITANNIA": "BRITANNIA", "HEROMOTOCO": "HEROMOTOCO", "HCLTECH": "HCLTECH", "HDFCLIFE": "HDFCLIFE",
    "BPCL": "BPCL", "COALINDIA": "COALINDIA", "EICHERMOT": "EICHERMOT", "HINDALCO": "HINDALCO",
    "BAJAJ-AUTO": "BAJAJ-AUTO", "SBILIFE": "SBILIFE", "SHREECEM": "SHREECEM", "APOLLOHOSP": "APOLLOHOSP",
    "TATAMOTORS": "TATAMOTORS", "UPL": "UPL", "WIPRO": "WIPRO"
}
import requests
import time
import random
import json
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/",
}

BASE_URL = "https://www.nseindia.com/api/quote-equity?symbol={}"

CACHE_FILE = "nse_cache.json"
CACHE_EXPIRY = 30  # seconds

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def get_ltp(symbol):
    cache = load_cache()
    now = time.time()
    if symbol in cache and now - cache[symbol]['timestamp'] < CACHE_EXPIRY:
        return cache[symbol]['ltp']
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        session.get("https://www.nseindia.com")  # Establish cookies
        time.sleep(random.uniform(0.5, 1.2))
        response = session.get(BASE_URL.format(symbol))
        if response.status_code == 200:
            data = response.json()
            ltp = data.get("priceInfo", {}).get("lastPrice")
            if ltp:
                cache[symbol] = {"ltp": ltp, "timestamp": now}
                save_cache(cache)
                return ltp
        return None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def fetch_ticker_data(symbols):
    data = {}
    for sym in symbols:
        ltp = get_ltp(sym)
        data[sym] = ltp if ltp else "—"
    return data

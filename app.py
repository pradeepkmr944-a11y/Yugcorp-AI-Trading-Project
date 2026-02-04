
import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="AI Trading App", layout="wide")
st.title("AI Stock Analysis Dashboard")

symbol = st.text_input("Enter Stock Symbol (Example: RELIANCE.NS, AAPL)", "RELIANCE.NS")

if symbol:
    try:
        data = yf.download(symbol, period="1y", progress=False)
        data = data.dropna()

        if data.empty or "Close" not in data.columns:
            st.error("No valid stock data found. Try another symbol.")
            st.stop()

        close_series = data["Close"].astype(float).squeeze()

        data["RSI"] = ta.momentum.RSIIndicator(close=close_series).rsi()
        data["SMA20"] = close_series.rolling(20).mean()
        data["SMA50"] = close_series.rolling(50).mean()

        st.subheader("Latest Stock Data")
        st.write(data.tail())

        st.subheader("Price Chart")
        st.line_chart(data["Close"])

        st.subheader("RSI Indicator")
        st.line_chart(data["RSI"])

    except Exception as e:
        st.error(f"Error loading stock data: {e}")

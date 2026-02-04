
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objects as go

st.set_page_config(page_title="Full AI Investment Platform", layout="wide")
st.title("📈 Full AI Investment Platform (Swing + Long Term)")

symbol = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

if symbol:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        data = yf.download(symbol, period="2y", progress=False)
        data = data.dropna()

        if data.empty:
            st.error("No stock data found.")
            st.stop()

        close = data["Close"].astype(float)

        data["RSI"] = ta.momentum.RSIIndicator(close=close).rsi()
        data["SMA20"] = close.rolling(20).mean()
        data["SMA50"] = close.rolling(50).mean()
        data["MACD"] = ta.trend.MACD(close=close).macd()

        latest = data.iloc[-1]
        rsi = latest["RSI"]

        swing_signal = "HOLD"
        if rsi < 35:
            swing_signal = "BUY"
        elif rsi > 65:
            swing_signal = "SELL"

        pe = info.get("trailingPE", None)
        market_cap = info.get("marketCap", None)

        long_term = "NEUTRAL"
        if pe and pe < 25:
            long_term = "GOOD FOR LONG TERM"

        st.subheader("📊 AI Recommendations")
        col1, col2 = st.columns(2)
        col1.metric("Swing Signal", swing_signal)
        col2.metric("Long Term Rating", long_term)

        st.subheader("📘 Fundamental Analysis")
        st.write({
            "Market Cap": market_cap,
            "P/E Ratio": pe,
            "EPS": info.get("trailingEps"),
            "Dividend Yield": info.get("dividendYield"),
        })

        st.subheader("🕯 Candlestick Chart")
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"]
        )])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📈 RSI Indicator")
        st.line_chart(data["RSI"])

        st.subheader("📉 MACD Indicator")
        st.line_chart(data["MACD"])

    except Exception as e:
        st.error(f"Error: {e}")

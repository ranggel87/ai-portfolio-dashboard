import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="AI Crypto Portfolio Advisor", layout="wide")

st.title("📊 AI Crypto Portfolio Advisor")
st.subheader("📁 Preview Data")

uploaded_file = st.file_uploader("Upload CSV transaksi kamu (Binance/Bitget manual export)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Preview awal
    st.write("### 🔍 File data:")
    st.dataframe(df)

    # Pastikan header kolom sudah benar
    required_cols = {"Date", "Coin", "Type", "Amount", "Price", "Exchange", "Fee"}
    if not required_cols.issubset(df.columns):
        st.warning(f"⚠️ Kolom wajib tidak lengkap. Harus ada: {', '.join(required_cols)}")
        st.stop()

    # Konversi tipe data
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    df["Fee"] = pd.to_numeric(df["Fee"], errors="coerce").fillna(0)

    # Ringkasan per coin
    st.subheader("📦 Token Summary")
    token_summary = df.groupby("Coin")["Amount"].sum().reset_index()
    token_summary.rename(columns={"Amount": "Total Amount"}, inplace=True)
    st.dataframe(token_summary)

    # Mapping Coin ke CoinGecko ID
    coingecko_mapping = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "BNB": "binancecoin",
        "ARB": "arbitrum",
        "OP": "optimism"
        # Tambahkan sesuai kebutuhan
    }
    token_summary["CoinGecko_ID"] = token_summary["Coin"].map(coingecko_mapping)

    def get_token_prices(tokens, vs_currency="usd"):
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(tokens),
            "vs_currencies": vs_currency
        }
        try:
            res = requests.get(url, params=params)
            return res.json()
        except:
            return {}

    prices = get_token_prices(token_summary["CoinGecko_ID"].dropna().tolist())

    # Ambil harga live dan hitung estimasi nilai
    token_summary["Current_Price_USD"] = token_summary["CoinGecko_ID"].map(lambda x: prices.get(x, {}).get("usd", 0))
    token_summary["Est_Value_USD"] = token_summary["Total Amount"] * token_summary["Current_Price_USD"]

    # Tampilkan nilai portofolio
    st.subheader("💰 Portfolio Value (Live)")
    st.dataframe(token_summary[["Coin", "Total Amount", "Current_Price_USD", "Est_Value_USD"]])

    # Pie chart
    st.subheader("📊 Portfolio Allocation")
    fig = px.pie(token_summary, names="Coin", values="Est_Value_USD", title="Distribusi Aset dalam USD")
    st.plotly_chart(fig, use_container_width=True)

    # Insight AI Rebalancing
    st.subheader("🤖 AI Rebalancing Suggestion")
    total_portfolio_value = token_summary["Est_Value_USD"].sum()
    equal_weight = total_portfolio_value / len(token_summary)
    token_summary["Ideal_Value_USD"] = equal_weight
    token_summary["Diff_to_Balance"] = token_summary["Est_Value_USD"] - equal_weight
    st.dataframe(token_summary[["Coin", "Est_Value_USD", "Ideal_Value_USD", "Diff_to_Balance"]])
else:
    st.info("Silakan upload file CSV transaksi kamu.")

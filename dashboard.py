import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="AI Crypto Portfolio Advisor", layout="wide")
st.title("📊 AI Crypto Portfolio Advisor")

st.subheader("📄 Preview Data")
st.caption("Upload CSV transaksi kamu (Binance/Bitget manual export)")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Normalisasi kolom
    df.columns = df.columns.str.strip().str.title()

    # Tampilkan preview
    st.dataframe(df)

    # Token Summary
    st.subheader("📊 Token Summary")
    try:
        summary = df.groupby("Coin")["Amount"].sum().reset_index()
        summary.columns = ["Coin", "Total Amount"]
        st.dataframe(summary)
    except Exception as e:
        st.error(f"Gagal menghitung summary token: {e}")

    # Integrasi CoinGecko
    st.subheader("💰 Estimasi Nilai Portofolio (Live Price)")

    def get_price(symbol):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
            r = requests.get(url).json()
            return r[symbol]["usd"]
        except:
            return None

    # Pemetaan nama Coin ke ID CoinGecko
    mapping = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "BNB": "binancecoin",
        "ARB": "arbitrum",
        "TIA": "celestia",
        "TAO": "bittensor",
        "APT": "aptos"
        # tambah sesuai kebutuhan
    }

    if "Coin" in df.columns and "Amount" in df.columns:
        portfolio = []
        for row in summary.itertuples():
            coin = row.Coin
            amount = row._2
            if coin in mapping:
                price = get_price(mapping[coin])
                value = round(amount * price, 2) if price else 0
                portfolio.append({
                    "Coin": coin,
                    "Amount": amount,
                    "Price": price,
                    "Value ($)": value
                })

        port_df = pd.DataFrame(portfolio)
        st.dataframe(port_df)

        total_value = port_df["Value ($)"].sum()
        st.success(f"💼 Total Portofolio Saat Ini: **${total_value:,.2f}**")

        # Pie Chart
        fig = px.pie(port_df, values='Value ($)', names='Coin', title='Distribusi Portofolio')
        st.plotly_chart(fig, use_container_width=True)

        # Insight sederhana (AI-like rebalancing suggestion)
        st.subheader("🧠 Insight Rebalancing (Sederhana)")
        target_pct = 100 / len(port_df)  # Equal Weighting
        port_df["Current %"] = port_df["Value ($)"] / total_value * 100
        port_df["Target %"] = target_pct
        port_df["Delta %"] = port_df["Target %"] - port_df["Current %"]
        st.dataframe(port_df[["Coin", "Current %", "Target %", "Delta %"]])

        st.markdown("📌 **Saran:** Positif artinya perlu tambah koin tersebut, negatif artinya kelebihan alokasi.")

else:
    st.warning("Silakan upload file CSV transaksi terlebih dahulu.")

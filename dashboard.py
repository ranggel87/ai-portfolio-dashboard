import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Crypto Portfolio Advisor", layout="wide")
st.title("📊 AI Crypto Portfolio Advisor")

st.sidebar.header("📁 Upload Portfolio CSV")
uploaded_file = st.sidebar.file_uploader("Upload your CSV", type=["csv"])

if uploaded_file:
    try:
        # Baca file dengan pemisah titik koma (;)
        df = pd.read_csv(uploaded_file, sep=';')
        st.subheader("📄 Preview Data")
        st.dataframe(df.head())

        # Coba deteksi kolom kunci
        coin_col = None
        amount_col = None

        for col in df.columns:
            if str(col).lower() in ["coin", "asset", "symbol", "cur.", "cur", "token"]:
                coin_col = col
            if str(col).lower() in ["amount", "buy", "sell", "qty", "quantity"]:
                amount_col = col

        if coin_col and amount_col:
            df = df.rename(columns={coin_col: "Coin", amount_col: "Amount"})
            token_summary = df.groupby("Coin")["Amount"].sum().reset_index()
            st.subheader("📈 Token Summary")
            st.dataframe(token_summary)
        else:
            st.warning("⚠️ Kolom Coin dan Amount tidak ditemukan otomatis. Harap pilih file lain atau edit header.")

    except Exception as e:
        st.error(f"❌ Error saat membaca file: {e}")
else:
    st.info("⬆️ Silakan upload file CSV terlebih dahulu.")

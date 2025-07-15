import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="AI Crypto Portfolio Advisor", layout="wide")
st.title("📊 AI Crypto Portfolio Advisor")

st.subheader("📄 Preview Data")

uploaded_file = st.file_uploader("Upload CSV transaksi kamu (Binance/Bitget manual export)", type=["csv"])

if uploaded_file is not None:
    # Deteksi delimiter otomatis
    sample = uploaded_file.read(1024).decode()
    delimiter = ";" if sample.count(";") > sample.count(",") else ","
    uploaded_file.seek(0)

    # Baca file CSV
    df = pd.read_csv(uploaded_file, delimiter=delimiter)

    # Preview
    st.dataframe(df.head())

    # Kolom penting: Coin dan Amount
    missing_cols = []
    for col in ["Coin", "Amount"]:
        if col not in df.columns:
            missing_cols.append(col)

    if missing_cols:
        st.warning(f"⚠️ Kolom {', '.join(missing_cols)} tidak ditemukan otomatis. Pilih kolom manual:")

        # Dropdown manual pemetaan kolom
        coin_col = st.selectbox("Pilih kolom Coin:", options=df.columns)
        amount_col = st.selectbox("Pilih kolom Amount:", options=df.columns)
    else:
        coin_col = "Coin"
        amount_col = "Amount"

    # Tampilkan ringkasan token
    st.subheader("📊 Token Summary")
    try:
        token_summary = df.groupby(coin_col)[amount_col].sum().reset_index()
        token_summary.columns = ["Coin", "Total Amount"]
        st.dataframe(token_summary)
    except Exception as e:
        st.error("Terjadi error saat membuat ringkasan. Pastikan file CSV valid.")
        st.exception(e)

else:
    st.info("⬆️ Silakan upload file CSV kamu untuk mulai.")

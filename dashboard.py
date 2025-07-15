import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Crypto Portfolio Advisor", layout="wide")
st.title("📊 AI Crypto Portfolio Advisor")

# --- Upload Section ---
st.sidebar.header("📁 Upload Your CSV File")
uploaded_file = st.sidebar.file_uploader("Upload your portfolio CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Preview Data")
    st.dataframe(df.head())

    # --- Token Summary ---
    st.subheader("📈 Token Summary")
    token_summary = df.groupby("Coin")["Amount"].sum().reset_index()
    st.dataframe(token_summary)

    # --- Placeholder: Narasi & Rebalancing (Coming Soon) ---
    st.subheader("🧠 Narasi & Rebalancing Insight (Coming Soon)")
    st.info("Modul analisis narasi dan saran alokasi sedang dikembangkan.")
else:
    st.warning("Silakan upload file CSV untuk memulai.")

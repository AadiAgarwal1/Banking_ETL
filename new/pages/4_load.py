import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("📊 Load / Visualize")

if "transformed" not in st.session_state:
    st.warning("⚠️ Please transform the data first.")
else:
    df = st.session_state["transformed"]

    if "account_type" in df.columns and "balance" in df.columns:
        st.subheader("Average Balance by Account Type")
        chart = df.groupby("account_type")["balance"].mean()
        st.bar_chart(chart)

    if "created_at" in df.columns:
        st.subheader("Customer Creation by Year")
        df["year"] = pd.to_datetime(df["created_at"]).dt.year
        chart = df.groupby("year").size()
        st.line_chart(chart)

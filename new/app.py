import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="ETL Dashboard",
    page_icon="🧊",
    layout="wide"
)

st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        font-weight: bold;
    }
    .blue {
        color: #1f77b4;
    }
    .center {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 6])
with col1:
    st.image("assets/logo.png", width=80)  # Optional logo
with col2:
    st.markdown('<div class="big-font center">WHERE DATA <span class="blue">DOES MORE</span></div>', unsafe_allow_html=True)
    st.write("Build your ETL pipeline with ease using SQL + Local Files + Python Transformations")

st.markdown("### Get started using the sidebar navigation ➡️")

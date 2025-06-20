import streamlit as st

st.set_page_config(page_title="ETL Dashboard", page_icon="🧊", layout="wide")

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #1f77b4;
        margin-bottom: 0.25em;
    }
    .hero-sub {
        font-size: 20px;
        color: #cbd5e1;
        margin-bottom: 1em;
    }
    .callout {
        background-color: #1e293b;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-top: 20px;
        font-size: 17px;
        color: #e2e8f0;
        border-left: 6px solid #22c55e;
    }
    .features {
        font-size: 17px;
        color: #e2e8f0;
        margin-top: 30px;
        line-height: 2.2em;
    }
    .features span {
        display: inline-block;
        min-width: 280px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
col1, col2 = st.columns([1, 6])
with col1:
    st.image("assets/logo.png", width=80)
with col2:
    st.markdown('<div class="hero-title">ETL Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">⚙️ Build seamless pipelines using <span style="color:#22c55e;">SQL + Excel + Python</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ------------------- CALLOUT -------------------
st.markdown("""
<div class="callout">
    📌 <strong>Get Started:</strong> Use the sidebar to <span style="color:#22c55e;">Connect</span>, 
    <span style="color:#22c55e;">Extract</span>, and <span style="color:#22c55e;">Transform</span> your data — all in one intuitive interface.
</div>
""", unsafe_allow_html=True)

# ------------------- FEATURES -------------------
st.markdown("""
<div class="features">
    <span>🤝 Connect to MySQL or Snowflake</span>
    <span>📁 Extract from Tables + Excel</span><br>
    <span>🧠 Apply Smart Transformations</span>
    <span>📊 Visualize with Interactive Charts</span>
</div>
""", unsafe_allow_html=True)

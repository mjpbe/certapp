import streamlit as st
import pandas as pd
import database as db
from theme import apply_theme

apply_theme()

# LOGIN CHECK
if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in first.")
    st.stop()

# TOP-RIGHT USER BOX
st.markdown(f"""
<div style="position: fixed; top: 10px; right: 20px; 
            background: #eef3ff; padding: 8px 15px; 
            border-radius: 8px; font-size: 14px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15); z-index: 1000;">
    👤 {st.session_state.user['username']}<br>
    ✉ {st.session_state.user['email']}
</div>
""", unsafe_allow_html=True)

st.title("🔍 Search Certificates")

year = st.selectbox("Select Year", [2024, 2025, 2026])
search = st.text_input("Search")

df = db.get_certs(year).drop(columns=["id"])

if search:
    df = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]

st.dataframe(df, use_container_width=True)

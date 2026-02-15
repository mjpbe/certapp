import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    /* Sidebar background + text */
    [data-testid="stSidebar"] {
        background-color: #e6f0ff !important;
    }
    [data-testid="stSidebar"] * {
        color: #003366 !important;
    }

    /* Freeze headers */
    [data-testid="stDataFrame"] table thead tr th,
    [data-testid="stDataEditor"] table thead tr th {
        position: sticky;
        top: 0;
        background-color: #f0f2f6;
        z-index: 3;
    }
    </style>
    """, unsafe_allow_html=True)

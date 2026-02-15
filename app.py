import streamlit as st
import database as db
from theme import apply_theme

st.set_page_config(page_title="Certificate Register", layout="wide")

# Apply global theme
apply_theme()

# ---------------------------
# SESSION STATE INIT
# ---------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------------------
# LOGIN SCREEN
# ---------------------------
if st.session_state.user is None:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = db.authenticate(username, password)
        if user:
            st.session_state.user = {"username": user[1], "email": user[2]}
            st.rerun()
        else:
            st.error("Invalid credentials")

else:
    # ---------------------------
    # TOP-RIGHT USER INFO
    # ---------------------------
    st.markdown(f"""
    <div style="position: fixed; top: 10px; right: 20px; 
                background: #eef3ff; padding: 8px 15px; 
                border-radius: 8px; font-size: 14px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15); z-index: 1000;">
        👤 {st.session_state.user['username']}<br>
        ✉ {st.session_state.user['email']}
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------
    # MAIN HOME PAGE CONTENT
    # ---------------------------
    st.title("📄 Certificate Register System")

    st.write(f"Welcome, **{st.session_state.user['username']}**")
    st.write("Use the sidebar on the left to navigate.")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

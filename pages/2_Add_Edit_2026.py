import streamlit as st
import pandas as pd
from datetime import datetime
import database as db
from theme import apply_theme

apply_theme()

# ---------------------------
# LOGIN PROTECTION
# ---------------------------
if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in first.")
    st.stop()

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
# PAGE TITLE
# ---------------------------
st.title("✏ Add / Edit Certificates – 2026")

user_email = st.session_state.user["email"]

# ---------------------------
# LOAD DATA
# ---------------------------
df = db.get_certs(2026)

# Highlighting
if "highlight_certnr" not in st.session_state:
    st.session_state.highlight_certnr = None

df["Status"] = ""
if st.session_state.highlight_certnr:
    df.loc[df["Certnr"] == st.session_state.highlight_certnr, "Status"] = "🟢 Updated"

# ---------------------------
# ADD NEW CERTIFICATE
# ---------------------------
st.subheader("➕ Add New Certificate")

if st.button("Add New Certificate"):
    st.session_state.show_add_form = True

if st.session_state.get("show_add_form", False):

    with st.form("add_cert_form", clear_on_submit=False):

        leverancier = st.text_input("Leverancier")
        artikel = st.text_input("Artikel")
        aantal = st.number_input("Aantal", min_value=1, step=1)
        powp = st.text_input("POWP")

        datum = st.date_input(
            "Datum Ontvangen",
            value=datetime(2026, 1, 1),
            min_value=datetime(2026, 1, 1),
            max_value=datetime(2026, 12, 31)
        )

        ontvdoor = user_email

        submitted = st.form_submit_button("Save Certificate")

        if submitted:
            datum_str = datum.strftime("%d/%m/%Y")

            new_certnr = db.insert_cert(
                2026, leverancier, artikel, int(aantal), powp, datum_str, ontvdoor
            )

            st.session_state.highlight_certnr = new_certnr
            st.session_state.show_add_form = False
            st.rerun()

st.markdown("---")

# ---------------------------
# EDIT EXISTING CERTIFICATES
# ---------------------------
st.subheader("✏ Edit Existing Certificates")

id_map = df[["id"]].copy()

df["DatumOntv"] = pd.to_datetime(df["DatumOntv"], format="%d/%m/%Y", errors="coerce")

df_display = df.drop(columns=["id"])

column_config = {
    "Certnr": st.column_config.TextColumn("Certnr", disabled=True),
    "Leverancier": st.column_config.TextColumn("Leverancier"),
    "Artikel": st.column_config.TextColumn("Artikel"),
    "Aantal": st.column_config.NumberColumn("Aantal", min_value=1),
    "POWP": st.column_config.TextColumn("POWP"),
    "DatumOntv": st.column_config.DateColumn(
        "DatumOntv",
        min_value=datetime(2026, 1, 1),
        max_value=datetime(2026, 12, 31)
    ),
    "Ontvdoor": st.column_config.TextColumn("Ontvdoor", disabled=True),
    "NameCertificateinPDF": st.column_config.TextColumn("NameCertificateinPDF", disabled=True),
    "Status": st.column_config.TextColumn("Status", disabled=True),
}

edited_df = st.data_editor(
    df_display,
    column_config=column_config,
    use_container_width=True,
    hide_index=True
)

edited_df = edited_df.join(id_map)

# ---------------------------
# SAVE CHANGES
# ---------------------------
if st.button("Save Changes"):
    last_certnr = None

    for idx, row in edited_df.iterrows():

        datum_str = (
            row["DatumOntv"].strftime("%d/%m/%Y")
            if pd.notna(row["DatumOntv"])
            else ""
        )

        new_namepdf = f"{row['Certnr']} {row['Leverancier']} {row['POWP']}"

        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE cert
            SET Leverancier=?, Artikel=?, Aantal=?, POWP=?, DatumOntv=?, Ontvdoor=?, NameCertificateinPDF=?
            WHERE id=?
        """, (
            row["Leverancier"], row["Artikel"], int(row["Aantal"]),
            row["POWP"], datum_str, row["Ontvdoor"], new_namepdf, row["id"]
        ))
        conn.commit()
        conn.close()

        last_certnr = row["Certnr"]

    st.session_state.highlight_certnr = last_certnr
    st.success(f"Certificate {last_certnr} updated!")
    st.rerun()

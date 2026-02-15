import sqlite3
import pandas as pd

DB_NAME = "cert.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# ----------------------
# Authentication
# ----------------------
def authenticate(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

# ----------------------
# Get certificates
# ----------------------
def get_certs(year):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, Certnr, Leverancier, Artikel, Aantal, POWP, DatumOntv, Ontvdoor, NameCertificateinPDF
        FROM cert
        WHERE Year=?
        ORDER BY id
    """, (year,))
    rows = cur.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=[
        "id","Certnr","Leverancier","Artikel","Aantal","POWP",
        "DatumOntv","Ontvdoor","NameCertificateinPDF"
    ])
    return df

# ----------------------
# Generate next Certnr
# ----------------------
def generate_certnr(year):
    conn = get_connection()
    cur = conn.cursor()
    prefix = f"BEC{str(year)[-2:]}"
    cur.execute("SELECT Certnr FROM cert WHERE Year=? ORDER BY id DESC LIMIT 1", (year,))
    last = cur.fetchone()
    conn.close()

    if last:
        number = int(last[0].split("-")[1]) + 1
    else:
        number = 1

    return f"{prefix}-{number:04d}"

# ----------------------
# Insert certificate
# ----------------------
def insert_cert(year, leverancier, artikel, aantal, powp, datum, ontvdoor):
    conn = get_connection()
    cur = conn.cursor()

    certnr = generate_certnr(year)
    namepdf = f"{certnr} {leverancier} {powp}"

    cur.execute("""
        INSERT INTO cert
        (Certnr,Year,Leverancier,Artikel,Aantal,POWP,DatumOntv,Ontvdoor,NameCertificateinPDF)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (certnr, year, leverancier, artikel, aantal, powp, datum, ontvdoor, namepdf))

    conn.commit()
    conn.close()
    return certnr

# ----------------------
# Update certificate
# ----------------------
def update_cert(id_value, leverancier, artikel, aantal, powp, datum, ontvdoor):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE cert
        SET Leverancier=?, Artikel=?, Aantal=?, POWP=?, DatumOntv=?, Ontvdoor=?
        WHERE id=?
    """, (leverancier, artikel, aantal, powp, datum, ontvdoor, id_value))

    conn.commit()
    conn.close()

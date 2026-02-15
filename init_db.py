import sqlite3

DB_NAME = "cert.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT,
        created_at TEXT
    )
    """)

    # CERT TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cert (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Certnr TEXT UNIQUE,
        Year INTEGER,
        Leverancier TEXT,
        Artikel TEXT,
        Aantal INTEGER,
        POWP TEXT,
        DatumOntv TEXT,
        Ontvdoor TEXT,
        NameCertificateinPDF TEXT
    )
    """)

    # INSERT USERS
    users = [
        ("MAS","mas@bes.nl","mas!","2026-02-14 10:46:45"),
        ("RGS","rgs@bes.nl","rgs!","2026-02-14 10:46:45"),
        ("MPZ","mpz@bes.nl","mpz!","2026-02-14 10:46:45")
    ]
    cur.executemany("""
    INSERT OR IGNORE INTO users (username,email,password,created_at)
    VALUES (?,?,?,?)
    """, users)

    # INSERT CERT DATA
    cert_data = [
        ("BEC24-0001",2024,"Jumbo","M-00-52-707-C",1,"313329","13/01/2024","MAS"),
        ("BEC24-0002",2024,"AlbertHeijn","M-00-52-805-AB",2,"341349","14/01/2024","MPZ"),
        ("BEC24-0003",2024,"Plus","M-00-52-805-AR",18,"313329","15/01/2024","MAS"),
        ("BEC24-0004",2024,"Aldi","24008.10.09-R0",40,"311329","16/01/2024","RGS"),
        ("BEC24-0005",2024,"Lidl","M-00-52-807-Z",40,"397329","17/01/2024","MAS"),
        ("BEC25-0001",2025,"Jumbo","14008.10.09-R0",1,"353190","25/01/2025","MAS"),
        ("BEC25-0002",2025,"AlbertHeijn","M-00-32-172-Z",37,"313329","21/02/2025","RGS"),
        ("BEC25-0003",2025,"Plus","M-00-52-377-AR",2,"383329","24/08/2025","MPZ"),
        ("BEC25-0004",2025,"Aldi","M-00-52-538-AR",3,"313382","29/09/2025","RGS"),
        ("BEC25-0005",2025,"Lidl","M-00-52-539-AR",2,"313323","16/11/2025","MAS"),
        ("BEC26-0001",2026,"Jumbo","M-00-52-707-C",1,"313329","13/01/2026","MAS"),
        ("BEC26-0002",2026,"AlbertHeijn","M-00-52-805-AB",2,"341349","14/01/2026","MPZ"),
        ("BEC26-0003",2026,"Plus","M-00-52-805-AR",18,"313329","15/01/2026","MAS"),
        ("BEC26-0004",2026,"Aldi","24008.10.09-R0",40,"311329","16/01/2026","RGS"),
        ("BEC26-0005",2026,"Lidl","M-00-52-807-Z",40,"397329","17/01/2026","MAS"),
    ]

    for c in cert_data:
        namepdf = f"{c[0]} {c[2]} {c[5]}"
        cur.execute("""
        INSERT OR IGNORE INTO cert
        (Certnr,Year,Leverancier,Artikel,Aantal,POWP,DatumOntv,Ontvdoor,NameCertificateinPDF)
        VALUES (?,?,?,?,?,?,?,?,?)
        """, (c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],namepdf))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")

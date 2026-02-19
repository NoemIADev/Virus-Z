import sqlite3

DB_NAME = "alertes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # table status (déjà existante)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY,
            last_count INTEGER,
            last_state TEXT
        )
    """)

    # table subscribers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    # table de liaison

    

    cursor.execute("SELECT COUNT(*) FROM status")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO status (id, last_count, last_state) VALUES (1, 0, 'NORMAL')"
        )

    conn.commit()
    conn.close()

def get_last_state():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT last_state FROM status WHERE id = 1")
    state = cursor.fetchone()[0]
    conn.close()
    return state


def update_state(count, state):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE status SET last_count = ?, last_state = ? WHERE id = 1",
        (count, state),
    )
    conn.commit()
    conn.close()


def add_subscriber(nom, prenom, email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO subscribers (nom, prenom, email) VALUES (?, ?, ?)",
            (nom, prenom, email)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_subscribers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM subscribers")
    emails = [row[0] for row in cursor.fetchall()]
    conn.close()
    return emails
import sqlite3

DB_PATH = "database.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def add_user(user_id, username):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        conn.commit()

def get_film_by_code(code):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM films WHERE code = ?", (code,))
        return cur.fetchone()

def increment_download(code):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE films SET downloads = downloads + 1 WHERE code = ?", (code,))
        conn.commit()


def get_next_code():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT MAX(code) FROM films")
        last = cur.fetchone()[0]
        return (last or 0) + 1

def add_film(code, title, message_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO films (code, title, message_id) VALUES (?, ?, ?)",
            (code, title, message_id)
        )
        conn.commit()


def get_users_count():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        return cur.fetchone()[0]


def get_users():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM users
            ORDER BY id DESC
            LIMIT 20
        """)
        return cur.fetchall()

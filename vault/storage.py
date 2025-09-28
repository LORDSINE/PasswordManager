import sqlite3
from vault.crypto import encrypt, decrypt

class VaultStorage:
    def __init__(self, db_path="vault.db"):
        self.db_path = db_path
        self.init_db()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT UNIQUE,
            username TEXT,
            password TEXT
            )
            """)
            conn.commit()

    def add_entry(self, service, username, password):
        enc_pwd = encrypt(password)
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO vault (service, username, password)
            VALUES (?, ?, ?)
            ON CONFLICT(service) DO UPDATE SET
            username = excluded.username,
                password = excluded.password
            """, (service, username, enc_pwd))
            conn.commit()

    def get_entry(self, service):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT username, password FROM vault WHERE service = ?", (service,))
            row = cur.fetchone()
            if row:
                username, enc_pwd = row
                return username, decrypt(enc_pwd)
            return None

    def list(self):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT service FROM vault")
            return [row[0] for row in cur.fetchall()]

    def delete(self, service):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE from vault WHERE service = ?", (service,))
            conn.commit()

import sqlite3
from datetime import datetime

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect("password_history.db")
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME,
                strength_score INTEGER,
                is_breached BOOLEAN
            )
        """)
        self.conn.commit()

    def add_record(self, strength_score, is_breached=False):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO history (timestamp, strength_score, is_breached)
            VALUES (?, ?, ?)
        """, (timestamp, strength_score, is_breached))
        self.conn.commit()

    def fetch_history(self, limit=10):
        self.cursor.execute("""
            SELECT timestamp, strength_score, is_breached 
            FROM history 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
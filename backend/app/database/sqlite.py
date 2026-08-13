import sqlite3
from pathlib import Path


# =====================================
# Database Path
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASE_PATH = BASE_DIR / "legal_cases.db"


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()

    # =====================================
    # Create Tables
    # =====================================

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS legal_cases (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            case_id TEXT UNIQUE,

            citizen_name TEXT,

            city TEXT,

            category TEXT,

            applicable_act TEXT,

            confidence TEXT,

            complaint TEXT,

            report_json TEXT,

            created_at TEXT

        )
        """)

        self.connection.commit()

    # =====================================
    # Execute Query
    # =====================================

    def execute(self, query, params=()):

        self.cursor.execute(query, params)

        self.connection.commit()

    # =====================================
    # Fetch One
    # =====================================

    def fetchone(self, query, params=()):

        cursor = self.connection.execute(query, params)

        row = cursor.fetchone()

        return dict(row) if row else None

    # =====================================
    # Fetch All
    # =====================================

    def fetchall(self, query, params=()):

        cursor = self.connection.execute(query, params)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]


db = Database()
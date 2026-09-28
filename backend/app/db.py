from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "feedback.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_sqft REAL,
            bedrooms INTEGER,
            bathrooms INTEGER,
            location_score REAL,
            age_years INTEGER,
            actual_price REAL
        )
        """
    )

    cursor.execute("PRAGMA table_info(feedback)")
    columns = [row[1] for row in cursor.fetchall()]

    if "predicted_price" not in columns:
        cursor.execute(
            """
            ALTER TABLE feedback
            ADD COLUMN predicted_price REAL
            """
        )

    conn.commit()
    conn.close()
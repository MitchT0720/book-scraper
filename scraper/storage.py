import sqlite3

DB_PATH = "books.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                title     TEXT NOT NULL,
                price     REAL,
                url       TEXT UNIQUE,
                scraped_at TEXT
            )
        """)

def save_books(books: list[dict]) -> int:
    inserted = 0
    with sqlite3.connect(DB_PATH) as conn:
        for book in books:
            try:
                conn.execute(
                    """
                    INSERT INTO books (title, price, url, scraped_at)
                    VALUES (:title, :price, :url, :scraped_at)
                    """,
                    book,
                )
                inserted += 1
            except sqlite3.IntegrityError:
                pass
    return inserted
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = "books.db"

def query_db(sql: str, params: tuple = ()) -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

@app.route("/books")
def get_books():
    title = request.args.get("title")
    price = request.args.get("price")
    limit = int(request.args.get("limit", 50))

    sql = "SELECT * FROM books WHERE 1=1"
    params = []

    if title:
        sql += " AND title LIKE ?"
        params.append(f"%{title}%")
    if price:
        sql += " AND price LIKE ?"
        params.append(f"%{price}%")

    sql += " ORDER BY scraped_at DESC LIMIT ?"
    params.append(limit)

    return jsonify(query_db(sql, tuple(params)))

@app.route("/books/stats")
def stats():
    data = query_db("""
        SELECT title, COUNT(*) as count
        FROM books
        GROUP BY title
        ORDER BY count DESC
        LIMIT 10
    """)
    return jsonify(data)
import sqlite3
from datetime import date
from decimal import Decimal, InvalidOperation


def connect(path="expenses.db"):
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            cents INTEGER NOT NULL CHECK (cents > 0),
            category TEXT NOT NULL,
            note TEXT NOT NULL DEFAULT ''
        )"""
    )
    return conn


def to_cents(text):
    try:
        amount = Decimal(text)
    except InvalidOperation:
        raise ValueError(f"'{text}' is not a number")
    if amount <= 0:
        raise ValueError("amount must be more than zero")
    return int((amount * 100).to_integral_value())


def money(cents):
    return f"{cents // 100}.{cents % 100:02d}"


def add(conn, cents, category, note="", day=None):
    day = day or date.today().isoformat()
    cur = conn.execute(
        "INSERT INTO expenses (day, cents, category, note) VALUES (?, ?, ?, ?)",
        (day, cents, category, note),
    )
    conn.commit()
    return cur.lastrowid


def list_all(conn):
    return conn.execute(
        "SELECT id, day, cents, category, note FROM expenses ORDER BY id"
    ).fetchall()


def totals(conn):
    return conn.execute(
        "SELECT category, SUM(cents) FROM expenses GROUP BY category ORDER BY SUM(cents) DESC"
    ).fetchall()


def remove(conn, expense_id):
    cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    return cur.rowcount == 1

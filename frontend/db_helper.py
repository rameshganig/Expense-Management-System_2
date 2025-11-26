import sqlite3
from contextlib import contextmanager
import os
from datetime import date
from pathlib import Path

# Make logging_setup import resilient to different working directories
try:
    from logging_setup import setup_logger
except Exception:
    try:
        from .logging_setup import setup_logger
    except Exception:
        def setup_logger(name: str):
            import logging
            logger = logging.getLogger(name)
            if not logger.handlers:
                handler = logging.StreamHandler()
                fmt = "%(asctime)s %(levelname)s %(message)s"
                handler.setFormatter(logging.Formatter(fmt))
                logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            return logger

# Allow importing this module outside a Streamlit runtime (e.g., during tests)
try:
    import streamlit as st
except Exception:
    st = None

logger = setup_logger('db_helper')


def _get_db_path():
    """Get SQLite database file path. Create in home directory for persistence."""
    db_dir = Path.home() / '.expense_manager'
    db_dir.mkdir(exist_ok=True)
    return str(db_dir / 'expenses.db')


@contextmanager
def get_db_cursor(commit=False):
    """Context manager that yields a SQLite cursor with row_factory set to dict-like access.

    Creates the `expenses` table if it doesn't exist.
    """
    db_path = _get_db_path()
    logger.info(f"✅ Using SQLite database at: {db_path}")

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
        cursor = conn.cursor()

        # Ensure table exists
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_date DATE NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

        try:
            yield cursor
            if commit:
                conn.commit()
        finally:
            cursor.close()
            conn.close()
    except sqlite3.Error as err:
        logger.error(f"SQLite connection error: {err}")
        raise


def _to_date_str(d):
    if isinstance(d, (date,)):
        return d.strftime("%Y-%m-%d")
    return str(d)


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    dstr = _to_date_str(expense_date)
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = ?", (dstr,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    dstr = _to_date_str(expense_date)
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = ?", (dstr,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    dstr = _to_date_str(expense_date)
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (?, ?, ?, ?)",
            (dstr, float(amount), category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    s = _to_date_str(start_date)
    e = _to_date_str(end_date)
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT category, SUM(amount) as total
            FROM expenses
            WHERE expense_date BETWEEN ? AND ?
            GROUP BY category;
            """,
            (s, e),
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else []


if __name__ == "__main__":
    # Quick local smoke test
    from datetime import date
    today = date.today()
    try:
        db_path = _get_db_path()
        print(f"Using SQLite database at: {db_path}")
        delete_expenses_for_date(today)
        insert_expense(today, 12.5, "Food", "Coffee")
        insert_expense(today, 100, "Shopping", "Books")
        print("Expenses for today:", fetch_expenses_for_date(today))
        print("Summary:", fetch_expense_summary(today, today))
    except Exception as e:
        print(f"Error: {e}")

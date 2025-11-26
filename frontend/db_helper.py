import mysql.connector
from contextlib import contextmanager
import os
from datetime import date

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


def _get_db_config():
    """Get MySQL database configuration from Streamlit secrets or environment variables.
    Priority:
      1. Streamlit secrets (if running inside Streamlit)
      2. Environment variables
      3. Defaults (localhost for local development)
    """
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'expense_manager',
        'port': 3306,
    }

    # 1) Try Streamlit secrets first
    if st is not None:
        try:
            config['host'] = st.secrets.get('DB_HOST', config['host'])
            config['user'] = st.secrets.get('DB_USER', config['user'])
            config['password'] = st.secrets.get('DB_PASSWORD', config['password'])
            config['database'] = st.secrets.get('DB_NAME', config['database'])
            config['port'] = int(st.secrets.get('DB_PORT', config['port']))
            logger.info(f"✅ Loaded DB config from Streamlit secrets: {config['host']}")
            return config
        except Exception as e:
            logger.warning(f"⚠️ Failed to load from Streamlit secrets: {e}")

    # 2) Try environment variables
    env_host = os.environ.get('DB_HOST')
    env_user = os.environ.get('DB_USER')
    env_pass = os.environ.get('DB_PASSWORD')
    env_db = os.environ.get('DB_NAME')
    env_port = os.environ.get('DB_PORT')
    
    if env_host or env_user or env_pass or env_db or env_port:
        config['host'] = env_host or config['host']
        config['user'] = env_user or config['user']
        config['password'] = env_pass or config['password']
        config['database'] = env_db or config['database']
        config['port'] = int(env_port) if env_port else config['port']
        logger.info(f"✅ Loaded DB config from environment variables: {config['host']}")
        return config

    logger.warning(f"⚠️ Using default DB config (localhost) - No secrets or env vars found!")
    return config


@contextmanager
def get_db_cursor(commit=False):
    """Context manager that yields a MySQL cursor with dict-like rows.

    Creates the `expenses` table if it doesn't exist.
    """
    config = _get_db_config()

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        # Ensure table exists
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                expense_date DATE NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                category VARCHAR(100) NOT NULL,
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
    except mysql.connector.Error as err:
        logger.error(f"MySQL connection error: {err}")
        raise


def _to_date_str(d):
    if isinstance(d, (date,)):
        return d.strftime("%Y-%m-%d")
    return str(d)


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    dstr = _to_date_str(expense_date)
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (dstr,))
        rows = cursor.fetchall()
        return rows if rows else []


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    dstr = _to_date_str(expense_date)
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (dstr,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    dstr = _to_date_str(expense_date)
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
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
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY category;
            """,
            (s, e),
        )
        rows = cursor.fetchall()
        return rows if rows else []


if __name__ == "__main__":
    # Quick local smoke test
    from datetime import date
    today = date.today()
    try:
        config = _get_db_config()
        print("DB Config:", {k: v if k != 'password' else '***' for k, v in config.items()})
        delete_expenses_for_date(today)
        insert_expense(today, 12.5, "Food", "Coffee")
        insert_expense(today, 100, "Shopping", "Books")
        print("Expenses for today:", fetch_expenses_for_date(today))
        print("Summary:", fetch_expense_summary(today, today))
    except Exception as e:
        print(f"Error: {e}")

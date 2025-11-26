import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
import streamlit as st
import os

logger = setup_logger('db_helper')


@contextmanager
def get_db_cursor(commit=False):
    """
    Create a database cursor with credentials from Streamlit secrets or environment variables.
    For Streamlit Cloud: Add secrets in app Settings → Secrets
    For local development: Use .streamlit/secrets.toml
    """
    try:
        db_host = st.secrets.get("DB_HOST", os.getenv("DB_HOST", "localhost"))
        db_user = st.secrets.get("DB_USER", os.getenv("DB_USER", "root"))
        db_password = st.secrets.get("DB_PASSWORD", os.getenv("DB_PASSWORD", ""))
        db_name = st.secrets.get("DB_NAME", os.getenv("DB_NAME", "expense_manager"))
        db_port = st.secrets.get("DB_PORT", os.getenv("DB_PORT", 3306))
    except Exception as e:
        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "")
        db_name = os.getenv("DB_NAME", "expense_manager")
        db_port = os.getenv("DB_PORT", 3306)
    
    try:
        # Convert port to int if it's a string
        try:
            db_port = int(db_port)
        except (ValueError, TypeError):
            db_port = 3306
            
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            autocommit=False,
            connection_timeout=10
        )
    except mysql.connector.Error as e:
        error_msg = f"""
        ❌ DATABASE CONNECTION ERROR
        
        Your app tried to connect to: {db_host}
        
        🚀 For Streamlit Cloud deployment:
        1. Go to your Streamlit app → Settings → Secrets
        2. Add these secrets:
           DB_HOST = "your-cloud-database-host"
           DB_USER = "your-database-user"
           DB_PASSWORD = "your-database-password"
           DB_NAME = "expense_manager"
           DB_PORT = "3306"
        
        ⭐ Recommended: Use PlanetScale (planetscale.com)
           - Free MySQL-compatible database
           - Easy setup (5 minutes)
           - No credit card needed
        
        📖 See CLOUD_DATABASE_SETUP.md for detailed instructions
        
        💻 For local development:
        - Update frontend/.streamlit/secrets.toml
        - Make sure MySQL is running
        - Use 'localhost' as DB_HOST
        
        Error details: {str(e)}
        """
        st.error(error_msg)
        logger.error(error_msg)
        raise Exception(error_msg)

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    expenses = fetch_expenses_for_date("2024-09-30")
    print(expenses)
    # delete_expenses_for_date("2024-08-25")
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in summary:
        print(record)

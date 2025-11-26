#!/usr/bin/env python3
"""
Migration script: SQLite (local) → AWS RDS MySQL

This script reads all expenses from the local SQLite database
and writes them to AWS RDS MySQL.

Usage:
    python migrate_sqlite_to_rds.py

Prerequisites:
    - AWS RDS MySQL instance must be reachable and security group configured
    - Credentials in ~/.streamlit/secrets.toml or as environment variables
"""

import sqlite3
import mysql.connector
from pathlib import Path
from datetime import datetime
import sys

def get_sqlite_path():
    """Get path to local SQLite database."""
    return str(Path.home() / '.expense_manager' / 'expenses.db')

def get_rds_config():
    """Get AWS RDS credentials from environment variables or defaults."""
    config = {
        'host': 'expensemanager.cjmwykkwio4g.us-east-2.rds.amazonaws.com',
        'user': 'root',
        'password': '1OX10ec425',
        'database': 'expensemanager',
        'port': 3306,
    }
    
    # Override with environment variables if set
    import os
    config['host'] = os.environ.get('DB_HOST', config['host'])
    config['user'] = os.environ.get('DB_USER', config['user'])
    config['password'] = os.environ.get('DB_PASSWORD', config['password'])
    config['database'] = os.environ.get('DB_NAME', config['database'])
    config['port'] = int(os.environ.get('DB_PORT', config['port']))
    
    return config

def read_from_sqlite():
    """Read all expenses from local SQLite database."""
    sqlite_path = get_sqlite_path()
    
    if not Path(sqlite_path).exists():
        print(f"❌ SQLite database not found at: {sqlite_path}")
        return []
    
    print(f"📖 Reading from SQLite: {sqlite_path}")
    
    try:
        conn = sqlite3.connect(sqlite_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT expense_date, amount, category, notes, created_at FROM expenses ORDER BY created_at")
        rows = cursor.fetchall()
        expenses = [dict(row) for row in rows]
        
        cursor.close()
        conn.close()
        
        print(f"✅ Read {len(expenses)} expenses from SQLite")
        return expenses
    
    except Exception as e:
        print(f"❌ Error reading from SQLite: {e}")
        return []

def write_to_rds(expenses):
    """Write all expenses to AWS RDS MySQL."""
    config = get_rds_config()
    
    print(f"🔗 Connecting to AWS RDS: {config['host']}")
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
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
        print("✅ Ensured table exists in RDS")
        
        # Insert all expenses
        inserted = 0
        skipped = 0
        
        for expense in expenses:
            try:
                cursor.execute(
                    "INSERT INTO expenses (expense_date, amount, category, notes, created_at) VALUES (%s, %s, %s, %s, %s)",
                    (
                        expense['expense_date'],
                        float(expense['amount']),
                        expense['category'],
                        expense['notes'],
                        expense['created_at']
                    )
                )
                inserted += 1
            except Exception as e:
                print(f"⚠️  Skipped expense {expense}: {e}")
                skipped += 1
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Successfully migrated {inserted} expenses to RDS")
        if skipped > 0:
            print(f"⚠️  Skipped {skipped} expenses due to errors")
        
        return True
    
    except mysql.connector.Error as err:
        print(f"❌ MySQL connection error: {err}")
        print("\n💡 Troubleshooting:")
        print("   1. Verify AWS RDS is running")
        print("   2. Check security group has inbound rule for port 3306 from your IP")
        print("   3. Verify credentials are correct in environment variables or code")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def verify_migration():
    """Verify data was migrated by comparing counts."""
    config = get_rds_config()
    sqlite_path = get_sqlite_path()
    
    try:
        # Count in SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute("SELECT COUNT(*) FROM expenses")
        sqlite_count = sqlite_cursor.fetchone()[0]
        sqlite_conn.close()
        
        # Count in RDS
        rds_conn = mysql.connector.connect(**config)
        rds_cursor = rds_conn.cursor()
        rds_cursor.execute("SELECT COUNT(*) FROM expenses")
        rds_count = rds_cursor.fetchone()[0]
        rds_cursor.execute("SELECT expense_date, amount, category FROM expenses ORDER BY created_at LIMIT 5")
        rds_sample = rds_cursor.fetchall()
        rds_conn.close()
        
        print("\n📊 Migration Verification:")
        print(f"   SQLite expenses: {sqlite_count}")
        print(f"   RDS expenses:    {rds_count}")
        
        if sqlite_count == rds_count:
            print("✅ Counts match! Data successfully migrated.")
            print("\n📋 Sample data from RDS (first 5 records):")
            for i, record in enumerate(rds_sample, 1):
                print(f"   {i}. Date: {record[0]}, Amount: {record[1]}, Category: {record[2]}")
            return True
        else:
            print(f"⚠️  Count mismatch! SQLite: {sqlite_count}, RDS: {rds_count}")
            return False
    
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def main():
    print("=" * 60)
    print("SQLite → AWS RDS MySQL Migration")
    print("=" * 60)
    
    # Step 1: Read from SQLite
    expenses = read_from_sqlite()
    
    if not expenses:
        print("ℹ️  No expenses to migrate. Exiting.")
        sys.exit(0)
    
    # Step 2: Ask for confirmation
    print(f"\n⚠️  Ready to migrate {len(expenses)} expenses to AWS RDS.")
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("Migration cancelled.")
        sys.exit(0)
    
    # Step 3: Write to RDS
    print()
    success = write_to_rds(expenses)
    
    if not success:
        sys.exit(1)
    
    # Step 4: Verify
    print()
    verify_migration()
    
    print("\n✅ Migration complete!")
    print("\n📝 Next steps:")
    print("   1. Modify db_helper.py to use MySQL instead of SQLite")
    print("   2. Restart the Streamlit app")
    print("   3. Verify the app loads data from AWS RDS")

if __name__ == "__main__":
    main()

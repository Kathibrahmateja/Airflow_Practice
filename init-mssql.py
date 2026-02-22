#!/usr/bin/env python3
"""Initialize MSSQL database for Airflow."""
import pyodbc
import time
import sys

# Retry configuration
max_retries = 30
retry_delay = 2

for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt + 1}/{max_retries}: Connecting to MSSQL server...")
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=mssql;'
            'UID=sa;'
            'PWD=Airflow123!;'
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'airflow')
            CREATE DATABASE airflow;
        """)
        conn.commit()
        
        print("✓ Airflow database created or already exists")
        conn.close()
        sys.exit(0)
        
    except Exception as e:
        if attempt < max_retries - 1:
            print(f"✗ Connection failed: {e}")
            print(f"  Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"✗ Failed after {max_retries} attempts: {e}")
            sys.exit(1)

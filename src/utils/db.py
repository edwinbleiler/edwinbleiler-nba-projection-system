"""
Database utilities for NBA Projection System.
Handles SQLite database connections and operations.
Author: Edwin (Ed) Bleiler
"""
import sqlite3
import pandas as pd
from pathlib import Path
from src.utils.paths import get_db_path
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def get_connection():
    """
    Get a SQLite database connection.

    Returns:
        sqlite3.Connection: Database connection
    """
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(db_path))


def execute_query(query, params=None):
    """
    Execute a SQL query.

    Args:
        query: SQL query string
        params: Query parameters (optional)

    Returns:
        pd.DataFrame: Query results
    """
    conn = get_connection()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()


def write_table(df, table_name, if_exists='replace'):
    """
    Write a DataFrame to a database table.

    Args:
        df: pandas DataFrame to write
        table_name: Target table name
        if_exists: How to behave if table exists ('replace', 'append', 'fail')
    """
    conn = get_connection()
    try:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        logger.info(f"Written {len(df)} rows to table '{table_name}'")
    finally:
        conn.close()


def table_exists(table_name):
    """
    Check if a table exists in the database.

    Args:
        table_name: Name of the table to check

    Returns:
        bool: True if table exists, False otherwise
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()


def get_latest_date(table_name, date_column='GAME_DATE'):
    """
    Get the most recent date from a table.

    Args:
        table_name: Name of the table
        date_column: Name of the date column

    Returns:
        str or None: Latest date as string, or None if table is empty
    """
    if not table_exists(table_name):
        return None

    query = f"SELECT MAX({date_column}) as max_date FROM {table_name}"
    result = execute_query(query)

    if result.empty or pd.isna(result.iloc[0]['max_date']):
        return None

    return result.iloc[0]['max_date']

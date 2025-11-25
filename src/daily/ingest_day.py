"""
Daily data ingestion script for NBA Projection System.
Loads daily data and appends to historical database.
Author: Edwin (Ed) Bleiler
"""
import pandas as pd
import os
from src.utils.db import write_table, execute_query, table_exists
from src.utils.logging import setup_logger, log_step

logger = setup_logger(__name__)


def load_daily_data(file_path='/tmp/daily_stats.csv'):
    """
    Load daily stats from CSV.

    Args:
        file_path: Path to daily stats CSV

    Returns:
        pd.DataFrame: Daily stats data
    """
    if not os.path.exists(file_path):
        logger.error(f"Daily data file not found: {file_path}")
        return pd.DataFrame()

    logger.info(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded {len(df)} records")

    return df


def deduplicate_data(df, existing_table='player_game_logs'):
    """
    Remove any duplicate records that already exist in the database.

    Args:
        df: New data to ingest
        existing_table: Name of existing table

    Returns:
        pd.DataFrame: Deduplicated data
    """
    if not table_exists(existing_table):
        logger.info("No existing table, no deduplication needed")
        return df

    # Fetch existing game IDs and player IDs
    query = "SELECT DISTINCT GAME_ID, PLAYER_ID FROM player_game_logs"
    existing_df = execute_query(query)

    if existing_df.empty:
        return df

    # Create composite key
    existing_df['key'] = existing_df['GAME_ID'].astype(str) + '_' + existing_df['PLAYER_ID'].astype(str)
    df['key'] = df['GAME_ID'].astype(str) + '_' + df['PLAYER_ID'].astype(str)

    # Filter out existing records
    original_count = len(df)
    df = df[~df['key'].isin(existing_df['key'])]
    df = df.drop(columns=['key'])

    removed_count = original_count - len(df)
    logger.info(f"Removed {removed_count} duplicate records")
    logger.info(f"New records to insert: {len(df)}")

    return df


def ingest_daily_data(file_path='/tmp/daily_stats.csv'):
    """
    Ingest daily data into the database.

    Args:
        file_path: Path to daily stats CSV
    """
    log_step(logger, "Starting Daily Ingestion")

    # Load data
    df = load_daily_data(file_path)

    if df.empty:
        logger.warning("No data to ingest")
        return

    # Deduplicate
    df = deduplicate_data(df)

    if df.empty:
        logger.info("All records already exist in database")
        return

    # Append to database
    write_table(df, 'player_game_logs', if_exists='append')

    log_step(logger, "Ingestion Complete")


def main():
    """Main execution function."""
    ingest_daily_data()


if __name__ == '__main__':
    main()

"""
Feature engineering pipeline for NBA Projection System.
Builds rolling averages and advanced features for player projections.
Author: Edwin (Ed) Bleiler
"""
import pandas as pd
import numpy as np
from src.utils.db import execute_query, write_table, table_exists
from src.utils.logging import setup_logger, log_step

logger = setup_logger(__name__)


def load_raw_game_logs():
    """
    Load raw game logs from database.

    Returns:
        pd.DataFrame: Raw game logs
    """
    if not table_exists('player_game_logs'):
        logger.error("player_game_logs table does not exist")
        return pd.DataFrame()

    query = "SELECT * FROM player_game_logs"
    df = execute_query(query)

    logger.info(f"Loaded {len(df)} game logs")

    return df


def prepare_data(df):
    """
    Prepare and clean data for feature engineering.

    Args:
        df: Raw game logs

    Returns:
        pd.DataFrame: Cleaned data
    """
    logger.info("Preparing data...")

    # Convert date to datetime
    if 'GAME_DATE' in df.columns:
        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])

    # Sort by player and date
    df = df.sort_values(['PLAYER_ID', 'GAME_DATE'])

    # Fill missing numeric values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    logger.info("Data preparation complete")

    return df


def calculate_rolling_features(df, windows=[3, 5, 10, 20]):
    """
    Calculate rolling average features.

    Args:
        df: Game logs DataFrame
        windows: List of window sizes for rolling averages

    Returns:
        pd.DataFrame: Data with rolling features
    """
    logger.info("Calculating rolling features...")

    stat_columns = ['MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FT_PCT', 'TOV']

    # Filter to columns that exist
    stat_columns = [col for col in stat_columns if col in df.columns]

    for window in windows:
        logger.info(f"  Computing {window}-game rolling averages")

        for stat in stat_columns:
            col_name = f'{stat}_ROLLING_{window}'

            df[col_name] = df.groupby('PLAYER_ID')[stat].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )

    logger.info("Rolling features complete")

    return df


def calculate_rate_features(df):
    """
    Calculate per-minute rate statistics.

    Args:
        df: Game logs DataFrame

    Returns:
        pd.DataFrame: Data with rate features
    """
    logger.info("Calculating rate features...")

    if 'MIN' not in df.columns:
        logger.warning("MIN column not found, skipping rate features")
        return df

    # Per-minute rates
    rate_stats = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV']

    for stat in rate_stats:
        if stat in df.columns:
            col_name = f'{stat}_PER_MIN'
            df[col_name] = df[stat] / df['MIN'].replace(0, np.nan)

    # Fill NaN rates with 0
    rate_cols = [col for col in df.columns if '_PER_MIN' in col]
    df[rate_cols] = df[rate_cols].fillna(0)

    logger.info("Rate features complete")

    return df


def calculate_advanced_features(df):
    """
    Calculate advanced statistics and trends.

    Args:
        df: Game logs DataFrame

    Returns:
        pd.DataFrame: Data with advanced features
    """
    logger.info("Calculating advanced features...")

    # Days rest (difference between games)
    df['DAYS_REST'] = df.groupby('PLAYER_ID')['GAME_DATE'].diff().dt.days.fillna(0)

    # Home/Away indicators (if available)
    if 'MATCHUP' in df.columns:
        df['IS_HOME'] = df['MATCHUP'].str.contains('vs.').astype(int)
    else:
        df['IS_HOME'] = 0

    # Season game number
    df['SEASON_GAME_NUM'] = df.groupby(['PLAYER_ID', 'SEASON']).cumcount() + 1

    # Usage rate proxy (if field goal attempts available)
    if 'FGA' in df.columns and 'MIN' in df.columns:
        df['USAGE_RATE'] = df['FGA'] / df['MIN'].replace(0, np.nan)
        df['USAGE_RATE'] = df['USAGE_RATE'].fillna(0)

    logger.info("Advanced features complete")

    return df


def build_all_features():
    """
    Main function to build all features.
    Loads raw data, engineers features, and saves to database.
    """
    log_step(logger, "Starting Feature Engineering")

    # Load data
    df = load_raw_game_logs()

    if df.empty:
        logger.error("No data to process")
        return

    # Prepare data
    df = prepare_data(df)

    # Build features
    df = calculate_rolling_features(df)
    df = calculate_rate_features(df)
    df = calculate_advanced_features(df)

    # Save to database
    write_table(df, 'player_features', if_exists='replace')

    log_step(logger, "Feature Engineering Complete")
    logger.info(f"Built features for {len(df)} records")
    logger.info(f"Total features: {len(df.columns)}")


def main():
    """Main execution function."""
    build_all_features()


if __name__ == '__main__':
    main()

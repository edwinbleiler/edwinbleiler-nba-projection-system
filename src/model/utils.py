"""
Model utilities for NBA Projection System.
Common functions for model training and prediction.
Author: Edwin (Ed) Bleiler
"""
import pandas as pd
import numpy as np
from src.utils.db import execute_query, write_table, table_exists
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def load_features():
    """
    Load engineered features from database.

    Returns:
        pd.DataFrame: Features data
    """
    if not table_exists('player_features'):
        logger.error("player_features table does not exist")
        return pd.DataFrame()

    query = "SELECT * FROM player_features"
    df = execute_query(query)

    logger.info(f"Loaded {len(df)} feature records")

    return df


def build_model_dataset():
    """
    Build model training dataset from features.
    Creates a cleaned dataset ready for model training.
    """
    logger.info("Building model dataset...")

    df = load_features()

    if df.empty:
        logger.error("No features available")
        return

    # Remove rows with insufficient data
    # Keep only games where player played at least 1 minute
    if 'MIN' in df.columns:
        df = df[df['MIN'] > 0]

    # Select feature columns for modeling
    feature_patterns = ['ROLLING', 'PER_MIN', 'DAYS_REST', 'IS_HOME', 'SEASON_GAME_NUM']
    feature_cols = [col for col in df.columns if any(pattern in col for pattern in feature_patterns)]

    # Add target columns
    target_cols = ['MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FT_PCT']
    target_cols = [col for col in target_cols if col in df.columns]

    # Add ID columns
    id_cols = ['PLAYER_ID', 'GAME_DATE', 'SEASON']
    id_cols = [col for col in id_cols if col in df.columns]

    # Combine all columns
    keep_cols = id_cols + feature_cols + target_cols
    keep_cols = [col for col in keep_cols if col in df.columns]

    df_model = df[keep_cols].copy()

    # Remove rows with any missing values in features
    df_model = df_model.dropna()

    logger.info(f"Model dataset: {len(df_model)} records, {len(feature_cols)} features")

    # Save to database
    write_table(df_model, 'model_dataset', if_exists='replace')

    logger.info("Model dataset saved")


def get_feature_columns():
    """
    Get list of feature columns for modeling.

    Returns:
        list: Feature column names
    """
    df = execute_query("SELECT * FROM model_dataset LIMIT 1")

    if df.empty:
        return []

    # Feature patterns
    feature_patterns = ['ROLLING', 'PER_MIN', 'DAYS_REST', 'IS_HOME', 'SEASON_GAME_NUM']
    feature_cols = [col for col in df.columns if any(pattern in col for pattern in feature_patterns)]

    return feature_cols


def prepare_training_data(target_column):
    """
    Prepare X and y for model training.

    Args:
        target_column: Name of target variable

    Returns:
        tuple: (X, y) training data
    """
    if not table_exists('model_dataset'):
        logger.error("model_dataset table does not exist")
        return None, None

    df = execute_query("SELECT * FROM model_dataset")

    if df.empty or target_column not in df.columns:
        logger.error(f"Cannot prepare training data for {target_column}")
        return None, None

    feature_cols = get_feature_columns()

    if not feature_cols:
        logger.error("No feature columns found")
        return None, None

    X = df[feature_cols]
    y = df[target_column]

    logger.info(f"Training data: {len(X)} samples, {len(feature_cols)} features")

    return X, y


def main():
    """Main execution function."""
    build_model_dataset()


if __name__ == '__main__':
    main()

"""
Minutes prediction module for NBA Projection System.
Uses trained model to predict minutes for players.
Author: Edwin (Ed) Bleiler
"""
import joblib
import pandas as pd
import numpy as np
from src.utils.paths import get_data_dir
from src.utils.db import execute_query
from src.model.utils import get_feature_columns
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def load_minutes_model():
    """
    Load trained minutes prediction model.

    Returns:
        lgb.Booster: Trained model
    """
    model_path = get_data_dir() / 'minutes_model.pkl'

    if not model_path.exists():
        logger.error(f"Minutes model not found at {model_path}")
        return None

    model = joblib.load(model_path)
    logger.info("Minutes model loaded")

    return model


def get_latest_features(player_ids=None):
    """
    Get latest features for players.

    Args:
        player_ids: List of player IDs (None = all players)

    Returns:
        pd.DataFrame: Latest features for each player
    """
    # Get latest features from database
    query = """
    SELECT *
    FROM player_features
    WHERE (PLAYER_ID, GAME_DATE) IN (
        SELECT PLAYER_ID, MAX(GAME_DATE)
        FROM player_features
        GROUP BY PLAYER_ID
    )
    """

    df = execute_query(query)

    if df.empty:
        logger.warning("No features found")
        return pd.DataFrame()

    if player_ids is not None:
        df = df[df['PLAYER_ID'].isin(player_ids)]

    logger.info(f"Retrieved features for {len(df)} players")

    return df


def predict_minutes(players_df=None):
    """
    Predict minutes for players.

    Args:
        players_df: DataFrame with PLAYER_ID column (None = all players)

    Returns:
        pd.DataFrame: Predictions with PLAYER_ID and PREDICTED_MINUTES
    """
    logger.info("Predicting minutes...")

    # Load model
    model = load_minutes_model()

    if model is None:
        logger.error("Cannot predict without model")
        return pd.DataFrame()

    # Get player IDs
    player_ids = None
    if players_df is not None and 'PLAYER_ID' in players_df.columns:
        player_ids = players_df['PLAYER_ID'].tolist()

    # Get features
    features_df = get_latest_features(player_ids)

    if features_df.empty:
        logger.error("No features available for prediction")
        return pd.DataFrame()

    # Get feature columns
    feature_cols = get_feature_columns()

    if not feature_cols:
        logger.error("No feature columns defined")
        return pd.DataFrame()

    # Check that all feature columns exist
    missing_cols = set(feature_cols) - set(features_df.columns)
    if missing_cols:
        logger.warning(f"Missing feature columns: {missing_cols}")
        feature_cols = [col for col in feature_cols if col in features_df.columns]

    if not feature_cols:
        logger.error("No valid feature columns available")
        return pd.DataFrame()

    # Prepare features
    X = features_df[feature_cols].fillna(0)

    # Predict
    predictions = model.predict(X)

    # Clip to reasonable range
    predictions = np.clip(predictions, 0, 48)

    # Create results DataFrame
    results_df = pd.DataFrame({
        'PLAYER_ID': features_df['PLAYER_ID'],
        'PREDICTED_MINUTES': predictions
    })

    logger.info(f"Predicted minutes for {len(results_df)} players")

    return results_df


def main():
    """Main execution function."""
    predictions = predict_minutes()

    if not predictions.empty:
        print(predictions.head(10))


if __name__ == '__main__':
    main()

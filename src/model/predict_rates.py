"""
Rate prediction module for NBA Projection System.
Uses trained models to predict per-minute stat rates.
Author: Edwin (Ed) Bleiler
"""
import joblib
import pandas as pd
import numpy as np
from src.utils.paths import get_data_dir
from src.model.predict_minutes import get_latest_features
from src.model.utils import get_feature_columns
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def load_rate_model(stat_name):
    """
    Load trained rate prediction model for a specific stat.

    Args:
        stat_name: Name of the stat (e.g., 'PTS', 'REB')

    Returns:
        lgb.Booster: Trained model or None
    """
    model_path = get_data_dir() / f'{stat_name.lower()}_rate_model.pkl'

    if not model_path.exists():
        logger.warning(f"Rate model not found for {stat_name} at {model_path}")
        return None

    model = joblib.load(model_path)
    return model


def predict_rates(players_df=None, stats=None):
    """
    Predict per-minute rates for multiple stats.

    Args:
        players_df: DataFrame with PLAYER_ID column (None = all players)
        stats: List of stats to predict (None = all)

    Returns:
        pd.DataFrame: Predictions with PLAYER_ID and PREDICTED_{STAT}_RATE columns
    """
    logger.info("Predicting per-minute rates...")

    if stats is None:
        stats = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FT_PCT']

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

    # Create results DataFrame
    results_df = pd.DataFrame({
        'PLAYER_ID': features_df['PLAYER_ID']
    })

    # Predict each stat
    for stat in stats:
        logger.info(f"  Predicting {stat} rate...")

        model = load_rate_model(stat)

        if model is None:
            logger.warning(f"Skipping {stat} - model not available")
            continue

        try:
            predictions = model.predict(X)

            # Clip to reasonable ranges
            if stat in ['FG_PCT', 'FT_PCT']:
                predictions = np.clip(predictions, 0, 1)
            else:
                predictions = np.clip(predictions, 0, 10)  # Per-minute upper bound

            results_df[f'PREDICTED_{stat}_RATE'] = predictions

        except Exception as e:
            logger.error(f"Failed to predict {stat}: {str(e)}")
            continue

    logger.info(f"Predicted rates for {len(results_df)} players")

    return results_df


def main():
    """Main execution function."""
    predictions = predict_rates()

    if not predictions.empty:
        print(predictions.head(10))


if __name__ == '__main__':
    main()

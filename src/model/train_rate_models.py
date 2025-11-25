"""
Per-minute rate models training for NBA Projection System.
Trains LightGBM models to predict per-minute stat rates.
Author: Edwin (Ed) Bleiler
"""
import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import numpy as np
from src.model.utils import prepare_training_data, get_feature_columns
from src.utils.paths import get_data_dir
from src.utils.logging import setup_logger, log_step

logger = setup_logger(__name__)


def train_rate_model(stat_name):
    """
    Train a model for a specific per-minute rate.

    Args:
        stat_name: Name of the stat (e.g., 'PTS', 'REB', 'AST')

    Returns:
        lgb.Booster: Trained model
    """
    logger.info(f"Training model for {stat_name}...")

    # Prepare target (per-minute rate)
    target_col = f'{stat_name}_PER_MIN'

    # Get feature columns
    feature_cols = get_feature_columns()

    if not feature_cols:
        logger.error("No features available")
        return None

    # Load data
    from src.utils.db import execute_query
    df = execute_query("SELECT * FROM model_dataset")

    if df.empty or target_col not in df.columns:
        logger.warning(f"Cannot train model for {stat_name}: missing data")
        return None

    X = df[feature_cols]
    y = df[target_col]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # LightGBM parameters
    params = {
        'objective': 'regression',
        'metric': 'mae',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'verbose': -1
    }

    # Create datasets
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    # Train model
    model = lgb.train(
        params,
        train_data,
        num_boost_round=300,
        valid_sets=[test_data],
        callbacks=[
            lgb.early_stopping(stopping_rounds=30),
            lgb.log_evaluation(period=100)
        ]
    )

    # Evaluate
    y_pred = model.predict(X_test, num_iteration=model.best_iteration)
    mae = mean_absolute_error(y_test, y_pred)

    logger.info(f"{stat_name} Test MAE: {mae:.4f} per minute")

    return model


def train_all_rate_models():
    """
    Train models for all stat rates.
    """
    log_step(logger, "Training Rate Models")

    # Stats to model
    stats = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FT_PCT']

    models = {}

    for stat in stats:
        model = train_rate_model(stat)

        if model is not None:
            # Save model
            model_path = get_data_dir() / f'{stat.lower()}_rate_model.pkl'
            joblib.dump(model, model_path)
            logger.info(f"Saved {stat} model to {model_path}")

            models[stat] = model

    log_step(logger, "Rate Models Training Complete")
    logger.info(f"Trained {len(models)} models")

    return models


def main():
    """Main execution function."""
    train_all_rate_models()


if __name__ == '__main__':
    main()

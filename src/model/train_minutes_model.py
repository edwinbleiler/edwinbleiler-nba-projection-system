"""
Minutes prediction model training for NBA Projection System.
Trains LightGBM model to predict player minutes.
Author: Edwin (Ed) Bleiler
"""
import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from src.model.utils import prepare_training_data
from src.utils.paths import get_data_dir
from src.utils.logging import setup_logger, log_step

logger = setup_logger(__name__)


def train_minutes_model():
    """
    Train LightGBM model to predict minutes played.

    Returns:
        lgb.Booster: Trained model
    """
    log_step(logger, "Training Minutes Model")

    # Prepare data
    X, y = prepare_training_data('MIN')

    if X is None or y is None:
        logger.error("Failed to prepare training data")
        return None

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    logger.info(f"Training set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")

    # LightGBM parameters
    params = {
        'objective': 'regression',
        'metric': 'mae',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': -1
    }

    # Create datasets
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    # Train model
    logger.info("Training model...")

    model = lgb.train(
        params,
        train_data,
        num_boost_round=500,
        valid_sets=[test_data],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(period=100)
        ]
    )

    # Evaluate
    y_pred = model.predict(X_test, num_iteration=model.best_iteration)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    logger.info(f"Test MAE: {mae:.2f} minutes")
    logger.info(f"Test RMSE: {rmse:.2f} minutes")

    # Save model
    model_path = get_data_dir() / 'minutes_model.pkl'
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")

    log_step(logger, "Minutes Model Training Complete")

    return model


def main():
    """Main execution function."""
    train_minutes_model()


if __name__ == '__main__':
    main()

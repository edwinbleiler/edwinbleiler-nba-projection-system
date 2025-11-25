"""
Daily feature update script for NBA Projection System.
Rebuilds features with latest data.
Author: Edwin (Ed) Bleiler
"""
from src.features.feature_engineering import build_all_features
from src.utils.logging import setup_logger, log_step

logger = setup_logger(__name__)


def update_features():
    """
    Update feature tables with latest data.
    Calls the main feature engineering pipeline.
    """
    log_step(logger, "Starting Feature Update")

    try:
        build_all_features()
        log_step(logger, "Feature Update Complete")

    except Exception as e:
        logger.error(f"Feature update failed: {str(e)}")
        raise


def main():
    """Main execution function."""
    update_features()


if __name__ == '__main__':
    main()

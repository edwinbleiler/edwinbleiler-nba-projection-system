"""
Daily model data update script for NBA Projection System.
Rebuilds model training datasets with latest features.
Author: Edwin (Ed) Bleiler
"""
from src.model.utils import build_model_dataset
from src.utils.logging import setup_logger, log_step

logger = setup_logger(__name__)


def update_model_data():
    """
    Update model training dataset with latest features.
    This rebuilds the training data used by prediction models.
    """
    log_step(logger, "Starting Model Data Update")

    try:
        build_model_dataset()
        log_step(logger, "Model Data Update Complete")

    except Exception as e:
        logger.error(f"Model data update failed: {str(e)}")
        raise


def main():
    """Main execution function."""
    update_model_data()


if __name__ == '__main__':
    main()

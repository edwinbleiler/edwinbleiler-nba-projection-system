"""
Daily projection generation script for NBA Projection System.
Generates player projections for upcoming games.
Author: Edwin (Ed) Bleiler
"""
import pandas as pd
from datetime import datetime
from src.model.predict_minutes import predict_minutes
from src.model.predict_rates import predict_rates
from src.utils.db import execute_query
from src.utils.paths import get_projections_dir
from src.utils.logging import setup_logger, log_step

logger = setup_logger(__name__)


def get_active_players():
    """
    Get list of active players to generate projections for.

    Returns:
        pd.DataFrame: Active players
    """
    query = """
    SELECT DISTINCT PLAYER_ID, PLAYER_NAME
    FROM player_game_logs
    WHERE SEASON = (SELECT MAX(SEASON) FROM player_game_logs)
    ORDER BY PLAYER_NAME
    """

    df = execute_query(query)
    logger.info(f"Found {len(df)} active players")

    return df


def generate_projections():
    """
    Generate projections for all active players.

    Returns:
        pd.DataFrame: Projections with minutes and stat rates
    """
    log_step(logger, "Generating Projections")

    # Get active players
    players_df = get_active_players()

    if players_df.empty:
        logger.warning("No active players found")
        return pd.DataFrame()

    # Predict minutes
    logger.info("Predicting minutes...")
    minutes_df = predict_minutes(players_df)

    # Predict rates (points, rebounds, assists, etc.)
    logger.info("Predicting per-minute rates...")
    rates_df = predict_rates(players_df)

    # Merge predictions
    projections_df = players_df.merge(
        minutes_df[['PLAYER_ID', 'PREDICTED_MINUTES']],
        on='PLAYER_ID',
        how='left'
    )

    projections_df = projections_df.merge(
        rates_df,
        on='PLAYER_ID',
        how='left'
    )

    # Calculate projected totals
    if 'PREDICTED_MINUTES' in projections_df.columns:
        for stat in ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FT_PCT']:
            rate_col = f'PREDICTED_{stat}_RATE'
            if rate_col in projections_df.columns:
                projections_df[f'PROJECTED_{stat}'] = (
                    projections_df['PREDICTED_MINUTES'] * projections_df[rate_col]
                )

    logger.info(f"Generated projections for {len(projections_df)} players")

    return projections_df


def save_projections(projections_df):
    """
    Save projections to CSV file.

    Args:
        projections_df: DataFrame with projections
    """
    if projections_df.empty:
        logger.warning("No projections to save")
        return

    # Create output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = get_projections_dir() / f'projections_{timestamp}.csv'

    projections_df.to_csv(output_path, index=False)
    logger.info(f"Saved projections to {output_path}")

    # Also save as latest
    latest_path = get_projections_dir() / 'projections_latest.csv'
    projections_df.to_csv(latest_path, index=False)
    logger.info(f"Saved latest projections to {latest_path}")


def run_projections():
    """
    Main function to run projection pipeline.
    """
    log_step(logger, "Starting Projection Pipeline")

    # Generate projections
    projections_df = generate_projections()

    # Save results
    save_projections(projections_df)

    log_step(logger, "Projection Pipeline Complete")


def main():
    """Main execution function."""
    run_projections()


if __name__ == '__main__':
    main()

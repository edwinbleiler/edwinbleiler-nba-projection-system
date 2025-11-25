"""
Historical data backfill script for NBA Projection System.
Fetches and stores historical player game logs from multiple NBA seasons.
Author: Edwin (Ed) Bleiler
"""
import pandas as pd
import time
from datetime import datetime
from nba_api.stats.endpoints import playergamelog, commonplayerinfo
from nba_api.stats.static import players
from src.utils.db import write_table, get_connection
from src.utils.fetch_utils import fetch_with_retry
from src.utils.logging import setup_logger, log_step
from src.utils.paths import ensure_dirs_exist

logger = setup_logger(__name__)


def get_all_active_players():
    """
    Get list of all NBA players.

    Returns:
        list: List of player dictionaries with id, full_name, etc.
    """
    logger.info("Fetching all NBA players...")
    all_players = players.get_players()
    logger.info(f"Found {len(all_players)} total players")
    return all_players


def fetch_player_game_logs(player_id, season, season_type='Regular Season'):
    """
    Fetch game logs for a specific player and season.

    Args:
        player_id: NBA player ID
        season: Season string (e.g., '2023-24')
        season_type: Type of season ('Regular Season' or 'Playoffs')

    Returns:
        pd.DataFrame: Player game logs
    """
    try:
        game_log = fetch_with_retry(
            playergamelog.PlayerGameLog,
            player_id=player_id,
            season=season,
            season_type_all_star=season_type
        )

        df = game_log.get_data_frames()[0]

        if not df.empty:
            df['PLAYER_ID'] = player_id
            df['SEASON'] = season

        return df

    except Exception as e:
        logger.warning(f"Failed to fetch logs for player {player_id}, season {season}: {str(e)}")
        return pd.DataFrame()


def backfill_seasons(start_year=2018, end_year=2024, max_players=None):
    """
    Backfill historical game logs for multiple seasons.

    Args:
        start_year: Starting year (e.g., 2018 for 2018-19 season)
        end_year: Ending year (e.g., 2024 for 2023-24 season)
        max_players: Maximum number of players to process (None = all)
    """
    ensure_dirs_exist()
    log_step(logger, "Starting Historical Backfill")

    # Get all players
    all_players = get_all_active_players()

    if max_players:
        all_players = all_players[:max_players]
        logger.info(f"Limited to {max_players} players for testing")

    # Generate season strings
    seasons = [f"{year}-{str(year + 1)[-2:]}" for year in range(start_year, end_year + 1)]
    logger.info(f"Backfilling seasons: {seasons}")

    all_game_logs = []
    total_requests = len(all_players) * len(seasons)
    request_count = 0

    for player in all_players:
        player_id = player['id']
        player_name = player['full_name']

        logger.info(f"Processing {player_name} (ID: {player_id})")

        for season in seasons:
            request_count += 1

            logger.info(f"  Fetching {season} [{request_count}/{total_requests}]")

            df = fetch_player_game_logs(player_id, season)

            if not df.empty:
                all_game_logs.append(df)
                logger.info(f"    Retrieved {len(df)} games")

            # Rate limiting: sleep between requests
            time.sleep(0.6)  # ~100 requests per minute

        # Additional delay between players
        time.sleep(1)

    # Combine and save
    if all_game_logs:
        log_step(logger, "Combining and Saving Data")

        combined_df = pd.concat(all_game_logs, ignore_index=True)
        logger.info(f"Total game logs retrieved: {len(combined_df)}")

        # Write to database
        write_table(combined_df, 'player_game_logs', if_exists='replace')

        log_step(logger, "Backfill Complete")
        logger.info(f"Saved {len(combined_df)} game logs to database")

    else:
        logger.warning("No game logs retrieved")


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description='Backfill NBA historical data')
    parser.add_argument('--start-year', type=int, default=2018,
                        help='Start year (default: 2018)')
    parser.add_argument('--end-year', type=int, default=2024,
                        help='End year (default: 2024)')
    parser.add_argument('--max-players', type=int, default=None,
                        help='Max players to process (default: all)')

    args = parser.parse_args()

    backfill_seasons(
        start_year=args.start_year,
        end_year=args.end_year,
        max_players=args.max_players
    )


if __name__ == '__main__':
    main()

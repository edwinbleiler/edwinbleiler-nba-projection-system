"""
Historical data backfill script for NBA Projection System.
Fetches and stores historical player game logs for recent NBA seasons.

Author: Edwin (Ed) Bleiler
"""

import time
from datetime import datetime
from typing import List, Dict, Optional

import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

from src.utils.db import write_table, get_connection  # get_connection may be unused but kept for compatibility
from src.utils.fetch_utils import fetch_with_retry
from src.utils.logging import setup_logger, log_step
from src.utils.paths import ensure_dirs_exist

logger = setup_logger(__name__)


def get_players(active_only: bool = True, max_players: Optional[int] = None) -> List[Dict]:
    """
    Get list of NBA players.

    Args:
        active_only: If True, only return currently active players.
        max_players: Optional limit for number of players (for testing or throttling).

    Returns:
        list of player dicts with id, full_name, etc.
    """
    if active_only:
        logger.info("Fetching ACTIVE NBA players from nba_api...")
        all_players = players.get_active_players()
    else:
        logger.info("Fetching ALL NBA players from nba_api (active + historical)...")
        all_players = players.get_players()

    logger.info(f"Found {len(all_players)} players before limiting")

    if max_players is not None and max_players > 0:
        all_players = all_players[:max_players]
        logger.info(f"Limiting to first {max_players} players for this run")

    logger.info(f"Using {len(all_players)} players for backfill")
    return all_players


def fetch_player_game_logs(player_id: int, season: str, season_type: str = "Regular Season") -> pd.DataFrame:
    """
    Fetch game logs for a specific player and season.

    Args:
        player_id: NBA player ID
        season: Season string (e.g., '2023-24')
        season_type: Type of season ('Regular Season' or 'Playoffs')

    Returns:
        pd.DataFrame: Player game logs for that season.
    """
    try:
        game_log = fetch_with_retry(
            playergamelog.PlayerGameLog,
            player_id=player_id,
            season=season,
            season_type_all_star=season_type,
        )

        df = game_log.get_data_frames()[0]

        if not df.empty:
            df["PLAYER_ID"] = player_id
            df["SEASON"] = season

        return df

    except Exception as e:
        logger.warning(f"Failed to fetch logs for player {player_id}, season {season}: {str(e)}")
        return pd.DataFrame()


def build_season_list(start_year: int, end_year: int) -> List[str]:
    """
    Build list of season strings between start_year and end_year inclusive.

    Example: start_year=2023, end_year=2024 -> ['2023-24', '2024-25']

    Args:
        start_year: Starting year (e.g., 2023)
        end_year: Ending year (e.g., 2024)

    Returns:
        List of season strings.
    """
    if end_year < start_year:
        raise ValueError(f"end_year ({end_year}) cannot be less than start_year ({start_year})")

    seasons = [f"{year}-{str(year + 1)[-2:]}" for year in range(start_year, end_year + 1)]
    return seasons


def backfill_seasons(
    start_year: int,
    end_year: int,
    max_players: Optional[int] = None,
    active_only: bool = True,
) -> None:
    """
    Backfill historical game logs for multiple seasons.

    Args:
        start_year: Starting year (e.g., 2023 for 2023-24 season).
        end_year: Ending year (e.g., 2024 for 2024-25 season).
        max_players: Maximum number of players to process (None = all).
        active_only: If True, only include currently active players.
    """
    ensure_dirs_exist()
    log_step(logger, "Starting Historical Backfill")

    seasons = build_season_list(start_year, end_year)
    logger.info(f"Backfilling seasons: {seasons}")

    # Get player universe
    player_list = get_players(active_only=active_only, max_players=max_players)

    if not player_list:
        logger.warning("Player list is empty; nothing to backfill.")
        return

    all_game_logs: List[pd.DataFrame] = []
    total_requests = len(player_list) * len(seasons)
    request_count = 0

    for player in player_list:
        player_id = player["id"]
        player_name = player.get("full_name") or player.get("full_name", "Unknown")

        logger.info(f"Processing {player_name} (ID: {player_id})")

        for season in seasons:
            request_count += 1
            logger.info(f"  Fetching {season} [{request_count}/{total_requests}]")

            df = fetch_player_game_logs(player_id, season)

            if not df.empty:
                all_game_logs.append(df)
                logger.info(f"    Retrieved {len(df)} games for {player_name} in {season}")

            # Rate limiting between requests (player + season)
            time.sleep(0.6)  # ~100 requests/minute safe zone

        # Additional delay between players to avoid hammering API
        time.sleep(1.0)

    if not all_game_logs:
        logger.warning("No game logs retrieved for any player/season combination.")
        return

    log_step(logger, "Combining and Saving Data")

    combined_df = pd.concat(all_game_logs, ignore_index=True)
    logger.info(f"Total game logs retrieved: {len(combined_df)}")

    # Persist to DB — full replace of table each backfill
    write_table(combined_df, "player_game_logs", if_exists="replace")

    log_step(logger, "Backfill Complete")
    logger.info(f"Saved {len(combined_df)} game logs to 'player_game_logs' table")


def main():
    """CLI entrypoint to backfill recent NBA seasons."""
    import argparse

    current_year = datetime.now().year

    # Default to roughly "last 2 seasons"
    # Example: if current_year=2025 => start_year=2023, end_year=2024
    default_start = current_year - 2
    default_end = current_year - 1

    parser = argparse.ArgumentParser(description="Backfill NBA historical data")
    parser.add_argument(
        "--start-year",
        type=int,
        default=default_start,
        help=f"Start year (default: {default_start})",
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=default_end,
        help=f"End year (default: {default_end})",
    )
    parser.add_argument(
        "--max-players",
        type=int,
        default=None,
        help="Max players to process (default: all active players)",
    )
    parser.add_argument(
        "--active-only",
        action="store_true",
        default=True,
        help="Only include currently active players (default: True)",
    )

    args = parser.parse_args()

    logger.info(
        f"Starting backfill with start_year={args.start_year}, "
        f"end_year={args.end_year}, max_players={args.max_players}, "
        f"active_only={args.active_only}"
    )

    backfill_seasons(
        start_year=args.start_year,
        end_year=args.end_year,
        max_players=args.max_players,
        active_only=args.active_only,
    )


if __name__ == "__main__":
    main()

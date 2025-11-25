"""
Daily data pull script for NBA Projection System.
Fetches yesterday's game data from NBA API.
Author: Edwin (Ed) Bleiler
"""
import pandas as pd
import time
from datetime import datetime, timedelta
from nba_api.stats.endpoints import scoreboardv2, playergamelog
from nba_api.stats.static import players
from src.utils.fetch_utils import fetch_with_retry
from src.utils.logging import setup_logger, log_step

logger = setup_logger(__name__)


def get_yesterday_date():
    """
    Get yesterday's date in NBA API format.

    Returns:
        str: Date string in format 'MM/DD/YYYY'
    """
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%m/%d/%Y')


def get_games_for_date(game_date):
    """
    Get all games for a specific date.

    Args:
        game_date: Date string in format 'MM/DD/YYYY'

    Returns:
        pd.DataFrame: Games data
    """
    logger.info(f"Fetching games for {game_date}")

    try:
        scoreboard = fetch_with_retry(
            scoreboardv2.ScoreboardV2,
            game_date=game_date
        )

        games_df = scoreboard.get_data_frames()[0]
        logger.info(f"Found {len(games_df)} games")

        return games_df

    except Exception as e:
        logger.error(f"Failed to fetch scoreboard: {str(e)}")
        return pd.DataFrame()


def get_player_stats_for_date(game_date):
    """
    Get all player stats for games on a specific date.

    Args:
        game_date: Date string in format 'MM/DD/YYYY'

    Returns:
        pd.DataFrame: Player stats for all games on that date
    """
    # First get the games
    games_df = get_games_for_date(game_date)

    if games_df.empty:
        logger.warning("No games found for this date")
        return pd.DataFrame()

    # Get game IDs
    if 'GAME_ID' in games_df.columns:
        game_ids = games_df['GAME_ID'].unique()
        logger.info(f"Found {len(game_ids)} unique games")
    else:
        logger.warning("No GAME_ID column in games data")
        return pd.DataFrame()

    # For simplicity, we'll fetch recent player game logs
    # and filter by date (more robust than iterating through box scores)
    logger.info("Fetching player stats via game logs...")

    all_players = players.get_players()
    all_stats = []

    # Get current season
    year = datetime.now().year
    month = datetime.now().month
    season = f"{year-1}-{str(year)[-2:]}" if month < 10 else f"{year}-{str(year+1)[-2:]}"

    for i, player in enumerate(all_players[:50]):  # Limit for daily run
        try:
            player_id = player['id']

            game_log = fetch_with_retry(
                playergamelog.PlayerGameLog,
                player_id=player_id,
                season=season,
                season_type_all_star='Regular Season'
            )

            df = game_log.get_data_frames()[0]

            if not df.empty:
                # Filter to just the target date
                df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
                target_date = datetime.strptime(game_date, '%m/%d/%Y')

                df_filtered = df[df['GAME_DATE'].dt.date == target_date.date()]

                if not df_filtered.empty:
                    all_stats.append(df_filtered)

            time.sleep(0.6)

        except Exception as e:
            logger.warning(f"Failed to fetch player {player['full_name']}: {str(e)}")
            continue

    if all_stats:
        combined_df = pd.concat(all_stats, ignore_index=True)
        logger.info(f"Retrieved stats for {len(combined_df)} player-games")
        return combined_df
    else:
        logger.warning("No player stats retrieved")
        return pd.DataFrame()


def main():
    """Main execution function."""
    log_step(logger, "Starting Daily Data Pull")

    game_date = get_yesterday_date()
    logger.info(f"Target date: {game_date}")

    # Get player stats
    stats_df = get_player_stats_for_date(game_date)

    if not stats_df.empty:
        # Save to CSV for next step
        output_path = '/tmp/daily_stats.csv'
        stats_df.to_csv(output_path, index=False)
        logger.info(f"Saved {len(stats_df)} records to {output_path}")

        log_step(logger, "Daily Pull Complete")
    else:
        logger.warning("No data to save")


if __name__ == '__main__':
    main()

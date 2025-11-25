import argparse
import os
import sqlite3
import time

import pandas as pd
from nba_api.stats.endpoints import LeagueGameLog


DB_PATH = os.path.join("data", "nba_data.db")


def season_str(year_start: int) -> str:
    """
    Convert a start year like 2024 into '2024-25'.
    """
    return f"{year_start}-{str(year_start + 1)[-2:]}"


def fetch_season_logs(year_start: int) -> pd.DataFrame:
    """
    Fetch league-wide game logs for a single season.
    One row per player-game.
    """
    season = season_str(year_start)
    print(f"[backfill] Fetching logs for season {season}...")

    logs = LeagueGameLog(
        season=season,
        season_type_all_star="Regular Season"
    )
    df = logs.get_data_frames()[0]

    # Keep a focused set of columns
    keep_cols = [
        "GAME_ID",
        "GAME_DATE",
        "SEASON_ID",
        "TEAM_ID",
        "TEAM_ABBREVIATION",
        "TEAM_NAME",
        "PLAYER_ID",
        "PLAYER_NAME",
        "MIN",
        "PTS",
        "REB",
        "AST",
        "FGM",
        "FGA",
        "FG3M",
        "FG3A",
        "FTM",
        "FTA",
        "STL",
        "BLK",
        "TOV",
        "PLUS_MINUS",
    ]

    df = df[keep_cols].copy()
    df.rename(columns={
        "GAME_ID": "game_id",
        "GAME_DATE": "game_date",
        "SEASON_ID": "season_id",
        "TEAM_ID": "team_id",
        "TEAM_ABBREVIATION": "team_abbrev",
        "TEAM_NAME": "team_name",
        "PLAYER_ID": "player_id",
        "PLAYER_NAME": "player_name",
        "MIN": "minutes",
        "PTS": "pts",
        "REB": "reb",
        "AST": "ast",
    }, inplace=True)

    df["season_start_year"] = year_start
    df["season"] = season

    return df


def write_to_db(df: pd.DataFrame, db_path: str = DB_PATH) -> None:
    """
    Append data to game_logs_raw table in SQLite.
    Creates the table if it does not exist.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(
            "game_logs_raw",
            conn,
            if_exists="append",
            index=False,
        )

        # Optional de-duplication to guard against reruns
        conn.execute("""
        CREATE TABLE IF NOT EXISTS game_logs_raw_dedup AS
        SELECT DISTINCT * FROM game_logs_raw;
        """)
        conn.execute("DROP TABLE game_logs_raw;")
        conn.execute("ALTER TABLE game_logs_raw_dedup RENAME TO game_logs_raw;")
        conn.commit()
    finally:
        conn.close()


def backfill_range(start_year: int, end_year: int) -> None:
    """
    Pull league-wide logs for start_year <= y < end_year.
    Example: start_year=2024, end_year=2026 pulls 2024-25 and 2025-26.
    """
    all_frames = []

    for year in range(start_year, end_year):
        df_season = fetch_season_logs(year)
        all_frames.append(df_season)
        time.sleep(1.0)  # light throttle for the API

    if not all_frames:
        print("[backfill] No seasons requested, nothing to do.")
        return

    full = pd.concat(all_frames, ignore_index=True)
    print(f"[backfill] Total rows fetched: {len(full):,}")
    write_to_db(full)
    print("[backfill] Finished writing game_logs_raw.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill league-wide NBA game logs into game_logs_raw"
    )
    parser.add_argument(
        "--start-year",
        type=int,
        required=True,
        help="First season start year to pull, e.g. 2024 for 2024-25.",
    )
    parser.add_argument(
        "--end-year",
        type=int,
        required=True,
        help="One past the last season start year to pull, e.g. 2026 pulls 2024-25 and 2025-26 with start-year=2024.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"[backfill] Backfilling league logs from {args.start_year} to {args.end_year} (exclusive)...")
    backfill_range(args.start_year, args.end_year)
    print("[backfill] Done.")


if __name__ == "__main__":
    main()

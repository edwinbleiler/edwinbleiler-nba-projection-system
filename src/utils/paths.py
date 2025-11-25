"""
Path utilities for NBA Projection System.
Handles consistent path resolution across the project.
Author: Edwin (Ed) Bleiler
"""
import os
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_dir():
    """Get the data directory path."""
    return get_project_root() / "data"


def get_outputs_dir():
    """Get the outputs directory path."""
    return get_project_root() / "outputs"


def get_projections_dir():
    """Get the projections output directory path."""
    return get_outputs_dir() / "projections"


def get_db_path():
    """Get the SQLite database path."""
    return get_data_dir() / "nba_data.db"


def ensure_dirs_exist():
    """Create all necessary directories if they don't exist."""
    get_data_dir().mkdir(parents=True, exist_ok=True)
    get_outputs_dir().mkdir(parents=True, exist_ok=True)
    get_projections_dir().mkdir(parents=True, exist_ok=True)

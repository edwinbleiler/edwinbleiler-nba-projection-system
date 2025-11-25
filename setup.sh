#!/bin/bash

# Setup script for NBA Player Projection System
# Author: Edwin (Ed) Bleiler
# Description: Initializes the project, runs backfill, builds features, trains models

set -e  # Exit on any error

echo "============================================"
echo "NBA Player Projection System - Setup"
echo "Author: Edwin (Ed) Bleiler"
echo "============================================"
echo ""

# Check Python version
echo "[1/8] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "[2/8] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping."
else
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo ""
echo "[3/8] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "[4/8] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed."

# Run historical backfill - aggregate league logs
echo ""
echo "[5/8] Running historical backfill (2024-2026, league logs)..."
echo "This pulls league-wide game logs and stores them as raw data."
python -m src.backfill.backfill_league_logs --start-year 2024 --end-year 2026
echo "Backfill complete."

# Build features
echo ""
echo "[6/8] Building features..."
python -m src.features.feature_engineering
echo "Features built."

# Build model dataset
echo ""
echo "[7/8] Building model dataset..."
python -m src.model.utils
echo "Model dataset ready."

# Train models
echo ""
echo "[8/8] Training models..."
echo ""
echo "Training minutes model..."
python -m src.model.train_minutes_model
echo ""
echo "Training rate models..."
python -m src.model.train_rate_models
echo "All models trained."

# Generate initial projections
echo ""
echo "[BONUS] Generating initial projections..."
python -m src.daily.run_projections
echo "Projections generated."

# Summary
echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "Database location: data/nba_data.db"
echo "Projections: outputs/projections/projections_latest.csv"
echo ""
echo "To run the daily pipeline:"
echo "  source venv/bin/activate"
echo "  python -m src.daily.pull_day"
echo "  python -m src.daily.ingest_day"
echo "  python -m src.daily.update_features"
echo "  python -m src.daily.update_model_data"
echo "  python -m src.daily.run_projections"
echo ""
echo "For more information, see README.md"
echo "============================================"

# NBA Player Projection System

**An end-to-end NBA Machine Learning Pipeline for player performance prediction**

Built by [Edwin (Ed) Bleiler](https://edwinbleiler.com) | [LinkedIn](https://www.linkedin.com/in/edwin-ed-bleiler) | [GitHub](https://github.com/edwinbleiler)

---

## Overview

This **NBA Player Projection System** is a comprehensive **Python SQL Machine Learning** pipeline that predicts NBA player performance using historical game data, advanced feature engineering, and **LightGBM Minutes Model** predictions. The system combines **Data Engineering** best practices with modern machine learning to deliver daily player projections.

## Key Features

- **Historical Data Backfill**: Automatically fetch and store NBA game logs from multiple seasons using the `nba_api`
- **Daily Ingestion Pipeline**: Incremental data updates with deduplication
- **Feature Engineering**: Rolling averages, per-minute rates, and advanced statistics
- **Machine Learning Models**:
  - **LightGBM Minutes Model**: Predicts playing time
  - **Rate Models**: Predicts per-minute statistics (points, rebounds, assists, etc.)
- **Automated CI/CD GitHub Actions**: Daily pipeline execution with artifact management
- **SQLite Database**: Efficient local data storage and querying

## Technology Stack

- **Python 3.x**
- **Pandas & NumPy**: Data manipulation
- **LightGBM**: Gradient boosting models
- **scikit-learn**: Model evaluation and utilities
- **nba_api**: Official NBA statistics API wrapper
- **SQLite**: Embedded database
- **GitHub Actions**: CI/CD automation

## Project Structure

```
edwinbleiler-nba-projection-system/
├── data/                          # SQLite database and models
├── outputs/
│   └── projections/              # Generated projections (CSV)
├── src/
│   ├── utils/                    # Utility modules
│   │   ├── paths.py             # Path resolution
│   │   ├── logging.py           # Logging configuration
│   │   ├── db.py                # Database operations
│   │   └── fetch_utils.py       # API fetch utilities
│   ├── backfill/
│   │   └── backfill_history.py  # Historical data backfill
│   ├── daily/                    # Daily pipeline scripts
│   │   ├── pull_day.py          # Fetch daily data
│   │   ├── ingest_day.py        # Ingest into database
│   │   ├── update_features.py   # Rebuild features
│   │   ├── update_model_data.py # Update model dataset
│   │   └── run_projections.py   # Generate projections
│   ├── features/
│   │   └── feature_engineering.py # Feature engineering pipeline
│   └── model/                    # Machine learning models
│       ├── utils.py             # Model utilities
│       ├── train_minutes_model.py   # Train minutes model
│       ├── train_rate_models.py     # Train rate models
│       ├── predict_minutes.py       # Predict minutes
│       └── predict_rates.py         # Predict rates
├── .github/
│   └── workflows/
│       └── daily_pipeline.yaml  # CI/CD workflow
├── requirements.txt              # Python dependencies
├── setup.sh                      # Setup and initialization script
├── CLAUDE.md                     # Development guidelines
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- 2GB disk space (for historical data)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/edwinbleiler/edwinbleiler-nba-projection-system.git
   cd edwinbleiler-nba-projection-system
   ```

2. **Run the setup script**:
   ```bash
   bash setup.sh
   ```

   This script will:
   - Create a Python virtual environment
   - Install dependencies from `requirements.txt`
   - Run the historical backfill (2018-2024 seasons)
   - Build features
   - Prepare model dataset
   - Train all machine learning models
   - Generate initial projections

### Manual Setup

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backfill
python -m src.backfill.backfill_history

# Build features
python -m src.features.feature_engineering

# Build model dataset
python -m src.model.utils

# Train models
python -m src.model.train_minutes_model
python -m src.model.train_rate_models

# Generate projections
python -m src.daily.run_projections
```

## Usage

### Running the Daily Pipeline

The daily pipeline fetches yesterday's games and updates projections:

```bash
# Activate virtual environment
source venv/bin/activate

# Run daily pipeline
python -m src.daily.pull_day           # Fetch yesterday's data
python -m src.daily.ingest_day         # Ingest into database
python -m src.daily.update_features    # Rebuild features
python -m src.daily.update_model_data  # Update model dataset
python -m src.daily.run_projections    # Generate new projections
```

### Viewing Projections

Projections are saved to `outputs/projections/`:

```bash
# View latest projections
cat outputs/projections/projections_latest.csv
```

### Retraining Models

To retrain models with updated data:

```bash
python -m src.model.train_minutes_model
python -m src.model.train_rate_models
```

## CI/CD with GitHub Actions

The system includes automated daily execution via **GitHub Actions**.

**Workflow**: `.github/workflows/daily_pipeline.yaml`

**Trigger**: Runs daily at 2 AM UTC (or manually via workflow_dispatch)

**Steps**:
1. Check out repository
2. Download previous day's database artifact
3. Set up Python environment
4. Install dependencies
5. Run daily ingestion pipeline
6. Rebuild features and model data
7. Generate projections
8. Upload updated database and projections as artifacts

**Artifacts**:
- `nba-database`: SQLite database with historical and daily data
- `projections`: Latest player projections (CSV)

## Feature Engineering

The system calculates:

- **Rolling Averages**: 3, 5, 10, and 20-game windows for all stats
- **Per-Minute Rates**: Points, rebounds, assists, steals, blocks per minute
- **Advanced Features**:
  - Days rest between games
  - Home/away indicators
  - Season game number
  - Usage rate proxies

## Machine Learning Models

### Minutes Model (LightGBM)

Predicts playing time based on:
- Recent performance (rolling averages)
- Historical patterns
- Rest and schedule factors

### Rate Models (LightGBM)

Separate models for each stat:
- Points per minute
- Rebounds per minute
- Assists per minute
- Steals per minute
- Blocks per minute
- Field goal percentage
- Free throw percentage

**Final Projections** = Predicted Minutes × Predicted Rates

## Data Engineering Best Practices

- **Incremental Updates**: Only new data is added to the database
- **Deduplication**: Prevents duplicate records
- **Error Handling**: Retry logic with exponential backoff for API calls
- **Logging**: Comprehensive logging throughout the pipeline
- **Modular Design**: Separate modules for utilities, ingestion, features, and models
- **Version Control**: All code tracked in Git
- **CI/CD**: Automated testing and deployment via GitHub Actions

## Performance

- **Minutes Model MAE**: ~4-6 minutes (typical)
- **Rate Model MAE**: Varies by stat (e.g., ~0.02-0.05 points per minute)
- **Backfill Time**: ~30-60 minutes for 7 seasons
- **Daily Pipeline**: ~5-10 minutes

## Future Enhancements

- Integration with real-time injury reports
- Team-level features (pace, defensive rating)
- Opponent-adjusted projections
- Web dashboard for visualization
- REST API for projections
- Advanced models (neural networks, ensemble methods)
- Player clustering and similarity analysis

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## About the Author

**Edwin (Ed) Bleiler** is a data engineer and machine learning practitioner specializing in sports analytics, Python development, and scalable data pipelines.

- **Website**: [https://edwinbleiler.com](https://edwinbleiler.com)
- **LinkedIn**: [https://www.linkedin.com/in/edwin-ed-bleiler](https://www.linkedin.com/in/edwin-ed-bleiler)
- **GitHub**: [https://github.com/edwinbleiler](https://github.com/edwinbleiler)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **nba_api**: For providing comprehensive NBA statistics
- **LightGBM**: For fast and efficient gradient boosting
- **Python Data Science Community**: For excellent tools and libraries

---

**Keywords**: NBA Player Projection System, NBA Machine Learning Pipeline, Python SQL Machine Learning, Edwin (Ed) Bleiler, Data Engineering, CI/CD GitHub Actions, LightGBM Minutes Model, Sports Analytics, Basketball Predictions, Feature Engineering, Automated Data Pipeline

---

*Built with Python, LightGBM, and passion for basketball analytics.*

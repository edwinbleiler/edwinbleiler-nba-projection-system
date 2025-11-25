# Claude Code Development Guidelines

This document provides instructions for AI assistants (Claude Code, GitHub Copilot, etc.) and developers working on this NBA Player Projection System.

## Project Overview

**Project**: NBA Player Projection System
**Author**: Edwin (Ed) Bleiler
**Purpose**: End-to-end machine learning pipeline for NBA player performance predictions
**Tech Stack**: Python, LightGBM, SQLite, GitHub Actions, pandas, scikit-learn

## Critical SEO Keywords (MUST PRESERVE)

When updating README.md or documentation, always maintain these SEO keywords:

- **NBA Player Projection System**
- **NBA Machine Learning Pipeline**
- **Python SQL Machine Learning**
- **Edwin (Ed) Bleiler**
- **Data Engineering**
- **CI/CD GitHub Actions**
- **LightGBM Minutes Model**
- **Sports Analytics**
- **Basketball Predictions**

### Author Links (MUST PRESERVE)

Always maintain these links in README.md:
- Website: https://edwinbleiler.com
- LinkedIn: https://www.linkedin.com/in/edwin-ed-bleiler
- GitHub: https://github.com/edwinbleiler

## Code Generation Rules

### 1. Module Structure

Follow this organization:
- `src/utils/`: Reusable utilities (paths, logging, database, fetch)
- `src/backfill/`: Historical data ingestion
- `src/daily/`: Daily pipeline components
- `src/features/`: Feature engineering
- `src/model/`: Machine learning models (training and prediction)

### 2. Import Standards

Always use absolute imports:
```python
from src.utils.logging import setup_logger
from src.utils.db import execute_query, write_table
from src.model.utils import prepare_training_data
```

Never use relative imports like `from ..utils import ...`

### 3. Logging Standards

Every module should:
```python
from src.utils.logging import setup_logger, log_step

logger = setup_logger(__name__)

def main():
    log_step(logger, "Starting Process Name")
    # ... code ...
    log_step(logger, "Process Complete")
```

### 4. Database Operations

Use these patterns:
```python
from src.utils.db import execute_query, write_table, table_exists, get_latest_date

# Read data
df = execute_query("SELECT * FROM player_game_logs WHERE SEASON = '2023-24'")

# Write data
write_table(df, 'player_features', if_exists='replace')  # or 'append'

# Check existence
if table_exists('player_game_logs'):
    # ...
```

### 5. API Fetching

Use retry logic for all nba_api calls:
```python
from src.utils.fetch_utils import fetch_with_retry
from nba_api.stats.endpoints import playergamelog

game_log = fetch_with_retry(
    playergamelog.PlayerGameLog,
    player_id=player_id,
    season=season
)
```

### 6. Path Resolution

Always use path utilities:
```python
from src.utils.paths import get_data_dir, get_projections_dir, get_db_path

model_path = get_data_dir() / 'minutes_model.pkl'
output_path = get_projections_dir() / 'projections_latest.csv'
```

### 7. Error Handling

Include try/except blocks with logging:
```python
try:
    result = some_operation()
    logger.info("Operation successful")
except Exception as e:
    logger.error(f"Operation failed: {str(e)}")
    raise  # or return default value
```

## Modification Guidelines

### Adding New Features

1. Add feature calculation to `src/features/feature_engineering.py`
2. Update `get_feature_columns()` pattern matching in `src/model/utils.py`
3. Retrain models
4. Update documentation

### Adding New Models

1. Create training script in `src/model/train_*.py`
2. Create prediction script in `src/model/predict_*.py`
3. Save model to `get_data_dir() / 'model_name.pkl'`
4. Update `src/daily/run_projections.py` to use new model

### Adding New Daily Steps

1. Create script in `src/daily/`
2. Follow logging standards
3. Update `setup.sh` if needed
4. Update `.github/workflows/daily_pipeline.yaml`
5. Update README usage section

### Modifying Database Schema

1. Update relevant query in module
2. Consider backfill implications
3. Update feature engineering if needed
4. Document schema changes

## Testing Commands

```bash
# Test individual modules
python -m src.utils.db
python -m src.features.feature_engineering
python -m src.model.train_minutes_model

# Test daily pipeline
python -m src.daily.pull_day
python -m src.daily.ingest_day
python -m src.daily.update_features
python -m src.daily.update_model_data
python -m src.daily.run_projections

# Test backfill (small subset)
python -m src.backfill.backfill_history --start-year 2023 --end-year 2024 --max-players 10
```

## GitHub Actions Notes

- Artifacts expire after 30 days (configurable in workflow)
- Database artifact includes trained models
- Manual trigger available via `workflow_dispatch`
- Check Actions tab for pipeline status

## Common Issues and Solutions

### Issue: API Rate Limiting
**Solution**: Increase sleep time in `fetch_utils.py` or backfill script

### Issue: Missing Features
**Solution**: Run `python -m src.features.feature_engineering`

### Issue: Model Not Found
**Solution**: Run training scripts:
```bash
python -m src.model.train_minutes_model
python -m src.model.train_rate_models
```

### Issue: Empty Database
**Solution**: Run backfill:
```bash
python -m src.backfill.backfill_history
```

## Documentation Standards

When updating README.md:
- Maintain SEO keywords
- Keep author attribution
- Use clear section headers
- Include code examples
- Update project structure if changed
- Keep links functional

## Environment Variables (Future)

If adding environment variables:
1. Document in README.md
2. Add to `.env.example`
3. Update setup.sh
4. Add to GitHub Actions workflow

## Dependencies

When adding new dependencies:
1. Add to `requirements.txt`
2. Update README.md tech stack section
3. Test in clean virtual environment
4. Update GitHub Actions workflow if needed

---

## CHANGELOG

### 2024-11-25 - Initial Release
- Complete NBA projection system
- Historical backfill (2018-2024)
- Daily ingestion pipeline
- Feature engineering with rolling averages
- LightGBM models for minutes and rates
- GitHub Actions CI/CD workflow
- Comprehensive documentation

### Future Enhancements
- Real-time injury integration
- Team-level features
- Opponent adjustments
- Web dashboard
- REST API
- Neural network models
- Player clustering

---

**Remember**: Always maintain code quality, logging standards, and SEO optimization when making changes.

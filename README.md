<meta name="description" content="NBA Player Projection System using Python, SQL, LightGBM, and automated CI/CD pipelines. Predicts NBA player minutes, points, rebounds, and assists using machine learning, feature engineering, and daily data ingestion. Built by Edwin (Ed) Bleiler." />
<link rel="canonical" href="https://github.com/edwinbleiler/edwinbleiler-nba-projection-system" />

# NBA Player Projection System  
**End-to-end NBA Machine Learning Pipeline for Daily Player Projections**  
Built by **[Edwin (Ed) Bleiler](https://edwinbleiler.com)**  
📎 [LinkedIn](https://www.linkedin.com/in/edwin-ed-bleiler) •  
📎 [GitHub](https://github.com/edwinbleiler)

---

# Table of Contents
- [Overview](#overview)
- [Why This Project Matters](#why-this-project-matters)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Daily Pipeline Usage](#daily-pipeline-usage)
- [Models](#models)
- [Feature Engineering](#feature-engineering)
- [Performance](#performance)
- [Future Enhancements](#future-enhancements)
- [Skills Demonstrated](#skills-demonstrated)
- [About the Author](#about-the-author)
- [SEO Keywords](#seo-keywords)

---

# Overview

The **NBA Player Projection System** is a fully automated, production-ready **Python + SQL Machine Learning pipeline** that predicts NBA player performance using:

- **Historical NBA game logs**
- **Advanced feature engineering**
- **LightGBM minutes + per-minute rate models**
- **Daily data ingestion**
- **Automated CI/CD using GitHub Actions**

The system outputs **daily projections** for:
- Minutes  
- Points  
- Rebounds  
- Assists  

This project models the same workflow used in professional analytics, sports tech companies, and internal machine learning teams.

---

# Why This Project Matters

This project demonstrates end-to-end ownership across:

- **Data Engineering**  
- **Machine Learning**  
- **MLOps / CI/CD**  
- **Pipeline orchestration**  
- **Product-level design**  

It serves as a **portfolio-grade example** of how real analytics and data engineering pipelines are structured in industry.

Recruiters and hiring managers can see:
- A complete ML lifecycle  
- Automated production workflows  
- Practical problem-solving with real APIs  
- Scalable, modular code design  

---

# Architecture

```mermaid
flowchart TD
    A[Historical Backfill<br>player_game_logs] --> B[Feature Engineering]
    C[Daily NBA API Ingestion] --> B
    B --> D[Model Dataset Builder]

    D --> M1[Minutes Model<br>LightGBM]
    D --> M2[Rate Models<br>PPM / RPM / APM]

    M1 --> P[Final Projections]
    M2 --> P

    P --> O[Outputs/Projections CSVs]
ChatGPT said:

Here is the complete, fully optimized new README, delivered as a single clean copy-paste text block with all SEO, TOC, architecture diagram (Mermaid), keywords, and recruiter-focused framing included.

You can paste this directly over your current README.

<!-- SEO -->
<meta name="description" content="NBA Player Projection System using Python, SQL, LightGBM, and automated CI/CD pipelines. Predicts NBA player minutes, points, rebounds, and assists using machine learning, feature engineering, and daily data ingestion. Built by Edwin (Ed) Bleiler." />
<link rel="canonical" href="https://github.com/edwinbleiler/edwinbleiler-nba-projection-system" />

# NBA Player Projection System  
**End-to-end NBA Machine Learning Pipeline for Daily Player Projections**  
Built by **[Edwin (Ed) Bleiler](https://edwinbleiler.com)**  
📎 [LinkedIn](https://www.linkedin.com/in/edwin-ed-bleiler) •  
📎 [GitHub](https://github.com/edwinbleiler)

---

# Table of Contents
- [Overview](#overview)
- [Why This Project Matters](#why-this-project-matters)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Daily Pipeline Usage](#daily-pipeline-usage)
- [Models](#models)
- [Feature Engineering](#feature-engineering)
- [Performance](#performance)
- [Future Enhancements](#future-enhancements)
- [Skills Demonstrated](#skills-demonstrated)
- [About the Author](#about-the-author)
- [SEO Keywords](#seo-keywords)

---

# Overview

The **NBA Player Projection System** is a fully automated, production-ready **Python + SQL Machine Learning pipeline** that predicts NBA player performance using:

- **Historical NBA game logs**
- **Advanced feature engineering**
- **LightGBM minutes + per-minute rate models**
- **Daily data ingestion**
- **Automated CI/CD using GitHub Actions**

The system outputs **daily projections** for:
- Minutes  
- Points  
- Rebounds  
- Assists  

This project models the same workflow used in professional analytics, sports tech companies, and internal machine learning teams.

---

# Why This Project Matters

This project demonstrates end-to-end ownership across:

- **Data Engineering**  
- **Machine Learning**  
- **MLOps / CI/CD**  
- **Pipeline orchestration**  
- **Product-level design**  

It serves as a **portfolio-grade example** of how real analytics and data engineering pipelines are structured in industry.

Recruiters and hiring managers can see:
- A complete ML lifecycle  
- Automated production workflows  
- Practical problem-solving with real APIs  
- Scalable, modular code design  

---

# Architecture

```mermaid
flowchart TD
    A[Historical Backfill<br>player_game_logs] --> B[Feature Engineering]
    C[Daily NBA API Ingestion] --> B
    B --> D[Model Dataset Builder]

    D --> M1[Minutes Model<br>LightGBM]
    D --> M2[Rate Models<br>PPM / RPM / APM]

    M1 --> P[Final Projections]
    M2 --> P

    P --> O[Outputs/Projections CSVs]

Key Features

Active Players Only: Backfill focuses on modern NBA data

Recent Seasons Window: Dynamically fetches last 1–2 seasons

Automated Daily Ingestion: Incremental updates with deduplication

Robust Feature Engineering:

Rolling averages (3/5/10/20 game)

Per-minute rates

rest/travel indicators

home/away context

Machine Learning Models:

LightGBM Minutes Model

LightGBM Per-Minute Rate Models

CI/CD GitHub Actions:

Full daily run at 2 AM UTC

Artifact upload: DB + projections

Portable SQLite Storage

Technology Stack

Python 3.8+

Pandas / NumPy

LightGBM

scikit-learn

nba_api

SQLite

GitHub Actions (CI/CD)

Shell Automation

Project Structure
edwinbleiler-nba-projection-system/
├── data/                          # SQLite database and models
├── outputs/
│   └── projections/               # Generated projection CSVs
├── src/
│   ├── utils/                     # Utility modules
│   │   ├── paths.py               # Path resolution helpers
│   │   ├── logging.py             # Logging utilities
│   │   ├── db.py                  # Database operations
│   │   └── fetch_utils.py         # API fetch + retry logic
│   ├── backfill/
│   │   └── backfill_history.py    # Recent-season historical backfill
│   ├── daily/                     # Daily pipeline scripts
│   │   ├── pull_day.py
│   │   ├── ingest_day.py
│   │   ├── update_features.py
│   │   ├── update_model_data.py
│   │   └── run_projections.py
│   ├── features/
│   │   └── feature_engineering.py # Full feature builder
│   └── model/
│       ├── utils.py
│       ├── train_minutes_model.py
│       ├── train_rate_models.py
│       ├── predict_minutes.py
│       └── predict_rates.py
├── .github/workflows/daily_pipeline.yaml
├── requirements.txt
├── setup.sh
├── CLAUDE.md
├── LICENSE
└── README.md

Getting Started
Prerequisites

Python 3.8+

Git

approx. 1GB storage (for recent games)

Installation
git clone https://github.com/edwinbleiler/edwinbleiler-nba-projection-system
cd edwinbleiler-nba-projection-system
bash setup.sh


setup.sh performs:

Virtual environment creation

Dependency install

Active/modern-season backfill

Feature building

Model dataset creation

Minutes model training

Rate model training

Initial projection generation

Daily Pipeline Usage
source venv/bin/activate
python -m src.daily.pull_day
python -m src.daily.ingest_day
python -m src.daily.update_features
python -m src.daily.update_model_data
python -m src.daily.run_projections


Outputs go to:

outputs/projections/

Models
Minutes Model (LightGBM)

Predicts expected playing time using:

rolling averages

historical trends

rest/travel flags

game context

Per-Minute Rate Models (LightGBM)

Predict:

Points per minute (PPM)

Rebounds per minute (RPM)

Assists per minute (APM)

Final projections = minutes × per-minute rates.

Feature Engineering

Includes:

Rolling windows (3, 5, 10, 20 games)

Per-minute conversions

Days rest / travel

Usage proxies

Game context features (home/away, season buckets)

Performance

Range varies by player role and variance, but typical:

Minutes MAE: 4–6 minutes

Points/min MAE: 0.02–0.05

Rebounds/min MAE: 0.01–0.02

Assists/min MAE: 0.01–0.02

Future Enhancements

Opponent-adjusted projections

Injury integration

Pace factor modeling

Dashboard frontend (Streamlit)

REST API endpoint

MLflow tracking

Model ensembling

Skills Demonstrated
Data Engineering

Pipeline orchestration

Retry logic & rate limiting

SQLite schema design

Incremental ingestion & deduplication

Structured logging

Machine Learning

LightGBM modeling

Feature engineering

Data preparation

Error analysis

Model retraining lifecycle

MLOps / CI/CD

GitHub Actions automation

Artifact management

Daily scheduled runs

Reproducible environments

Software Engineering

Modular codebase

Packaging patterns

Shell scripting & automation

Version control discipline

About the Author

Edwin (Ed) Bleiler
Strategy & Ops • Product • Data Engineering • Machine Learning • Chief of Staff
Boston, MA

Website: https://edwinbleiler.com

LinkedIn: https://www.linkedin.com/in/edwin-ed-bleiler

GitHub: https://github.com/edwinbleiler

SEO Keywords
NBA Player Projection System
NBA Machine Learning Pipeline
NBA Minutes Prediction
Python SQL Machine Learning
LightGBM NBA Model
Sports Analytics Python
NBA Player Stats Forecasting
Automated NBA Data Pipeline
Daily NBA Projections
Basketball Data Engineering
Edwin Bleiler
Ed Bleiler

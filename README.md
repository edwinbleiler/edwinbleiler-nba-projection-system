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
- **Automated CI/CD via GitHub Actions**

The system produces **daily projections** for:
- Minutes  
- Points  
- Rebounds  
- Assists  

---

# Why This Project Matters

This project demonstrates real-world end-to-end ownership in:

- Data Engineering  
- Machine Learning  
- MLOps / CI/CD  
- Modeling strategy  
- Pipeline orchestration  

It is designed as a **portfolio-grade example** of modern analytics engineering.

This project shows:
- System design thinking  
- Robust pipeline architecture  
- Modeling fundamentals  
- Code modularity  
- Automated production workflows  

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

# Key Features

Active Players Only (no historical noise)

Recent Seasons Only (dynamic defaults)

Automated Daily Ingestion

Rolling & Rate-Based Feature Engineering

LightGBM Machine Learning Models

GitHub Actions CI/CD

Portable SQLite Storage

# Technology Stack

Python 3.8+

Pandas / NumPy

LightGBM

scikit-learn

nba_api

SQLite

GitHub Actions

# Project Structure
edwinbleiler-nba-projection-system/
├── data/
├── outputs/
│   └── projections/
├── src/
│   ├── utils/
│   ├── backfill/
│   ├── daily/
│   ├── features/
│   └── model/
├── .github/workflows/
├── requirements.txt
├── setup.sh
├── CLAUDE.md
└── README.md

# Getting Started
Prerequisites

Python 3.8+

Git

Installation
git clone https://github.com/edwinbleiler/edwinbleiler-nba-projection-system
cd edwinbleiler-nba-projection-system
bash setup.sh

# Daily Pipeline Usage
source venv/bin/activate
python -m src.daily.pull_day
python -m src.daily.ingest_day
python -m src.daily.update_features
python -m src.daily.update_model_data
python -m src.daily.run_projections


Outputs will appear in:

outputs/projections/

# Models
Minutes Model

Predicts expected playing time based on:

Rolling averages

Game context

Rest/travel

Rate Models

For each stat, predicts:

Points per minute

Rebounds per minute

Assists per minute

Final Projections = Minutes × Rates

# Feature Engineering

Includes:

Rolling windows

Per-minute rates

Home/away indicators

Rest/travel metrics

Usage proxies

# Performance

Typical ranges on modern NBA data:

Minutes MAE: 4–6 minutes

Points rate MAE: 0.02–0.05

Rebounds rate MAE: 0.01–0.02

Assists rate MAE: 0.01–0.02

# Future Enhancements

Opponent-adjusted projections

Injury model integration

Pace & defensive efficiency factors

Dashboard visualization (Streamlit)

REST API endpoint

MLflow experiment tracking

# Skills Demonstrated
Data Engineering

Pipeline design

Retry logic

Incremental ingestion

SQLite schema work

Structured logging

Machine Learning

LightGBM

Feature engineering

Evaluation and validation

Model lifecycle management

MLOps

GitHub Actions

Daily scheduled runs

Artifact management

Reproducible environments

Software Engineering

Modular architecture

Reusable utility modules

Shell scripting

Version control workflows

# About the Author

Edwin (Ed) Bleiler
Strategy & Ops • Product • Data Engineering • Machine Learning
Boston, MA

https://edwinbleiler.com

https://www.linkedin.com/in/edwin-ed-bleiler

https://github.com/edwinbleiler

# SEO Keywords
NBA Player Projection System
NBA Machine Learning Pipeline
NBA Minutes Prediction
Python SQL Machine Learning
LightGBM NBA Model
Sports Analytics Python
NBA Player Stats Forecasting
Daily NBA Projections
Basketball Data Engineering
Edwin Bleiler
Ed Bleiler

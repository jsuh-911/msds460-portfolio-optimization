# MSDS 460 - Portfolio Optimization

## Overview
Linear programming approach to financial portfolio optimization. Selecting allocations across 30 large-cap US equities that maximize expected return while managing risk under real-world constraints.

## Team
- Rachel Raia
- Jung Suh
- Scott Keighley

## Course
MSDS 460: Decision Analytics | Northwestern University | Dr. Kline

## Data
- **Source:** Yahoo Finance (yfinance API)
- **Universe:** 30 S&P 500 large-cap equities across 10 sectors
- **Window:** 10 years monthly adjusted close prices
- **Evaluation:** Walk-forward backtest, one month rolling

## Project Structure
```
├── data/                # Raw and processed data (CSVs)
├── notebooks/           # Exploratory analysis and modeling
├── src/                 # Source scripts (data pull, optimization)
├── requirements.txt
└── README.md
```

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/pull_data.py
```

## Methods
- Linear programming (PuLP) for portfolio allocation
- Mean absolute deviation as LP-compatible risk measure
- Comparison against Markowitz quadratic formulation (extension)
- Backtesting against S&P 500 benchmark

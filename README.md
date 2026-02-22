# Crypto Price Prediction with Rolling Backtesting and Baselines

**Machine Learning and Data Mining**  
ECPS 211 — Winter 2026 Final Project

Predict **next-day** cryptocurrency price (regression) using rolling backtesting, baselines, lag-feature models, and an LSTM. Meets course-wide requirements (pipelines, hyperparameter search, interpretability, error analysis).

## Setup

```bash
cd crypto-price-prediction
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Data

- **Asset:** BTC-USD (or set in code).
- **Source:** e.g. Yahoo Finance via `yfinance`. See notebook for download and date range.
- **Storage:** Save raw or processed series in `data/` (folder is gitignored by default; add a small sample to repo or document download steps in the notebook).

## Reproducing results

1. Install dependencies (above).
2. Run the main notebook(s) in `notebooks/` in order (data → baselines → lag model → LSTM → ablation → interpretability).
3. Report and slides are in `docs/` (or linked from this repo).

## Project plan and timeline

See [TEAM_PLAN.md](TEAM_PLAN.md) for the full timeline, phase breakdown, and task ownership.

## Deliverables

- Written report  
- Presentation slides  
- Python code that reproduces results (this repo)

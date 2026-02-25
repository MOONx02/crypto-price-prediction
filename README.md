# Crypto Price Prediction

**Machine Learning and Data Mining** — ECPS 211 Winter 2026 Final Project

Predict **next-day** cryptocurrency price using rolling backtesting, baselines (last value, 7-day MA), a lag-feature Ridge model, and an LSTM. Includes time-series CV, ablation (volume, volatility), permutation importance, PDP/ICE, and error analysis.

---

## Quick start

### Option 1: Google Colab (no install)

1. Open **[notebooks/Crypto_Colab_AllInOne_v6.ipynb](notebooks/Crypto_Colab_AllInOne_v6.ipynb)**.
2. In Colab: **File → Upload notebook** (or open from GitHub), then **Runtime → Run all**.
3. Change asset in the config cell if desired: `ASSET = "BTC-USD"` | `"ETH-USD"` | `"XRP-USD"` | `"ETC-USD"`.

Optional: **Runtime → Change runtime type → GPU** for faster LSTM.

### Option 2: Local

```bash
git clone https://github.com/MOONx02/crypto-price-prediction.git
cd crypto-price-prediction
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then run `notebooks/Crypto_Colab_AllInOne_v6.ipynb` (Jupyter or VS Code). Python 3.11 or 3.12 recommended (TensorFlow compatibility).

---

## Deliverables

| Deliverable | Location |
|-------------|----------|
| **Report** | [REPORT.md](REPORT.md) — intro, data, methods, results (baselines, Lag+Ridge, LSTM, ablation, interpretability, error analysis), conclusion |
| **Slides** | [Crypto_Price_Prediction_Slides.pptx](Crypto_Price_Prediction_Slides.pptx) — presentation aligned with report |
| **Code** | This repo. Single notebook reproduces all results: [notebooks/Crypto_Colab_AllInOne_v6.ipynb](notebooks/Crypto_Colab_AllInOne_v6.ipynb) |

---

## Repo structure

```
crypto-price-prediction/
├── README.md                 # this file
├── REPORT.md                 # full written report
├── Crypto_Price_Prediction_Slides.pptx
├── requirements.txt
├── TEAM_PLAN.md              # phase breakdown and timeline
├── PROGRESS_LOG.md           # what was done and when
├── notebooks/
│   ├── Crypto_Colab_AllInOne_v6.ipynb   # main notebook (run this)
│   ├── README.md             # version history and asset config
│   └── archive/              # older notebook versions
├── data/                     # parquet cache (created on first run)
└── src/                      # optional metrics module
```

---

## What the notebook does

1. **Data** — Download daily OHLCV (yfinance), derive returns and 14-day volatility; 70/15/15 time split.
2. **Baselines** — Last value, 7-day moving average; MAE, RMSE, directional accuracy.
3. **Lag+Ridge** — 30 lags + log_volume + volatility_14; `ColumnTransformer` + `Pipeline`; TimeSeriesSplit + RandomizedSearchCV (Ridge alpha); rolling backtest.
4. **LSTM** — 30-step sequences (return, log_volume, volatility); predict next-day return → price; same metrics.
5. **Ablation** — Lags only / +volume / +volatility / all; compare MAE, RMSE, Dir.Acc.
6. **Interpretability** — Permutation importance (best Lag+Ridge), PDP and ICE for 1–2 features.
7. **Error analysis** — Residual plots and “where the model performs poorly.”

---

## Results at a glance (ETC-USD example)

| Model | MAE | RMSE | Dir.Acc |
|-------|-----|------|---------|
| Last value | **0.58** | **0.87** | — |
| 7-day MA | 0.89 | 1.30 | **55.3%** |
| Lag+Ridge (best CV) | 0.90 | 1.18 | 53.2% |
| LSTM | 0.61 | 0.90 | 45.6% |

Last value wins on MAE/RMSE; 7-day MA and Lag+Ridge best on direction. See [REPORT.md](REPORT.md) for full tables and cross-asset summary.

---

## Course requirements

- [x] Two baselines (last value, moving average)
- [x] Time-based split only; no shuffle
- [x] MAE, RMSE, directional accuracy
- [x] Baseline + at least two improved models (lag model, LSTM)
- [x] ColumnTransformer + Pipeline
- [x] RandomizedSearchCV with time-series CV
- [x] Rolling backtest
- [x] LSTM compared to baselines and lag model
- [x] Ablation (volume, rolling volatility)
- [x] Error analysis (residual plots + where model fails)
- [x] Interpretability (permutation importance + PDP/ICE)
- [x] Report + slides + reproducible code

---

## References

- **Plan and timeline:** [TEAM_PLAN.md](TEAM_PLAN.md)
- **Progress log:** [PROGRESS_LOG.md](PROGRESS_LOG.md)
- **Colab (clone-based):** [COLAB.md](COLAB.md)

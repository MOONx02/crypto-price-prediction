# Crypto Price Prediction

**Machine Learning and Data Mining** — ECPS 211 Winter 2026 Final Project

Predict **next-day** cryptocurrency price using rolling backtesting, baselines (last value, 7-day MA), a lag-feature Ridge model, and an LSTM. Includes time-series CV, ablation (volume, volatility), permutation importance, PDP/ICE, and error analysis.

---

## Quick start

### Option 1: Google Colab (no install)

1. Open **[notebooks/Crypto_Colab_EC_v1.ipynb](notebooks/Crypto_Colab_EC_v1.ipynb)** (recommended; canonical notebook for extra credit execution).
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

Then run `notebooks/Crypto_Colab_EC_v1.ipynb` (Jupyter or VS Code). Python 3.11 or 3.12 recommended (TensorFlow compatibility).

If you plan to run **Extension 3 (TFT)**, install optional dependencies:

```bash
pip install torch lightning pytorch-forecasting
```

---

## Deliverables

| Deliverable | Location |
|-------------|----------|
| **Report/Slides exports** | Archived under `archive/documents_presentations/` after cleanup |
| **Code** | This repo. **EC canonical notebook**: [notebooks/Crypto_Colab_EC_v1.ipynb](notebooks/Crypto_Colab_EC_v1.ipynb) (initialized from v9 baseline). Baseline reference remains [notebooks/Crypto_Colab_AllInOne_v9.ipynb](notebooks/Crypto_Colab_AllInOne_v9.ipynb). Legacy result exports were moved to `archive/legacy_artifacts/root_notebook_exports/`. |

---

## Repo structure

```
crypto-price-prediction/
├── README.md
├── CLEANUP_LOG.md
├── requirements.txt
├── notebooks/
│   ├── Crypto_Colab_EC_v1.ipynb         # canonical EC execution notebook
│   ├── Crypto_Colab_AllInOne_v9.ipynb   # baseline reference notebook
│   ├── README.md
│   └── archive/
├── archive/
│   ├── legacy_artifacts/
│   └── documents_presentations/
├── data/
└── src/
```

---

## Using the notebooks together

| Notebook | What you get |
|----------|--------------|
| [**AllInOne_Plus_TensorTrade.ipynb**](notebooks/AllInOne_Plus_TensorTrade.ipynb) | **Combined:** data, baselines, Lag+Ridge, LSTM, comparison table + TensorTrade backtest (P&L vs buy-and-hold vs cash) in one run. |
| [Crypto_Colab_AllInOne_v7.ipynb](notebooks/Crypto_Colab_AllInOne_v7.ipynb) | Full pipeline v7: returns-based targets, directional acc on returns, vol per-split, CV gap, LSTM simplif., long/short backtest. |
| [TensorTrade_Model_Backtest.ipynb](notebooks/TensorTrade_Model_Backtest.ipynb) | TensorTrade only (same data + Lag+Ridge); run with v6 for trading P&L. |

Use the **same `ASSET`** (e.g. `ETC-USD`). **AllInOne_Plus_TensorTrade** gives both prediction metrics and trading outcome in one notebook.

---

## What the EC notebook does


1. **Data** — Download daily OHLCV (yfinance), derive returns and 14-day volatility; 70/15/15 time split.
2. **Baselines** — Last value, 7-day moving average; MAE, RMSE, directional accuracy.
3. **Baseline lock + shared eval** — freeze v9 split/metric references and evaluate all variants through one function.
4. **XGBoost + indicators** — add RSI(14), MACD signal, Bollinger width; tune and compare against Ridge.
5. **Huber + Attention LSTM** — replace MSE with Huber loss and add timestep attention.
6. **TFT (optional)** — run constrained benchmark with `pytorch-forecasting` if dependencies are available.
7. **Final compare** — single table for Dir.Acc, MAE(return), Sharpe, P&L, trades.

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

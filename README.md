# Crypto Price Prediction

A time-series ML project for next-day crypto return prediction and strategy evaluation.  
The repository includes baseline models, feature engineering, deep-learning variants, and trading-oriented evaluation (Sharpe, P&L, trade count) with reproducible notebook workflows.

## Highlights

- End-to-end pipeline from OHLCV ingestion to model comparison and backtesting
- Baselines: last-value and moving-average predictors
- ML models: Ridge, XGBoost (+ technical indicators), LSTM, Huber+Attention LSTM, TFT benchmark
- Time-aware validation design: rolling windows and no-shuffle splits
- Analysis tooling: ablation studies, threshold tuning, cost sensitivity, and diagnostics

## Quick Start

### Colab (recommended)
1. Open `notebooks/final/Crypto_Prediction_EC_Assignment.ipynb`, or `notebooks/Crypto_Colab_EC_v1.ipynb`.
2. Run the install/setup cell.
3. Restart runtime when prompted.
4. Run all cells.

### Local
```bash
git clone https://github.com/MOONx02/crypto-price-prediction.git
cd crypto-price-prediction
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run `notebooks/final/Crypto_Prediction_EC_Assignment.ipynb` in Jupyter/VS Code.  
For TFT sections, install optional dependencies:

```bash
pip install torch lightning pytorch-forecasting
```

## Primary Artifacts

- **Final notebook:** `notebooks/final/Crypto_Prediction_EC_Assignment.ipynb`
- **Final report (readable):** `reports/EC_FINAL_REPORT.md`
- **Final report (submission formats):** `reports/EC_Final_Report.docx`, `reports/EC_Final_Report.pdf`
- **Experiment notes:** `reports/EC_FINDINGS_LOG.md`, `proposals/model_extension_proposal.md`

## Repository Layout

```text
crypto-price-prediction/
├── README.md
├── docs/
├── reports/
├── proposals/
├── notebooks/
│   └── final/
│       └── Crypto_Prediction_EC_Assignment.ipynb
├── scripts/
├── src/
├── data/
└── archive/
```

## Method Overview

1. Build return-based features from OHLCV data (lags, volume, volatility, technical indicators).
2. Train/evaluate baseline and advanced models on consistent time splits.
3. Tune decision thresholds with trade-count guards.
4. Compare models by directional accuracy **and** trading metrics.
5. Validate robustness under multiple transaction cost assumptions.

## Notes

- Results can shift between runs due to optimization/randomness and dependency/runtime differences.
- Current project conclusions are aligned to the latest `notebooks/final/Crypto_Prediction_EC_Assignment.ipynb` outputs.

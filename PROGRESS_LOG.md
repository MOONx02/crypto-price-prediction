# Progress Log

**Crypto Price Prediction** — ECPS 211 Winter 2026

Update this file as you complete tasks. See [TEAM_PLAN.md](TEAM_PLAN.md) for full phase breakdown and owners.

---

## What we did

### Setup (done)
- [x] Created Python 3.12 venv (TensorFlow doesn't support 3.14)
- [x] Installed dependencies from `requirements.txt` (including `pyarrow` for data cache)
- [x] Created `data/` directory for raw/processed series
- [x] Updated README with Python 3.11/3.12 setup note

### Phase 1: Data and baselines (done)
- [x] **1.1** Data source: yfinance, asset BTC-USD, date range from 2020-01-01
- [x] **1.2** Data pipeline: download in notebook, clean (ffill, dropna), save/load cache in `data/BTC_USD_daily.parquet`
- [x] **1.3** Time-based split: 70% train / 15% val / 15% test
- [x] **1.4** Baseline 1: last value (tomorrow = today) on test set
- [x] **1.5** Baseline 2: 7-day moving average on test set
- [x] **1.6** Metrics: `src.metrics.regression_metrics()` → MAE, RMSE, directional accuracy

**Deliverable:** Data loaded, two baselines run, three metrics on test set. ✅

---

## What we need to do

### Phase 2: Lag-feature model and rolling backtest (Week 2)
- [ ] **2.1** Feature design: lag features (e.g. price lags 1–7 or 1–30), optionally log returns; document in notebook
- [ ] **2.2** Preprocessing + Pipeline: ColumnTransformer (e.g. StandardScaler) + Pipeline with regression (e.g. Ridge or Gradient Boosting)
- [ ] **2.3** Rolling backtest: train on past only, predict next day, roll forward; no future leakage
- [ ] **2.4** Time-series CV: TimeSeriesSplit + RandomizedSearchCV; document param grid
- [ ] **2.5** Evaluation: rolling backtest metrics (MAE, RMSE, dir. acc.), residual plots, short error discussion

**Deliverable:** Lag-feature model with pipeline and rolling backtest; metrics and residual analysis.

---

### Phase 3: LSTM and comparison (Week 3)
- [ ] **3.1** LSTM research: how to feed sequences (e.g. last 7–30 days) for next-day prediction (Keras/TF)
- [ ] **3.2** LSTM implementation: small LSTM (1–2 layers), same train/val/test or rolling window
- [ ] **3.3** Fair comparison: same test period and metrics as baselines and lag model
- [ ] **3.4** Results table: Baselines vs Lag vs LSTM; short summary of which model wins on which metric

**Deliverable:** LSTM trained and evaluated; comparison table and short write-up.

---

### Phase 4: Features and ablation (Week 3)
- [ ] **4.1** Extra features: define 2–3 (volume, rolling volatility, simple indicator e.g. RSI or MA crossover); document formulas
- [ ] **4.2** Feature implementation: add to pipeline; rolling backtest uses only past data
- [ ] **4.3** Ablation study: (1) lags only, (2) lags + volume, (3) lags + volatility, (4) all; report MAE/RMSE/dir. acc.
- [ ] **4.4** Ablation summary: short conclusion for report (which features help)

**Deliverable:** Ablation results and "what helps" for the report.

---

### Phase 5: Interpretability, report, and presentation (End Week 3 / Week 4)
- [ ] **5.1** Permutation importance on best lag/tree model; plot and short interpretation
- [ ] **5.2** SHAP or PDP/ICE: interpret 1–2 important features
- [ ] **5.3** Error analysis: finalize residual plots and "where the model performs poorly"
- [ ] **5.4** Report: intro, data, methods, baselines, lag model, LSTM, ablation, interpretability, error analysis, conclusion
- [ ] **5.5** Slides: aligned with report; assign slides per person
- [ ] **5.6** Code cleanup: one notebook or script that reproduces all results; README with run instructions

**Deliverable:** Report, slides, reproducible code.

---

### Course requirements checklist
- [x] Two baselines (last value, moving average)
- [x] Time-based split only; no shuffle
- [x] MAE / RMSE + directional accuracy
- [ ] Baseline + at least two improved models (lag model, LSTM)
- [ ] ColumnTransformer + Pipeline
- [ ] RandomizedSearchCV (or Bayesian) with time-series CV
- [ ] Rolling backtest
- [ ] LSTM compared to baselines and lag model
- [ ] Ablation with extra/derived features
- [ ] Error analysis: residual plots + where model fails
- [ ] Interpretability: permutation importance + one of SHAP / PDP / ICE
- [ ] Report + slides + reproducible code

---

*Last updated: 2026-02-22*

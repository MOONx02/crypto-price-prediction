# Crypto Price Prediction with Rolling Backtesting and Baselines

**Machine Learning and Data Mining** — WINTER 2026

---

## Team Plan & Timeline

Goal: finish in **3 weeks**, use **Week 4 as buffer** before the due date.

---

## Timeline overview

| Phase | Focus | Target |
|-------|--------|--------|
| **1** | Data + baselines | End of Week 1 |
| **2** | Lag-feature model + pipeline + rolling backtest | End of Week 2 |
| **3** | LSTM + comparison | Mid Week 3 |
| **4** | Features + ablation | End of Week 3 |
| **5** | Interpretability + report + slides | End of Week 3 |
| **Buffer** | Final review, rehearsal, submission | Week 4 |

---

## Phase 1: Data and baselines (Week 1)

**Goal:** Data source and asset chosen, data downloaded and cleaned, time-based split, two baselines, metrics.

| Task | Description | Owner |
|------|-------------|--------|
| 1.1 Data source research | Compare sources (e.g. yfinance BTC-USD, CoinGecko). Pick one source + one asset. Document how to get daily OHLCV and date range. | Tae (completed) |
| 1.2 Data pipeline | Script/notebook: download history, handle missing values, clean DataFrame (date index, price, volume). | Tae (completed) |
| 1.3 Time-based split | Train/validation/test by time (e.g. 70% / 15% / 15%). Document split dates. | Tae (completed) |
| 1.4 Baseline 1 – Last value | Predict tomorrow = today’s price. Compute MAE, RMSE, directional accuracy on test set. | Tae (completed) |
| 1.5 Baseline 2 – Moving average | e.g. 7-day or 30-day MA. Same metrics. | Tae (completed) |
| 1.6 Metrics function | One function: (y_true, y_pred) → MAE, RMSE, directional accuracy. Reuse for all models. | Tae (completed) |

**Deliverable:** Data loaded, two baselines run, three metrics on test set.

---

## Phase 2: Lag-feature model and rolling backtest (Week 2)

**Goal:** ColumnTransformer + Pipeline, lag features, rolling backtest, hyperparameter search.

| Task | Description | Owner |
|------|-------------|--------|
| 2.1 Feature design | Lag features (e.g. price lags 1–7 or 1–30). Optionally log returns. Document in notebook. | Tae (completed) |
| 2.2 Preprocessing + Pipeline | ColumnTransformer (e.g. StandardScaler) + Pipeline with regression model (e.g. Ridge or Gradient Boosting). | Tae (completed) |
| 2.3 Rolling backtest | True rolling backtest: train on past only, predict next day, roll forward one day. No future leakage. | |
| 2.4 Time-series CV | TimeSeriesSplit + RandomizedSearchCV. Document param grid. | |
| 2.5 Evaluation | Rolling backtest for lag model; MAE, RMSE, directional accuracy; residual plots and short error discussion. | |

**Deliverable:** Lag-feature model with pipeline and rolling backtest; metrics and residual analysis.

---

## Phase 3: LSTM and comparison (Week 3)

**Goal:** LSTM implemented, same time discipline; compare to baselines and lag model.

| Task | Description | Owner |
|------|-------------|--------|
| 3.1 LSTM research | How to feed sequences (e.g. last 7–30 days) into LSTM for next-day prediction (Keras/TF or PyTorch). | Tae (completed) |
| 3.2 LSTM implementation | Small LSTM (1–2 layers), same train/val/test and rolling or expanding window. | Tae (completed) |
| 3.3 Fair comparison | Same test period and metrics (MAE, RMSE, directional accuracy) as baselines and lag model. | Tae (completed) |
| 3.4 Results table | Table: Baselines vs Lag vs LSTM. Short summary of which model wins on which metric. | Tae (completed) |

**Deliverable:** LSTM trained and evaluated; comparison table and short write-up.

---

## Phase 4: Features and ablation (Week 3)

**Goal:** Add volume, volatility, simple indicators; ablation to see what helps.

| Task | Description | Owner |
|------|-------------|--------|
| 4.1 Extra features research | Define 2–3 features: volume, rolling volatility, simple indicator (e.g. RSI or MA crossover). Document formulas. | Tae (completed) |
| 4.2 Feature implementation | Add to pipeline; rolling backtest uses only past data. | Tae (completed) |
| 4.3 Ablation study | Models: (1) lags only, (2) lags + volume, (3) lags + volatility, (4) all. Report MAE/RMSE/directional accuracy. | |
| 4.4 Ablation summary | Short conclusion: which features help; 1–2 sentences for report. | |

**Deliverable:** Ablation results and “what helps” for the report.

---

## Phase 5: Interpretability, report, and presentation (End of Week 3 / Week 4)

**Goal:** Interpretability, report draft, slides.

| Task | Description | Owner |
|------|-------------|--------|
| 5.1 Permutation importance | On best lag/tree model. Plot and short interpretation. | |
| 5.2 SHAP or PDP/ICE | One of: SHAP, partial dependence, or ICE. Interpret 1–2 important features. | |
| 5.3 Error analysis | Finalize residual plots and “where the model performs poorly.” | |
| 5.4 Report | Intro, data, methods, baselines, lag model, LSTM, ablation, interpretability, error analysis, conclusion. | |
| 5.5 Slides | Aligned with report; assign slides per person. | |
| 5.6 Code cleanup | One notebook or script that reproduces all results; README with run instructions. | |

**Deliverable:** Report, slides, reproducible code.

---

## Course requirements checklist

- [x] Baseline + at least two improved models (e.g. lag model, LSTM)
- [x] Time-based split only; no shuffle
- [x] ColumnTransformer + Pipeline
- [ ] RandomizedSearchCV (or Bayesian) with time-series CV
- [ ] Error analysis: residual plots + where model fails
- [ ] Interpretability: permutation importance + one of SHAP / PDP / ICE
- [x] Two baselines (last value, moving average)
- [ ] Rolling backtest
- [x] MAE or RMSE + directional accuracy
- [x] LSTM compared to baselines and lag model
- [x] Ablation with extra/derived features (volume, rolling volatility in AllInOne v3)
- [ ] Report + slides + reproducible code

---

**Tip:** Assign names to the Owner column and set concrete “by when” dates (e.g. “Phase 1 done by Feb 28”) so everyone stays on track.

# ECPS 211 Final Project — Requirements Checklist & Gap Analysis

**Project:** Modified Option 11 — **Crypto** Price Prediction with Rolling Backtesting and Baselines  
**Source:** ECPS211_Final_Projects_Winter_2026.pdf + `Crypto_Colab_AllInOne_v8.ipynb` + REPORT.md

---

## 1. Course-wide requirements (apply to every project)

| Requirement | Status | Where in v8 notebook |
|-------------|--------|----------------------|
| **Baseline + ≥2 improved models** | ✅ Met | Baselines: Last value, 7-day MA. Improved: Ridge (lag features), XGBoost, LSTM. |
| **Data split** | ✅ Met | Time-based only: 70% train, 15% val, 15% test (§2 split). |
| **Preprocessing + Pipeline** | ✅ Met | Ridge: `ColumnTransformer(StandardScaler)` + `Pipeline` (§5). Ablation (§10) also uses Pipeline. |
| **Hyperparameter search** | ✅ Met | Optuna (Bayesian-style) for Ridge & XGBoost (§5, §6). RandomizedSearchCV used for XGBoost classifier (§8c). PDF allows “RandomizedSearchCV or Bayesian optimization.” |
| **Error analysis (regression)** | ✅ Met | §12: residual histogram, predicted vs actual, residuals over time, \|residual\| vs volatility; text on where model performs poorly. |
| **Interpretability** | ✅ Met | §11: **permutation importance** (Ridge + XGBoost) + **PDP and ICE** (`PartialDependenceDisplay`, `kind="both"`) for Ridge. |
| **Imbalanced classification** | N/A | Regression project. |

---

## 2. Project Option 11 (Stock → Crypto) — core task

| Requirement | Status | Where in v8 notebook |
|-------------|--------|----------------------|
| **Predict next-day (or next-week) price — regression** | ✅ Met | Next-day **return** predicted; price = prev_price × (1 + pred_return). (§4–§7, metrics) |
| **≥2 baselines** | ✅ Met | Last value (§3), 7-day MA (§3). |
| **Model with lag features** | ✅ Met | Ridge with 30 return lags + extra features (§5). |
| **True rolling backtest (rolling window evaluation)** | ✅ Met | §9b: **Expanding-window evaluation** — multiple test windows, retrain Ridge & XGBoost on expanding train, report mean ± std of MAE_ret and Dir.Acc. §13: Long/short backtest (P&L with costs). |
| **Report MAE or RMSE + directional accuracy** | ✅ Met | §9 comparison table: MAE (price), RMSE (price), Dir.Acc, MAE (return). |
| **LSTM and compare to baselines + lag-feature model** | ✅ Met | §7 LSTM; §9 table compares Last value, 7d MA, Ridge, XGBoost, LSTM, ensembles. |
| **External/derived features + ablation** | ✅ Met | Volume, volatility, RSI, MACD, BB, ATR, OBV, multi-horizon returns, calendar, BTC cross-asset (§2). §10: ablation by feature groups (6 steps). |

---

## 3. What you still need to do

### 3.1 Update the written report (REPORT.md) — **high priority**

The current **REPORT.md** describes the **v7** pipeline, not v8. It should be updated so the report matches the notebook and the syllabus.

- **Update to reflect v8:**
  - **Target:** Next-day **return** (then price); not “price lags” — use **return lags** + stationarity.
  - **Features:** ~55 features (30 return lags + 25 extra: RSI, MACD, BB, ATR, OBV, multi-horizon returns, calendar, BTC lags + rotation).
  - **Models:** Ridge (Optuna), **XGBoost**, LSTM (64→32, dropout, early stopping, ReduceLROnPlateau), **weighted ensemble**, **stacking meta-learner** (§8, §8b), and optional XGBoost classifier (§8c).
  - **Methodology:** **Expanding-window evaluation** (§9b): walk-forward, multiple test windows, mean ± std of Dir.Acc and MAE_ret.
  - **Hyperparameter:** Optuna for Ridge and XGBoost (not only RandomizedSearchCV).
  - **Ablation:** 6 feature groups (§10), not 4.
  - **Interpretability:** Permutation importance for Ridge and XGBoost; PDP/ICE for Ridge.
  - **Error analysis:** E.g. XGBoost residuals (§12).
  - **Reproducibility:** Point to `notebooks/Crypto_Colab_AllInOne_v8.ipynb` (not v7).

- **Suggestion:** Replace or rewrite sections 2–6 of REPORT.md so they align with v8 (data, methods, results, interpretability, error analysis, conclusion). Keep the same overall structure (Introduction, Data, Methods, Results, Conclusion).

### 3.2 Align slides with v8 and requirements

- The file **Crypto_Price_Prediction_Slides.pptx** could not be read as text here. Please check manually that the slides:
  - Describe **v8** (return-based targets, XGBoost, ensemble, expanding-window, 6-group ablation).
  - Explicitly mention: **two baselines**, **lag-feature model (Ridge)**, **LSTM**, **rolling/expanding-window evaluation** (§9b), **MAE/RMSE + directional accuracy**, **external/derived features + ablation**, **interpretability** (permutation + PDP/ICE), **error analysis** (residuals + where model fails).

### 3.3 Clarify “rolling backtest” in report/slides (optional but recommended)

- The syllabus asks for a “true rolling backtest (rolling window evaluation).”
- Your **§9b** implements **expanding-window** walk-forward (train set grows, multiple test windows). That is a standard and acceptable form of rolling/walk-forward evaluation for time series.
- **Recommendation:** In REPORT.md and in the slides, add one short sentence, e.g.:  
  *“We implement rolling window evaluation via an expanding-window walk-forward scheme (Section 9b): we retrain on all past data before each test window and report mean ± std of MAE and directional accuracy across windows.”*  
  No code change needed if the instructor accepts expanding-window as “rolling window evaluation.”

### 3.4 Deliverables checklist

- [ ] **Written report:** Update REPORT.md to v8 (see 3.1).
- [ ] **Presentation slides:** Ensure Crypto_Price_Prediction_Slides.pptx matches v8 and all requirements (see 3.2).
- [ ] **Python code:** Confirm that “run all” on `notebooks/Crypto_Colab_AllInOne_v8.ipynb` reproduces the results cited in the report and slides (asset set in config, e.g. `ASSET = "ETC-USD"`).

---

## 4. Summary

- **Notebook v8** already satisfies the course-wide requirements and Option 11 (crypto version) requirements: baselines, lag-feature model, LSTM, rolling/expanding-window evaluation, MAE/RMSE + directional accuracy, extra features, ablation, interpretability (permutation + PDP/ICE), error analysis, Pipeline/ColumnTransformer, and hyperparameter search (Optuna + RandomizedSearchCV for classifier).
- The main remaining work is **updating REPORT.md** to describe v8 instead of v7, and **verifying that the slides** describe v8 and explicitly hit each requirement. Optionally, add one sentence in the report and slides stating that “rolling window evaluation” is implemented as expanding-window walk-forward in Section 9b.

# Progress Log

**Crypto Price Prediction** — ECPS 211 Winter 2026

Update this file as you complete tasks. See [TEAM_PLAN.md](TEAM_PLAN.md) for full phase breakdown and owners.

**Log discipline:** When you (or the AI) make significant changes—new features, refactors, Colab runs, model fixes—add a short entry under **What we did** and update **Last updated** at the bottom. That way the log stays current even if you don’t remember to ask.

---

## What we did

### Setup (done)
- [x] Created Python 3.12 venv (TensorFlow doesn't support 3.14)
- [x] Installed dependencies from `requirements.txt` (including `pyarrow` for data cache)
- [x] Created `data/` directory for raw/processed series
- [x] Updated README with Python 3.11/3.12 setup note

### Phase 1: Data and baselines (done)
- [x] **1.1** Data source: yfinance, asset BTC-USD, date range from 2017-01-01
- [x] **1.2** Data pipeline: download in notebook, clean (ffill, dropna), save/load cache in `data/BTC_USD_daily.parquet`
- [x] **1.3** Time-based split: 70% train / 15% val / 15% test
- [x] **1.4** Baseline 1: last value (tomorrow = today) on test set
- [x] **1.5** Baseline 2: 7-day moving average on test set
- [x] **1.6** Metrics: `src.metrics.regression_metrics()` → MAE, RMSE, directional accuracy

**Deliverable:** Data loaded, two baselines run, three metrics on test set. 

### Colab run and LSTM fix (2026-02-22)
- Ran full pipeline in Colab (Copy_of_Crypto_Colab_AllInOne). **Findings:** Last value was best (MAE ~1585, RMSE ~2210). Lag+Ridge and 7-day MA were worse; directional accuracy ~49% (random). LSTM was broken: MAE/RMSE ~97k (predicting raw price without scaling).
- **Actions:** (1) Archived original notebooks `01_data_and_baselines`, `02_lag_model`, `03_lstm` to `notebooks/archive/`. (2) Fixed `Crypto_Colab_AllInOne.ipynb`: LSTM now predicts **returns** (not raw price), input sequences are **StandardScaler**-scaled, then predicted return is converted back to price for the comparison table. Ready to re-run on Colab for a fair LSTM vs baselines comparison.
- **Colab re-run (fixed notebook):** Uploaded fixed AllInOne from computer to Colab. **Results:** LSTM MAE 1597.58, RMSE 2202.31, Dir.Acc 0.498 — now in same range as last value (MAE 1585.59, RMSE 2210.14). LSTM RMSE slightly better than last value; directional accuracy still ~50% (random).

### AllInOne notebook: lag model + LSTM (2026-02-22)
- **Crypto_Colab_AllInOne.ipynb** now includes: (1) Data + baselines (last value, 7-day MA). (2) **Lag model:** 30 price lags, ColumnTransformer(StandardScaler) + Pipeline(Ridge), same 70/15/15 split; metrics on test set. (3) **LSTM:** predicts returns (scaled sequences), convert to price; same test period and metrics. (4) **Comparison table:** Last value, 7-day MA, Lag+Ridge, LSTM with MAE/RMSE/dir. acc. Derived columns (returns, volatility_14, log_volume) are in the dataframe for future ablation; no rolling backtest or TimeSeriesSplit/RandomizedSearchCV in AllInOne yet (those exist in `notebooks/archive/02_lag_model.ipynb`).

### Volume and rolling volatility (2026-02-22)
- **Data:** In AllInOne, after load: added `ret` (day-over-day return), `volatility_14` (14-day rolling std of returns), `log_volume` (log1p(volume)); volume set to 0 if missing.
- **Lag model:** Ridge pipeline now includes two extra features per sample: `log_volume` and `volatility_14` at the last-lag time index. Printed as "Lag+Ridge (+ volume, volatility_14)".
- **LSTM:** Sequences are 3-channel: (return, log_volume, volatility_14) per timestep; input shape `(SEQ_LEN, 3)`; scaling on all three. Printed as "LSTM (+ volume, volatility_14, predict returns → price)".
- Re-run on Colab to compare metrics (ablation: with vs without these features).

### AllInOne versioning (2026-02-22)
- **Three versions:** **v1** (original, LSTM on raw price — broken), **v2** (fix: LSTM returns + scaling), **v3** (improvement: + volume, volatility). Working notebook is `notebooks/Crypto_Colab_AllInOne_v3.ipynb`. v1 and v2 live in `notebooks/archive/`; when you start v4, move v3 to archive and create v4.
- **Docs:** `notebooks/README.md` has the version history table and archive contents.

### AllInOne v4 (ETH), v5 (XRP), v6 (ETC) (2026-02-22)
- **v4_ETH:** `Crypto_Colab_AllInOne_v4_ETH.ipynb` — same pipeline as v3, data = ETH-USD; cache `ETH_USD_daily.parquet`. Run on Colab to compare MAE/RMSE/Dir.Acc to BTC.
- **v5_XRP:** `Crypto_Colab_AllInOne_v5_XRP.ipynb` — same pipeline, data = XRP-USD (Ripple); cache `XRP_USD_daily.parquet`. Run to compare to BTC/ETH.
- **v6_ETC:** `Crypto_Colab_AllInOne_v6_ETC.ipynb` — same pipeline, data = ETC-USD (Ethereum Classic); cache `ETC_USD_daily.parquet`. Run to compare to BTC/ETH/XRP.

### Colab run — ETC (v6) results (2026-02-22)
- Ran v6_ETC on Colab. **Results:** **7-day MA Dir.Acc 55.3%** (best directional so far); Lag+Ridge 53.7%; LSTM 46.0%. On ETC the simple 7-day MA beats LSTM on direction; LSTM did not help. Last value best MAE/RMSE (0.587 / 0.900). ETC shows more predictable structure for simple models with same pipeline.

### Colab run — ETH (v4) results (2026-02-22)
- Ran v4_ETH on Colab. **Results:** LSTM MAE 86.02, RMSE 121.52, **Dir.Acc 51.5%**; Lag+Ridge **Dir.Acc 53.4%** (best directional so far); 7-day MA 51.0%. Last value best on MAE/RMSE (82.53 / 118.77). **Vs BTC (v3):** ETH shows slightly better direction (Lag+Ridge 53.4% vs ~49.7% on BTC; LSTM 51.5% vs ~51% on BTC)—same pipeline, ETH a bit more predictable for direction.

### Colab run — XRP (v5) results (2026-02-22)
- Ran v5_XRP on Colab. **Results:** LSTM MAE 0.089, RMSE 0.128, **Dir.Acc 50.0%** (no edge); 7-day MA **52.1%**, Lag+Ridge **51.5%**. On XRP the LSTM did not add directional value; simpler models (7-day MA, Lag+Ridge) slightly above random. Last value best on MAE/RMSE (XRP price ~$0.5–2 so errors in dollars are small).
- **Cross-asset:** BTC ~51% LSTM; ETH best (Lag 53.4%, LSTM 51.5%); XRP LSTM 50%. **Moving focus to ETH** for report/next steps (best directional results with same pipeline).

### Colab run with volume + volatility (AllInOne copy)
- Ran full pipeline (data, baselines, Lag+Ridge + volume/volatility, LSTM + volume/volatility) on Colab. **Results:** LSTM MAE 1599.64, RMSE 2208.82, **Dir.Acc 0.510** (above random). Lag+Ridge Dir.Acc 0.497. Volume and volatility features give a small directional lift; MAE/RMSE in line with previous runs.

### Cleanup: names and duplicates (2026-02-22)
- **Removed:** `notebooks/Crypto_Colab_AllInOne copy.ipynb`; from 211 root: `Crypto_Colab_AllInOne_copy.ipynb`, `Crypto_Colab_AllInOne (1).ipynb`, `Crypto_Colab_AllInOne (2).ipynb`.
- **Renamed in archive:** `Copy_of_Crypto_Colab_AllInOne.ipynb` → `Crypto_Colab_AllInOne_legacy.ipynb`.
- **Saved in archive:** Colab run (51% Dir.Acc) as `archive/Crypto_Colab_AllInOne_v1_colab_run.ipynb`. Single working notebook: `notebooks/Crypto_Colab_AllInOne_v1.ipynb`.

### Rolling backtest + TimeSeriesSplit + residuals (2026-02-25)
- **AllInOne v4** (main BTC): **3b** Rolling backtest for Lag+Ridge (train on past only, predict next day; uses lags + log_volume + volatility_14). **3c** TimeSeriesSplit(5) + RandomizedSearchCV over Ridge alpha (logspace -2..2), scoring neg MAE. **3d** Best model on test set, residual histogram, predicted vs actual scatter, short error discussion (tails in volatile regimes). v3 moved to `notebooks/archive/`; working notebook is now `Crypto_Colab_AllInOne_v4.ipynb`.

### Asset as variation, not version (2026-02-25)
- **One notebook, one version.** v4 has config cell `ASSET = "BTC-USD"` (or ETH-USD, XRP-USD, ETC-USD). Cache and download use `ASSET`; no separate file per coin. v4_ETH, v5_XRP, v6_ETC-test moved to `archive/`. README: version = pipeline only; asset = variation.

### Colab run — BTC (v4) (2026-02-25)
- Ran v4 on Colab with **BTC-USD**. **Results:** Last value MAE 1594, RMSE 2220 (best on error); 7-day MA 2677 / 3560, Dir.Acc 49.4%; Lag+Ridge 2332 / 3067, Dir.Acc 49.6%; **LSTM 1710 / 2295, Dir.Acc 50.5%** (only model above 50% directional). Conclusion: last value best MAE/RMSE; LSTM slight directional edge on BTC.

### Phase 4 ablation → v5 (2026-02-25)
- **v5 created:** Phase 4 ablation (Section 4) added; notebook promoted to **v5**. `Crypto_Colab_AllInOne_v5.ipynb` is now the current notebook. v4 moved to `notebooks/archive/`. Ablation compares Lag+Ridge: (1) lags only, (2) lags + volume, (3) lags + volatility, (4) all; reports MAE, RMSE, Dir.Acc and short summary for report.

---

## What we need to do

### Phase 2: Lag-feature model and rolling backtest (Week 2)
- [x] **2.1** Feature design: lag features (e.g. price lags 1–7 or 1–30), optionally log returns; document in notebook
- [x] **2.2** Preprocessing + Pipeline: ColumnTransformer (e.g. StandardScaler) + Pipeline with regression (e.g. Ridge or Gradient Boosting)
- [x] **2.3** Rolling backtest: train on past only, predict next day, roll forward; no future leakage
- [x] **2.4** Time-series CV: TimeSeriesSplit + RandomizedSearchCV; document param grid
- [x] **2.5** Evaluation: rolling backtest metrics (MAE, RMSE, dir. acc.), residual plots, short error discussion

**Deliverable:** Lag-feature model with pipeline and rolling backtest; metrics and residual analysis. ✅ Integrated in `Crypto_Colab_AllInOne_v4.ipynb` (sections 3b–3d).

---

### Phase 3: LSTM and comparison (Week 3)
- [x] **3.1** LSTM research: how to feed sequences (e.g. last 7–30 days) for next-day prediction (Keras/TF)
- [x] **3.2** LSTM implementation: small LSTM (1–2 layers), same train/val/test or rolling window
- [x] **3.3** Fair comparison: same test period and metrics as baselines and lag model
- [x] **3.4** Results table: Baselines vs Lag vs LSTM; short summary of which model wins on which metric

**Deliverable:** LSTM trained and evaluated; comparison table and short write-up. ✅ (In AllInOne.)

---

### Phase 4: Features and ablation (Week 3)
- [x] **4.1** Extra features: define 2–3 (volume, rolling volatility, simple indicator e.g. RSI or MA crossover); document formulas
- [x] **4.2** Feature implementation: add to pipeline; rolling backtest uses only past data
- [x] **4.3** Ablation study: (1) lags only, (2) lags + volume, (3) lags + volatility, (4) all; report MAE/RMSE/dir. acc.
- [ ] **4.4** Ablation summary: short conclusion for report (which features help) — fill in after Colab run

**Deliverable:** Ablation results and "what helps" for the report. ✅ Section 4 in v4 runs ablation; summarize in report after viewing results.

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
- [x] Baseline + at least two improved models (lag model, LSTM)
- [x] ColumnTransformer + Pipeline
- [x] RandomizedSearchCV (or Bayesian) with time-series CV
- [x] Rolling backtest
- [x] LSTM compared to baselines and lag model
- [x] Ablation with extra/derived features (volume, volatility in v3)
- [x] Error analysis: residual plots + where model fails
- [ ] Interpretability: permutation importance + one of SHAP / PDP / ICE
- [ ] Report + slides + reproducible code

---

### v5 fixes (2026-02-25)
- **Comparison table:** Lag+Ridge row now uses **best-from-CV** (`metrics_best` from Section 3d) instead of fixed-alpha `m_lag`, so table matches residual evaluation. Label: "Lag+Ridge (best CV)".
- **Duplicate 7-day MA removed:** Inline "7-day MA forecast from end of series" cell (after Section 2) removed; Section 7 is the single place for future 7-day MA.
- **Last-value Dir.Acc:** Comment added in baselines cell: "Last value predicts no change, so Dir.Acc is not meaningful (often 0)."

---

*Last updated: 2026-02-25 (v5 fixes: best CV in table, duplicate MA removed, last-value comment)*

# Crypto Price Prediction: Report

**Machine Learning and Data Mining** — ECPS 211 Winter 2026

---

## 1. Introduction

We predict **next-day cryptocurrency price** (regression) using a time-based pipeline: two baselines, a lag-feature Ridge model, and an LSTM. The project uses a single configurable asset (e.g. ETC-USD, BTC-USD) with **time-based splits only**, **rolling backtesting** (no future leakage), **time-series cross-validation** for hyperparameter tuning, **ablation** on extra features (volume, volatility), **interpretability** (permutation importance, PDP/ICE), and **error analysis** (residuals and where the model fails). All experiments are reproducible via the notebook `notebooks/Crypto_Colab_AllInOne_v6.ipynb`; the asset is set in a config cell (e.g. `ASSET = "ETC-USD"`).

**Main findings:** The naive **last-value** baseline is best on MAE/RMSE across assets. Directional accuracy varies by asset; on ETC-USD the **7-day moving average** and **Lag+Ridge** beat the **LSTM**. Adding volume and volatility improves direction at a small cost to point-forecast error. The best Lag+Ridge model performs worst during **high-volatility** periods and on **large price moves**.

---

## 2. Data

- **Source:** Yahoo Finance via `yfinance`. Daily OHLCV; we use adjusted close and volume.
- **Asset:** Configurable (e.g. BTC-USD, ETH-USD, XRP-USD, ETC-USD). Results below use **ETC-USD** (Ethereum Classic) unless noted.
- **Date range:** From 2017-01-01 to present; data are downloaded in the notebook and cached as `data/<ASSET>_daily.parquet` (e.g. `ETC_USD_daily.parquet`).
- **Processing:** Forward-fill, dropna; datetime index (timezone-naive). We derive:
  - **Returns:** \(r_t = (P_t - P_{t-1}) / (P_{t-1} + \epsilon)\)
  - **Rolling volatility:** 14-day standard deviation of returns (past only), `volatility_14`
  - **Log volume:** \(\log(1 + \text{volume})\), `log_volume`
- **Split:** **Time-based only**, no shuffle: **70% train**, **15% validation**, **15% test**. Same split is used for baselines, Lag+Ridge, LSTM, ablation, and interpretability.

Example (ETC-USD): 3031 rows; train 2121, val 455, test 455.

---

## 3. Methods

### 3.1 Metrics

A single function `regression_metrics(y_true, y_pred)` returns:

- **MAE:** mean absolute error  
- **RMSE:** root mean squared error  
- **Directional accuracy:** fraction of test steps where the sign of (next price − current price) matches the sign of (predicted next − current). Last-value baseline predicts no change, so its directional accuracy is not meaningful (often 0).

### 3.2 Baselines

1. **Last value:** \(\hat{P}_{t+1} = P_t\).  
2. **7-day moving average:** \(\hat{P}_{t+1} = \frac{1}{7}\sum_{i=0}^{6} P_{t-i}\).

Both are evaluated on the same test period; MAE and RMSE are computed on next-day price.

### 3.3 Lag-feature model (Ridge)

- **Features:** 30 price lags (lag 1 = most recent, …, lag 30), plus **log_volume** and **volatility_14** at the last-lag time index (32 features total).
- **Pipeline:** `ColumnTransformer(StandardScaler()` on all columns) → **Ridge** regression. No shuffle; fit on train, evaluate on test.
- **Hyperparameter search:** **TimeSeriesSplit** (5 splits) + **RandomizedSearchCV** over Ridge `alpha` in `np.logspace(-2, 2, 20)`, 10 iterations, scoring **neg_mean_absolute_error**. Best model (e.g. `alpha=0.01`) is used for test evaluation, comparison table, residual plots, permutation importance, and PDP/ICE.
- **Rolling backtest:** For each day, train on past data only (min 500 + 31 points), predict next-day price with the same feature set; no future leakage. Reported separately from the fixed-split test metrics.

### 3.4 LSTM

- **Target:** Next-day **return** (not raw price); predicted return is converted to price for comparison: \(\hat{P}_{t+1} = P_t (1 + \hat{r}_t)\).
- **Inputs:** Sequences of length 30; each step has (return, log_volume, volatility_14). StandardScaler fit on train and applied to all three channels.
- **Architecture:** 2 LSTM layers (32 then 16 units), then Dense(1). Trained with MSE, batch size 32, 30 epochs; validation on the same time-based val set.
- **Evaluation:** Same test period and metrics (MAE, RMSE, directional accuracy) as baselines and Lag+Ridge, on **prices** derived from predicted returns.

### 3.5 Ablation (Lag+Ridge only)

Four feature sets, same train/test split and pipeline (Ridge alpha fixed at 1.0 for ablation):

1. **Lags only** (30 features)  
2. **Lags + volume** (31)  
3. **Lags + volatility** (31)  
4. **Lags + volume + volatility** (32)

We report MAE, RMSE, and directional accuracy for each.

### 3.6 Interpretability

- **Permutation importance:** On the **best Lag+Ridge** (from CV), on the test set: shuffle each feature 10 times, measure increase in MAE; plot and interpret top features.
- **PDP/ICE:** Partial dependence and individual conditional expectation (ICE) for 1–2 important features (e.g. lag_1, log_volume) using the best Lag+Ridge model.

### 3.7 Error analysis

Residual plots for the best Lag+Ridge on test: (1) histogram of residuals, (2) predicted vs actual, (3) residuals over time, (4) |residual| vs volatility_14. Short discussion of **where the model performs poorly**.

---

## 4. Results

### 4.1 Baselines (ETC-USD, test set)

| Model       | MAE    | RMSE   | Dir.Acc |
|------------|--------|--------|---------|
| Last value | **0.575** | **0.871** | 0%*  |
| 7-day MA   | 0.894 | 1.305 | **55.3%** |

\*Last value predicts no change; directional accuracy is not meaningful.

Last value is best on MAE and RMSE; 7-day MA gives the best directional accuracy among baselines.

### 4.2 Lag model and rolling backtest

- **Lag+Ridge (fixed alpha=1.0, all features), test:** MAE 0.895, RMSE 1.177, Dir.Acc 53.4%.  
- **Best Lag+Ridge (from CV, alpha=0.01), test:** MAE 0.895, RMSE 1.178, Dir.Acc **53.2%**.  
- **Rolling backtest (Lag+Ridge):** MAE 1.38, RMSE 3.49, Dir.Acc 52.7%. Rolling backtest is stricter (retrain each day) and shows higher error.

### 4.3 LSTM (ETC-USD, test set)

| Metric | Value   |
|--------|---------|
| MAE    | 0.609   |
| RMSE   | 0.905   |
| Dir.Acc| **45.6%** |

LSTM is between last value and 7-day MA on MAE/RMSE but **below 50%** on directional accuracy on this run—worse than random for up/down prediction.

### 4.4 Model comparison (ETC-USD, test set)

| Model              | MAE    | RMSE   | Dir.Acc |
|--------------------|--------|--------|---------|
| Last value         | **0.575** | **0.871** | 0%   |
| 7-day MA           | 0.894 | 1.305 | **55.3%** |
| Lag+Ridge (best CV)| 0.895 | 1.178 | 53.2%  |
| LSTM               | 0.609 | 0.905 | 45.6%  |

- **Best MAE/RMSE:** Last value.  
- **Best directional accuracy:** 7-day MA (55.3%), then Lag+Ridge (53.2%). LSTM is worst on direction for this asset.

### 4.5 Ablation (ETC-USD, test set)

| Features                    | MAE    | RMSE   | Dir.Acc |
|----------------------------|--------|--------|---------|
| Lags only                  | **0.806** | **1.098** | 52.0% |
| Lags + volume              | 0.892 | 1.172 | **53.9%** |
| Lags + volatility          | 0.815 | 1.109 | 52.5%  |
| Lags + volume + volatility | 0.895 | 1.177 | 53.4%  |

- **MAE/RMSE:** Lags-only is best; adding volume or volatility increases point-forecast error slightly.  
- **Directional accuracy:** Adding volume gives the largest gain (52.0% → 53.9%); volatility adds a smaller improvement. So extra features **improve direction** at a **small cost to magnitude**.

### 4.6 Interpretability

- **Permutation importance (best Lag+Ridge, test):** In the reported ETC-USD run, the top three features by permutation importance were **log_volume**, **volatility_14**, and **lag_15**. Shuffling these increased MAE the most, so they contribute to point forecasts; the important lag horizon was mid (lag_15) in this run. (Interpretation in the notebook is data-driven and can change by run/asset.)
- **PDP/ICE:** Partial dependence for **lag_1** is roughly linear (higher lag_1 → higher prediction; Ridge is linear in features). **log_volume** has a flatter PDP. ICE curves for lag_1 show a similar slope across samples (effect is fairly homogeneous).

### 4.7 Error analysis

- **Residuals:** Centered near zero with **long tails**; large errors in both directions.  
- **Over time:** Errors **cluster in periods** (volatility regimes), not uniformly.  
- **|Residual| vs volatility_14:** **Larger errors** tend to occur when volatility is high.  
- **Conclusion:** The model performs worst during **high-volatility periods** and on **large price moves**; it behaves like a smoothed extrapolation of recent lags and under/overpredicts sharp moves.

---

## 5. Cross-asset summary (from project runs)

- **BTC-USD:** Last value best MAE/RMSE; LSTM had a slight directional edge (50.5%); Lag+Ridge and 7-day MA ~49–50%.  
- **ETH-USD:** Lag+Ridge best direction (53.4%); LSTM 51.5%; last value best MAE/RMSE.  
- **XRP-USD:** 7-day MA and Lag+Ridge ~51–52% direction; LSTM 50%.  
- **ETC-USD:** 7-day MA and Lag+Ridge best direction (55.3%, 53.2%); LSTM below 50%.  

So directional predictability and which model wins vary by asset; last value remains best on MAE/RMSE; LSTM does not consistently beat simpler models on direction.

---

## 6. Conclusion

We implemented a full pipeline for next-day crypto price prediction with **time-based splits**, **rolling backtest**, **TimeSeriesSplit + RandomizedSearchCV**, **ablation**, **permutation importance**, **PDP/ICE**, and **error analysis**.  

- **Baselines:** Last value is best on MAE/RMSE; 7-day MA can achieve the best directional accuracy (e.g. 55.3% on ETC-USD).  
- **Lag+Ridge:** Competitive on direction (e.g. 53.2%); lags-only is best for MAE/RMSE; adding volume helps direction, volatility adds a smaller gain.  
- **LSTM:** Similar or worse than simpler models on direction (e.g. 45.6% on ETC-USD); does not dominate.  
- **Interpretability:** Permutation importance and PDP/ICE show which features (and lag horizon) matter; results can differ by run/asset.  
- **Error analysis:** The best Lag+Ridge fails most in **high-volatility** regimes and on **large moves**.  

Reproducibility: one notebook, `notebooks/Crypto_Colab_AllInOne_v6.ipynb`; set `ASSET` and run all cells. See `README.md` and `notebooks/README.md` for setup and version history.

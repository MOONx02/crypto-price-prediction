# Model Improvement Assessment

**Crypto Price Prediction**
**Date:** March 2, 2026

---

## Current Performance Summary

| Model | MAE | RMSE | Dir.Acc | Verdict |
|-------|-----|------|---------|---------|
| Last value | **0.575** | **0.871** | 0%* | Best point forecast |
| 7-day MA | 0.894 | 1.305 | **55.3%** | Best direction |
| Lag+Ridge (best CV) | 0.895 | 1.178 | 53.2% | Competitive direction |
| LSTM | 0.609 | 0.905 | 45.6% | Below random on direction |

*ETC-USD test set. The naive last-value baseline dominates on MAE/RMSE, and the LSTM fails to beat 50% directional accuracy on ETC.*

**Core problem:** Your ML models do not consistently beat simple baselines. This is actually common in financial time series (the efficient market hypothesis in action), but there are concrete improvements that can narrow the gap and potentially push directional accuracy above 55%.

---

## 1. LSTM Architecture Issues (High Impact)

### 1a. Architecture is undersized and undertrained

Your current LSTM: 2 layers (32 → 16 units), 30 epochs, batch 32. This is quite small.

**Recommendations:**

∙ Increase hidden size to 64 → 32 (or 128 → 64) with dropout (0.2–0.3) between layers to prevent overfitting while giving the model more capacity.

∙ Add **Bidirectional LSTM** or switch to **GRU** (fewer parameters, often trains better on small datasets). GRU is worth trying since your dataset is only ~3000 rows.

∙ Use **learning rate scheduling** (ReduceLROnPlateau) instead of a fixed learning rate. Start at 1e-3, reduce by 0.5 when val loss plateaus for 5 epochs.

∙ Train for more epochs (100–200) with **early stopping** (patience=15, restore_best_weights=True). 30 epochs may not be enough for convergence.

∙ Try **batch size 64 or 128** — smaller batches (32) can cause noisy gradients on financial data.

### 1b. Loss function mismatch

You train the LSTM with **MSE loss** but evaluate with **directional accuracy**. These objectives are misaligned.

**Recommendations:**

∙ Add a **custom directional loss** that penalizes wrong-direction predictions more heavily. For example, a weighted loss: `loss = MSE + lambda * direction_penalty` where direction_penalty is 1 when the predicted direction is wrong.

∙ Alternatively, frame the problem as **classification** (up/down) for a separate directional model, using binary cross-entropy. You can ensemble it with your regression model.

### 1c. Sequence length is fixed at 30

You use a fixed 30-step lookback. This may not be optimal for all assets.

**Recommendations:**

∙ Treat `SEQ_LEN` as a hyperparameter. Try 7, 14, 30, 60, and 90 — shorter windows capture recent momentum, longer windows capture regime context.

∙ Use the validation set to pick the best sequence length.

**Confidence: 0.85** — These are well-established deep learning best practices that consistently help.

---

## 2. Feature Engineering Gaps (High Impact)

### 2a. Missing technical indicators

You only use returns, log_volume, and volatility_14. Financial practitioners rely on many more signals.

**Add these features (all computed from past data only, no leakage):**

∙ **RSI (14-day):** Relative Strength Index — captures overbought/oversold conditions. Values above 70 or below 30 are historically informative for mean-reversion.

∙ **MACD:** Moving Average Convergence Divergence (12/26/9 EMA). The MACD line, signal line, and histogram capture momentum shifts.

∙ **Bollinger Band position:** Where the current price sits relative to the 20-day Bollinger Bands (as a percentile). Captures volatility-adjusted price extremes.

∙ **ATR (14-day):** Average True Range — a volatility measure that differs from your rolling std and may capture intraday range information.

∙ **On-Balance Volume (OBV) change:** Rate of change in OBV over 7 and 14 days — captures volume momentum that simple log_volume misses.

∙ **Return momentum at multiple horizons:** 3-day, 7-day, 14-day, 30-day cumulative returns. Your model only sees 1-day return at each lag; multi-horizon returns make trend strength explicit.

### 2b. Calendar and time features

∙ **Day of week:** Crypto has known weekend effects (lower volume, different volatility).

∙ **Month:** Seasonal patterns exist in crypto (e.g., "Sell in May").

∙ Encode these as sine/cosine cyclical features, not one-hot.

### 2c. Cross-asset features

∙ **BTC return as a feature for altcoins:** BTC drives the market. When predicting ETC, include BTC's lagged returns (lag 1–3) as features. This is one of the strongest signals for altcoin direction.

∙ **BTC dominance ratio change:** Captures rotation between BTC and alts.

**Confidence: 0.80** — Technical indicators are standard; their marginal value varies by asset and time period. Cross-asset features (especially BTC returns for altcoins) tend to be particularly strong.

---

## 3. Model Selection Improvements (High Impact)

### 3a. Try gradient boosting (XGBoost / LightGBM)

Ridge regression is linear. Financial data often has nonlinear relationships (e.g., volatility regimes, momentum breakouts).

**Recommendations:**

∙ Replace or supplement Ridge with **XGBoost** or **LightGBM**. These handle nonlinear interactions, feature selection, and missing values natively.

∙ Use the same `TimeSeriesSplit + RandomizedSearchCV` framework you already have. Key hyperparameters to tune: `max_depth` (3–8), `n_estimators` (100–500), `learning_rate` (0.01–0.1), `subsample` (0.7–0.9), `colsample_bytree` (0.7–1.0).

∙ XGBoost typically outperforms Ridge on tabular financial data by 5–15% on directional accuracy in similar setups.

### 3b. Ensemble your models

∙ **Simple average ensemble:** Average the predictions of Ridge, XGBoost, and LSTM. Ensembles often beat individual models by 1–3% directional accuracy because they smooth out individual model errors.

∙ **Stacking:** Use Ridge/XGBoost/LSTM predictions as features for a meta-learner (logistic regression on direction). Train the meta-learner on validation predictions only.

∙ **Weighted ensemble:** Weight models by their validation directional accuracy. Models with >50% val accuracy get higher weight.

### 3c. Direct classification approach

∙ Train a **separate classifier** (Random Forest, XGBoost classifier) to predict up/down directly, using log-loss or AUC as the objective. This aligns the training objective with your directional accuracy metric.

∙ Compare this classifier's directional accuracy to your regression models' directional accuracy.

**Confidence: 0.85** — XGBoost on financial features is well-documented to outperform linear models. Ensembles are almost always beneficial.

---

## 4. Training Methodology Improvements (Medium Impact)

### 4a. Target variable design

∙ Your Ridge model predicts **raw price** from lagged prices. This is problematic because prices are non-stationary (the distribution changes over time). The LSTM already predicts returns, which is better.

∙ **Switch Ridge to predict returns too.** Use lagged returns (not lagged prices) as features, predict next-day return, then convert to price. This makes the problem stationary and improves generalization.

### 4b. Expanding window vs. fixed split

∙ Your fixed 70/15/15 split uses a single train/test boundary. Results may be sensitive to where that boundary falls (e.g., a volatile period right at the split).

∙ **Use expanding-window evaluation:** Multiple test periods (e.g., walk-forward with monthly retraining). Report mean and std of metrics across windows. This gives more robust performance estimates.

∙ You already have a rolling backtest, but it retrains daily which is expensive. A monthly retrain with daily prediction is a good compromise.

### 4c. Hyperparameter tuning depth

∙ Your RandomizedSearchCV only tunes Ridge `alpha` (1 hyperparameter, 10 iterations). This is minimal.

∙ With XGBoost, you'd have 5–6 hyperparameters to tune. Use **Optuna** or **BayesSearchCV** instead of RandomizedSearchCV for more efficient search in higher-dimensional spaces.

∙ For the LSTM, tune: learning rate, hidden size, number of layers, dropout rate, sequence length, batch size. Use Optuna with Keras callbacks.

### 4d. Proper validation for LSTM

∙ Ensure LSTM validation uses the same time-based split (no data leakage in sequence construction). Sequences near the train/val boundary can leak future data if not handled carefully — verify that the last training sequence ends at `train_end - 1`, not `train_end`.

**Confidence: 0.80** — These are methodological improvements that reduce bias in your evaluation and better align training with evaluation.

---

## 5. Error Analysis Improvements (Medium Impact)

### 5a. Regime-conditional evaluation

∙ Your error analysis shows the model fails in high-volatility periods. Quantify this: **split the test set into terciles by volatility_14** and report MAE/RMSE/Dir.Acc for each tercile separately.

∙ This tells you exactly how much worse the model gets and whether directional accuracy degrades uniformly or collapses only in one regime.

### 5b. Calibration analysis

∙ For directional predictions, plot a **reliability diagram**: bin predictions by predicted return magnitude, check if larger predicted moves correspond to higher actual directional accuracy.

∙ If the model is not calibrated (e.g., it's equally accurate on small and large predicted moves), you can improve by only trading when the predicted move is large (a threshold approach you've started exploring in TensorTrade).

### 5c. Temporal patterns in errors

∙ Check if errors are **autocorrelated** (is a bad prediction today likely followed by a bad prediction tomorrow?). If yes, you can meta-learn when to trust the model.

∙ Plot directional accuracy as a **rolling 30-day window** over the test set to see if there are extended periods where the model works or fails.

**Confidence: 0.75** — These won't directly improve the model, but they provide insight for targeted improvements and better academic analysis.

---

## 6. Quick Win Priority List

Ranked by expected impact and implementation effort:

| Priority | Improvement | Expected Dir.Acc Gain | Effort |
|----------|-------------|----------------------|--------|
| 1 | Add XGBoost model | +2–5% | Low (drop-in with existing pipeline) |
| 2 | Add RSI, MACD, Bollinger features | +1–3% | Low (ta-lib or manual calc) |
| 3 | Add BTC returns as feature for altcoins | +1–3% | Low |
| 4 | Switch Ridge to return-based prediction | +0.5–2% | Low |
| 5 | LSTM early stopping + LR scheduling | +1–2% | Low |
| 6 | Ensemble (avg of Ridge + XGBoost + LSTM) | +1–3% | Medium |
| 7 | Custom directional loss for LSTM | +1–3% | Medium |
| 8 | Sequence length tuning | +0.5–1% | Medium |
| 9 | Optuna hyperparameter search | +0.5–2% | Medium |
| 10 | Direct classification model | +1–3% | Medium |

**Realistic target:** With improvements 1–6 implemented, directional accuracy on ETC-USD could move from ~53–55% to **57–62%**. On more predictable assets (ETH), potentially **60–65%**.

---

## 7. What Probably Won't Help

∙ **More lags beyond 30:** Diminishing returns. Your permutation importance already shows mid-range lags (lag_15) matter more than recent ones in some runs, suggesting 30 is sufficient.

∙ **Transformer/attention models:** Your dataset (~3000 rows) is too small. Transformers need 10x–100x more data to outperform LSTMs.

∙ **Sentiment analysis (without significant effort):** Free sentiment data (Twitter/Reddit) is noisy and hard to align with daily prices. It's a project in itself.

∙ **Raw price as target for Ridge:** You're already seeing the non-stationarity problem; switching to returns is the fix, not adding more price lags.

---

## Overall Confidence: 0.80

The improvements above are grounded in standard financial ML practice. The largest gains will come from XGBoost, better features, and ensembling. The LSTM improvements are important for academic rigor (showing you can properly train a deep model) but may not dramatically change the outcome — on daily crypto data with ~3000 samples, tree-based models typically match or beat LSTMs.

**Key caveat:** Crypto markets are noisy. Even with all improvements, consistent directional accuracy above 60% on daily data is difficult. The academic value is in demonstrating rigorous methodology and honest evaluation, not in achieving unrealistic accuracy.

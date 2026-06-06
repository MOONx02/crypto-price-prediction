# Model Extension Proposal — Crypto Price Prediction

## What We Found (v9)

| Model | Dir. Acc | Sharpe |
|---|---|---|
| Ridge | 54.16% | 1.14 |
| LSTM | 46.32% | -1.50 |

Three specific problems motivate the extensions below:

1. **The LSTM collapsed** — it made only 61 trades (vs Ridge's 169) and ended up predicting near-zero almost always. MSE loss on heavy-tailed return data causes this: the model learns to predict 0 to avoid big penalties on spike days.
2. **Ridge can't model interactions** — the ablation showed volatility alone *hurt* accuracy, but combined with volume it helped. That's a conditional effect a linear model can't express.
3. **Non-local lags dominate** — top features were lag_9, lag_16, lag_30, not recent lags. The LSTM compresses all 30 steps through a sequential hidden state, which buries exactly the signal that matters.

---

## Three Extensions

**1. Huber Loss + Attention LSTM**
Swap MSE for Huber loss (reduces the pull toward zero on spike days) and add an attention layer so the model can directly weight lag_9/lag_16/lag_30 instead of compressing everything sequentially. Minimal code change to the existing LSTM.

**2. XGBoost + Technical Indicators**
Replace Ridge with XGBoost (captures the volume×volatility interaction Ridge misses) and add RSI(14), MACD, and Bollinger Band width — all computed from existing OHLCV data. Run the same ablation to see which indicators actually help.

**3. Temporal Fusion Transformer**
Full architectural replacement of the LSTM. TFT uses multi-head attention across all 30 timesteps, so it can learn that lag_9 and lag_30 matter more than lag_1 without having to pass through every step in between. Most work to implement but most directly addresses why the LSTM failed.

---

## Plan

Start with **Extension 2** (easiest, tests the ablation hypothesis), then **Extension 1** (targeted fix to the LSTM), then **Extension 3** if time allows. All evaluated on the same test set and metrics as v9.

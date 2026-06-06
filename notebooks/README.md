# Notebooks

## AllInOne versioning

- **Version = pipeline only.** The current extra-credit working notebook is `Crypto_Colab_EC_v1.ipynb` (initialized from the v9 baseline and used for extension work).
- **Asset is a variation, not a version.** In the second cell, set `ASSET = "BTC-USD"` (or `"ETH-USD"`, `"XRP-USD"`, `"ETC-USD"`, etc.). One notebook runs any coin; no separate file per asset.
- **When you add a new pipeline revision:** Move the current file to `archive/` and create a new versioned notebook for the next milestone.

## Version history (pipeline only)

| Version | Description |
|---------|-------------|
| **v1** | Original: baselines, Lag+Ridge, LSTM on raw price (no scaling) → LSTM broken (~97k MAE). |
| **v2** | Fix: LSTM predicts returns, inputs scaled; convert predicted return to price. MAE/RMSE ~1598 / ~2202. |
| **v3** | + volume and rolling volatility (data, Lag+Ridge, LSTM). (Archived.) |
| **v4** | v3 + rolling backtest, TimeSeriesSplit + RandomizedSearchCV, residual plots. (Archived.) |
| **v5** | v4 + **Phase 4 ablation** (lags only / +volume / +volatility / all). (Archived.) |
| **v6** | v5 + **Phase 5 interpretability** (permutation importance, PDP/ICE, error analysis). (Superseded by v7.) |
| **v7** | v6 + returns-based targets (Ridge/baselines predict return), directional accuracy on returns (excl. zero), volatility per-split, TimeSeriesSplit gap=21, single-layer LSTM + dropout, long/short backtest with transaction costs. |
| **v8** | v7 + **XGBoost** (nonlinear model), **technical indicators** (RSI, MACD, Bollinger Band position), **multi-horizon returns** (3d/7d/14d/30d), **BTC cross-asset features** (lag 1–3), **return-based Ridge** (stationarity fix), **improved LSTM** (64→32, dropout 0.2, early stopping, LR scheduling), **weighted ensemble** (Ridge + XGBoost + LSTM by val Dir.Acc). |
| **v9** | Simplified rubric-aligned pipeline: baselines + Ridge + LSTM, 32 features (30 lags + volume + volatility), 4-group ablation, interpretability, error analysis, and long/short backtest. |
| **EC_v1** | Extra-credit execution notebook seeded from v9 baseline; intended home for XGBoost+indicators, Huber+Attention LSTM, and TFT experiments. **Current.** |

## EC_v1 run order

For reproducible EC results in `Crypto_Colab_EC_v1.ipynb`, run in this order:
1. Baseline sections (1-13 from v9 flow)
2. Baseline lock + unified evaluation ledger
3. Extension 2: XGBoost + indicators + 5-group ablation
4. Extension 1: Huber-loss attention LSTM
5. Extension 3: TFT benchmark (optional dependencies)
6. Final unified comparison outputs

## Archive

`archive/` holds:

- **01_data_and_baselines.ipynb**, **02_lag_model.ipynb**, **03_lstm.ipynb** — original pipeline notebooks.
- **Crypto_Colab_AllInOne_v1.ipynb**, **v2.ipynb**, **v3.ipynb**, **v4.ipynb**, **v5.ipynb** — superseded by v6 (in archive).
- **Crypto_Colab_AllInOne_v3_colab_run.ipynb** — v3 run on Colab.
- **v4_ETH.ipynb**, **v5_XRP.ipynb**, **v6_ETC-test.ipynb** — old per-coin copies; asset is now a config in v4, not a separate version.

## TensorTrade (optional)

**TensorTrade_Model_Backtest.ipynb** uses the [TensorTrade](https://github.com/tensortrade-org/tensortrade) RL framework to backtest our Lag+Ridge (or LSTM) predictions as a trading signal: threshold policy (buy/sell/hold when predicted return exceeds a threshold) inside TensorTrade’s execution simulation (commission, P&L). Run data + Lag model cells (or AllInOne v6 pipeline), then install TensorTrade (`pip install gymnasium git+https://github.com/tensortrade-org/tensortrade.git`) and run the backtest to compare model-threshold P&L vs buy-and-hold.

**Reference run:** [result.ipynb](../result.ipynb) at repo root is a saved Colab run of this backtest (ETC-USD, with pip/outputs). Use it as the reference for expected dependency messages and backtest output.

**Using with AllInOne v7:** Use the same **ASSET** in both notebooks. Run v7 for prediction quality (MAE, RMSE, Dir.Acc, ablation, interpretability); run TensorTrade_Model_Backtest for trading outcome (P&L, buys/sells, vs buy-and-hold vs cash). Together they give you prediction metrics and simulated trading results for the same asset and split.

## Combined notebook (pipeline + TensorTrade)

**AllInOne_Plus_TensorTrade.ipynb** merges both in one place: (1) data, baselines, Lag+Ridge, LSTM, comparison table (same essentials as v7); (2) TensorTrade backtest on the Lag+Ridge signal. One run gives you prediction metrics and trading P&L. For the full v7 pipeline (returns-based, vol per-split, CV gap, LSTM, long/short backtest) use [Crypto_Colab_AllInOne_v7.ipynb](Crypto_Colab_AllInOne_v7.ipynb).

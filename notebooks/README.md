# Notebooks

## AllInOne versioning

- **Version = pipeline only.** The current notebook is `Crypto_Colab_AllInOne_v5.ipynb` (rolling backtest, TimeSeriesSplit + RandomizedSearchCV, residual plots, **Phase 4 ablation**).
- **Asset is a variation, not a version.** In the second cell, set `ASSET = "BTC-USD"` (or `"ETH-USD"`, `"XRP-USD"`, `"ETC-USD"`, etc.). One notebook runs any coin; no separate file per asset.
- **When you add a new pipeline revision:** Move the current file to `archive/` and create `Crypto_Colab_AllInOne_v(N+1).ipynb` (e.g. v5 → v6); update the first cell.

## Version history (pipeline only)

| Version | Description |
|---------|-------------|
| **v1** | Original: baselines, Lag+Ridge, LSTM on raw price (no scaling) → LSTM broken (~97k MAE). |
| **v2** | Fix: LSTM predicts returns, inputs scaled; convert predicted return to price. MAE/RMSE ~1598 / ~2202. |
| **v3** | + volume and rolling volatility (data, Lag+Ridge, LSTM). (Archived.) |
| **v4** | v3 + rolling backtest, TimeSeriesSplit + RandomizedSearchCV, residual plots. (Archived.) |
| **v5** | v4 + **Phase 4 ablation** (lags only / +volume / +volatility / all). Current. Asset chosen via `ASSET` in notebook. |

## Archive

`archive/` holds:

- **01_data_and_baselines.ipynb**, **02_lag_model.ipynb**, **03_lstm.ipynb** — original pipeline notebooks.
- **Crypto_Colab_AllInOne_v1.ipynb**, **v2.ipynb**, **v3.ipynb**, **v4.ipynb** — superseded by v5.
- **Crypto_Colab_AllInOne_v3_colab_run.ipynb** — v3 run on Colab.
- **v4_ETH.ipynb**, **v5_XRP.ipynb**, **v6_ETC-test.ipynb** — old per-coin copies; asset is now a config in v4, not a separate version.

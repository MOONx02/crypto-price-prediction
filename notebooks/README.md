# Notebooks

## AllInOne versioning

- **Current working notebook:** `Crypto_Colab_AllInOne_vN.ipynb` (use the **highest** version number in this folder). **v3** = BTC; **v4_ETH** = Ethereum; **v5_XRP** = Ripple; **v6_ETC** = Ethereum Classic (same pipeline, different asset).
- **When you're done with a version** (e.g. ran it on Colab, saved results):  
  Move that file to `archive/` and create the next as `Crypto_Colab_AllInOne_v(N+1).ipynb`.
- **Next revision:** Copy the latest versioned file, rename to the new version number, and update the first cell.

## Version history

| Version | Description |
|---------|-------------|
| **v1** | Original: baselines, Lag+Ridge, LSTM on raw price (no scaling) → LSTM broken (~97k MAE). |
| **v2** | Fix: LSTM predicts returns, inputs scaled; convert predicted return to price. MAE/RMSE ~1598 / ~2202. |
| **v3** | Improvement: + volume and rolling volatility (data, Lag+Ridge, LSTM). BTC. LSTM Dir.Acc ~51%. |
| **v4_ETH** | Same as v3, asset = **Ethereum** (ETH-USD). Compare to BTC. |
| **v5_XRP** | Same as v3, asset = **Ripple** (XRP-USD). Compare to BTC/ETH. |
| **v6_ETC** | Same as v3, asset = **Ethereum Classic** (ETC-USD). Compare to BTC/ETH/XRP. |

## Archive

`archive/` holds:

- **01_data_and_baselines.ipynb**, **02_lag_model.ipynb**, **03_lstm.ipynb** — original pipeline notebooks.
- **Crypto_Colab_AllInOne_v1.ipynb** — original (broken LSTM).
- **Crypto_Colab_AllInOne_v2.ipynb** — fix (returns + scaling).
- **Crypto_Colab_AllInOne_v3_colab_run.ipynb** — v3 run on Colab (51% Dir.Acc).
- When you start v4, move `Crypto_Colab_AllInOne_v3.ipynb` here and create v4 in the notebooks folder.

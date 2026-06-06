# EC Findings Log

## 2026-05-03 - V2 Results Snapshot

Notebook: `Crypto_Colab_EC_v2_results.ipynb`

### Key outcomes
- `MA7_baseline`: Dir.Acc `0.5629`
- `Ridge_v9_baseline`: Dir.Acc `0.5186`, Sharpe `0.1514`, P&L `+0.1635`
- `XGBoost_indicators`: Dir.Acc `0.5000`, Sharpe `1.1894`, P&L `+1.2793` (best trading outcome)
- `Huber_Attention_LSTM`: Dir.Acc `0.4860`, Sharpe `0.1334`, P&L `+0.1439`
- `LSTM_v9_baseline`: Dir.Acc `0.4651`, Sharpe `-1.2260`, P&L `-1.3197`
- `TFT`: Dir.Acc `0.4721`, Sharpe `-1.1597`, P&L `-1.2491`

### Findings
- XGBoost delivered the strongest trading metrics despite lower directional accuracy than Ridge.
- Huber+Attention improved LSTM direction and reduced loss severity, but remains below Ridge/XGBoost.
- TFT underperformed in this constrained CPU training configuration.
- Current ranking differs by metric family (Dir.Acc vs Sharpe/P&L), indicating objective mismatch.

### Improvement direction (next run)
1. Tune long/short decision threshold on validation per model (Sharpe-first).
2. Select final model by trading objective (Sharpe/P&L) instead of direction alone.
3. Keep TFT as optional benchmark unless training budget is increased.

## 2026-05-03 - v3 notebook created

Notebook: `Crypto_Colab_EC_v3.ipynb`

Implemented incremental improvements:
- Added `vol_x_volume` interaction feature.
- Retuned XGBoost on validation Sharpe with tighter regularization.
- Added validation threshold tuning with minimum-trade guard.
- Added cost sensitivity analysis (5/10/15/20 bps).
- Added Section 17 graphical effectiveness analysis (Sharpe/P&L bars, cumulative curves, cost lines, threshold sweep).

## 2026-05-18 - v3 stable notebook created

Notebook: `Crypto_Colab_EC_v3_stable.ipynb`

Purpose: reliable Colab **Run all** without kernel crashes.

Changes vs v3:
- Removed LSTM and TFT sections entirely.
- Removed TensorFlow/Torch installs and imports.
- Keeps baselines, Ridge, XGBoost v3, threshold tuning, cost sensitivity, and Section 17 plots.

## 2026-05-18 - proposal_complete notebook created

Notebook: `Crypto_Colab_EC_proposal_complete.ipynb`

Purpose: full extra-credit proposal coverage with safe execution controls.

Includes:
- Extension 2: XGBoost + RSI/MACD/Bollinger + vol_x_volume + 5-group ablation
- Extension 1: Huber + Attention LSTM (default params in SAFE_MODE)
- Extension 3: TFT with try/except skip path
- SAFE_MODE switch (`SAFE_MODE=True` skips TFT/heavy Optuna by default)
- Section 18 proposal compliance checklist (PASS/FAIL table)
- Default asset set to ETH-USD

## 2026-05-18 - proposal_complete (2) full run snapshot

Notebook: `Crypto_Colab_EC_proposal_complete (2).ipynb`

Run mode:
- `SAFE_MODE=False`, `RUN_TFT=True`, `RUN_LSTM_OPTUNA=True`
- All three extensions executed; compliance score `7/8 PASS`

### Key outcomes
- `Ridge_v9_baseline`: Dir.Acc `0.5231`, Sharpe `1.1028`, P&L `+1.1226`
- `XGBoost_raw`: Dir.Acc `0.5417`, Sharpe `0.6080`, P&L `+0.6208`
- `XGBoost_tuned`: Dir.Acc `0.5417`, Sharpe `0.1592`, P&L `+0.1262`
- `Huber_Attention_LSTM`: Dir.Acc `0.5069`, Sharpe `0.2864`, P&L `+0.2925`
- `TFT`: Dir.Acc `0.5139`, Sharpe `0.3835`, P&L `+0.3917`
- `LSTM_v9_baseline`: Dir.Acc `0.4676`, Sharpe `-0.1406`, P&L `-0.1437`

### Emphasized takeaway
- Highest directional accuracy came from XGBoost: `54.17%` (`0.541667`), higher than Ridge (`52.31%`).
- Both `XGBoost_raw` and `XGBoost_tuned` kept the same Dir.Acc (`54.17%`) because threshold tuning changed execution/trade filtering more than sign prediction.
- XGBoost's directional lift is consistent with richer nonlinear feature modeling (lags + RSI/MACD/Bollinger + interaction effects).
- Ranking remains metric-dependent: XGBoost leads direction, while Ridge remains best on Sharpe/P&L.

### Additional notes
- XGBoost regime behavior supports the proposal hypothesis:
  - `high_vol`: XGB `0.5833` vs Ridge `0.5463`
  - `high_vol_high_volume`: XGB `0.6098` vs Ridge `0.5854`
- Threshold tuning reduced Sharpe for top models in this run (Ridge and XGBoost), indicating policy overfitting risk.

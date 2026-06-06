# Extra Credit Final Report - Crypto Price Prediction (ECPS 211)

## 1) Purpose and Scope

This report summarizes the extra-credit work proposed in `extra_credit_proposal.md` and documents findings from `EC_FINDINGS_LOG.md`. The goal was to investigate whether targeted model and feature upgrades could address known weaknesses in the v9 baseline system:

- LSTM collapse toward near-zero predictions under MSE on heavy-tailed returns.
- Ridge inability to capture nonlinear interactions (especially volatility-volume effects).
- Evidence that non-local lags (e.g., lag_9, lag_16, lag_30) matter more than recent lags.

The proposal committed to three extensions:
1. **Extension 1:** Huber Loss + Attention LSTM  
2. **Extension 2:** XGBoost + technical indicators  
3. **Extension 3:** Temporal Fusion Transformer (TFT)  

All models were evaluated with the same family of metrics: directional accuracy, Sharpe ratio, and P&L.

---

## 2) What Was Implemented

### Extension 1 - Huber + Attention LSTM
- Replaced MSE-oriented setup with Huber-style robustness and added attention over lookback timesteps.
- Intended effect: reduce pull-to-zero behavior on spike days and preserve informative non-local lags.

### Extension 2 - XGBoost + Indicator Set
- Added nonlinear tree model and expanded features using RSI(14), MACD, Bollinger Band width, and interaction term `vol_x_volume`.
- Included ablation and regime comparisons to test whether nonlinear interactions improve directional signal.

### Extension 3 - Temporal Fusion Transformer (TFT)
- Added TFT as the full architecture replacement for sequence modeling.
- Included safe execution controls and optional skip path for computational stability.

### Execution/Engineering Support
- Built progressively from v2 -> v3 -> v3 stable -> proposal-complete notebooks.
- Added threshold tuning, cost sensitivity analysis, and graphical diagnostics.
- Added `SAFE_MODE` controls for reliable Colab execution while preserving full-coverage run options.

---

## 3) Results Summary

## Final full-coverage run (`SAFE_MODE=False`, all extensions executed)

| Model | Directional Accuracy | Sharpe | P&L |
|---|---:|---:|---:|
| Ridge v9 baseline | 0.5231 | **1.1028** | **+1.1226** |
| XGBoost raw | **0.5417** | 0.6080 | +0.6208 |
| XGBoost tuned | **0.5417** | 0.1592 | +0.1262 |
| Huber + Attention LSTM | 0.5069 | 0.2864 | +0.2925 |
| TFT | 0.5139 | 0.3835 | +0.3917 |
| LSTM v9 baseline | 0.4676 | -0.1406 | -0.1437 |

Compliance status from the notebook log: **7/8 PASS**.

### Earlier run signal (v2 snapshot)
- XGBoost achieved the best trading outcome in that run (Sharpe 1.1894, P&L +1.2793) despite lower directional accuracy than some baselines.
- This reinforced that model ranking depends strongly on the selected objective.

---

## 4) Findings by Proposed Topic

### Topic A - Fixing LSTM collapse
**Finding:** Partially successful.  
- Huber + Attention clearly improved over the old LSTM baseline (direction and trading metrics both improved from negative/weak baseline behavior).
- However, the upgraded LSTM still did not surpass Ridge on Sharpe/P&L or XGBoost on directional accuracy.

**Interpretation:**  
The proposed fix addressed part of the failure mode (reduced collapse severity), but sequence model gains were not strong enough to dominate tree/linear baselines on this dataset and compute budget.

### Topic B - Capturing nonlinear interactions (Ridge limitation)
**Finding:** Supported.  
- XGBoost produced the highest directional accuracy in the full run (54.17% vs Ridge 52.31%).
- Regime breakdown favored XGBoost in high-volatility and high-volatility-high-volume subsets.

**Interpretation:**  
This supports the proposal hypothesis that richer nonlinear modeling better captures conditional structure (including interaction-like behavior) than Ridge.

### Topic C - Handling non-local lag importance
**Finding:** Mixed support.  
- Attention LSTM and TFT both improved over old LSTM baseline behavior, suggesting some value from architectures that can better access non-local temporal information.
- Neither sequence architecture became top performer overall in this project setting.

**Interpretation:**  
Non-local lag handling likely matters, but practical performance remained constrained by optimization, training budget, and policy calibration.

### Topic D - Objective mismatch (direction vs trading quality)
**Finding:** Strongly confirmed.  
- The model with best directional accuracy was not always best on Sharpe/P&L.
- In final run: XGBoost led direction; Ridge led Sharpe/P&L.
- In earlier run: XGBoost led trading metrics even when not top in direction.

**Interpretation:**  
Direction-only selection is insufficient for a trading task; final model choice must be aligned to Sharpe/P&L and transaction-cost-aware execution.

---

## 5) Important Discoveries

1. **Directional edge and trading edge are not equivalent.**  
   The experiments repeatedly showed ranking flips between directional accuracy and Sharpe/P&L.

2. **XGBoost provided the strongest directional lift.**  
   It reached 54.17% directional accuracy and showed stronger behavior in volatile/high-volume regimes.

3. **Ridge remained a robust trading benchmark.**  
   In the full proposal-complete run, Ridge delivered the best Sharpe and P&L.

4. **Huber + Attention improved LSTM reliability but did not fully close the gap.**  
   The collapse problem was mitigated relative to old LSTM, yet not enough for overall leadership.

5. **Threshold tuning can overfit execution policy.**  
   The log notes cases where tuning lowered Sharpe for top models, highlighting validation-policy fragility.

6. **TFT is sensitive to compute and training setup.**  
   It underperformed in constrained settings and remained a secondary benchmark unless more budget is available.

---

## 6) Conclusion

The proposal was substantially executed: all three extensions were implemented and run in the full-coverage notebook, with documented compliance and stable execution controls. The major empirical outcome is that **Extension 2 (XGBoost + engineered indicators/interactions) gave the clearest directional improvement**, while **Ridge remained the strongest trading baseline in the final run**.  

The project's most important methodological lesson is objective alignment: a model chosen for directional accuracy alone may be suboptimal for actual trading outcomes. Future iterations should prioritize Sharpe/P&L-aware selection, robust threshold policy validation, and expanded compute for sequence models only if justified by incremental gains.

---

## 7) Recommended Next Steps (if continuing)

- Select model by trading objective first (Sharpe/P&L under costs), not direction alone.
- Re-run threshold tuning with stricter anti-overfit controls (rolling validation or nested validation).
- Keep TFT as optional unless additional training budget and tuning depth are available.
- Preserve XGBoost regime diagnostics; they are the strongest evidence for nonlinear interaction value.

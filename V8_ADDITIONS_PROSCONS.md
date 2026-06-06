# v8 Additions: Did They Help? Pros & Cons

**Purpose:** Compare v7 → v8 (ETC-USD) and summarize what to keep in the report/PPT/notebook vs what to downplay or omit. **Bug fixes and methodology fixes stay regardless.**

---

## Quick numbers (ETC-USD, test)

| Metric | v7 (pre-v8) | v8 (current) |
|--------|-------------|--------------|
| **Ridge** | Lag+Ridge: MAE(price) 0.895, Dir.Acc **53.2%** | Ridge: MAE(price) 0.524, Dir.Acc **52.0%** |
| **LSTM** | Dir.Acc **45.6%** | Dir.Acc **48.2%** |
| **7-day MA** | Dir.Acc 55.3% | Dir.Acc 55.2% |
| **Best Dir.Acc** | 7-day MA (55.3%) | 7-day MA (55.2%) |
| **Best ML Dir.Acc** | Ridge 53.2% | Ridge 52.0% |

v8 **additions**: XGBoost (Dir.Acc 48.2%), weighted ensemble (50.8%), 53 features (vs ~32), Optuna tuning, stacking meta-learner, XGBoost classifier, expanding-window eval, error analysis (regime/calibration/temporal).

---

## 1. Return-based Ridge (predict return → price)

| | Pros | Cons |
|---|-----|-----|
| **Impact** | **Large.** MAE(price) 0.895 → 0.524. Stationarity fix; methodology is correct. | — |
| **Report/notebook** | **Keep.** This is a core fix and improves MAE/RMSE fairly. |

**Verdict:** Meaningful improvement. Keep in report and notebook.

---

## 2. 53 features vs ~32 (technical indicators, multi-horizon returns, calendar, BTC cross-asset)

| | Pros | Cons |
|---|-----|-----|
| **Impact** | Ablation shows which groups help; interpretability (importance, PDP) is richer. | Ridge Dir.Acc **53.2% → 52.0%** (slight drop). No clear directional gain; more complexity, more overfitting risk. |
| **Report/notebook** | Good for methods (we tried standard finance features) and ablation/interpretability. | Don’t oversell “53 features” as an improvement; numbers don’t support it for direction. |

**Verdict:** No meaningful directional improvement; slight loss for Ridge. Keep feature list in methods, report ablation and interpretability; in report/PPT don’t emphasize “53 vs 32” as a win. Optional: in notebook you could keep a “lite” run (e.g. lags + volume + volatility only) for a simpler comparison.

---

## 3. XGBoost

| | Pros | Cons |
|---|-----|-----|
| **Impact** | Best MAE on returns and price (0.0293, 0.513). Adds model diversity for ensemble. | Dir.Acc **48.2%** (below 50%). Assessment hoped for +2–5%; we got worse direction than Ridge. |
| **Report/notebook** | Shows you tried nonlinear models; honest result (best MAE, worse direction). | Don’t claim XGBoost “improves” the project; it improves MAE only. |

**Verdict:** Meaningful for MAE only; not for direction. Keep in report as “best point forecast among ML models, directional accuracy below 50%.” In PPT, one line is enough; no need to highlight as a big win.

---

## 4. Weighted ensemble (Ridge + XGBoost + LSTM by val Dir.Acc)

| | Pros | Cons |
|---|-----|-----|
| **Impact** | Dir.Acc 50.8% (between Ridge and XGBoost/LSTM); shows ensemble methodology. | Doesn’t beat Ridge (52%) or 7-day MA (55.2%). No clear benefit over “just use Ridge.” |
| **Report/notebook** | Methodologically sound; good for a “we tried ensembling” sentence. | Don’t oversell; say it sits between models and doesn’t beat best single model. |

**Verdict:** No meaningful improvement over Ridge. Keep briefly in report/notebook; don’t feature in PPT as an improvement.

---

## 5. Optuna tuning (Ridge + XGBoost)

| | Pros | Cons |
|---|-----|-----|
| **Impact** | Rigorous hyperparameter search; reproducible. | Ridge direction slightly worse than v7 (53.2% → 52.0%); no visible directional gain from tuning. |
| **Report/notebook** | Keep in methods (how models were tuned). | Don’t claim “Optuna improved results”; it didn’t for direction. |

**Verdict:** Methodology improvement only. Keep in methods; don’t cite as a performance win in report/PPT.

---

## 6. LSTM improvements (64→32 units, dropout, early stopping, LR scheduling)

| | Pros | Cons |
|---|-----|-----|
| **Impact** | Dir.Acc **45.6% → 48.2%** (~+2.6%). Training is more robust. | Still below 50%; doesn’t beat Ridge or 7-day MA. |
| **Report/notebook** | Keep; shows proper deep-learning practice and a clear LSTM improvement. | Don’t oversell; still “LSTM not competitive on direction for this asset.” |

**Verdict:** Small but real improvement. Keep in report/notebook; frame as “LSTM improved but still below 50% direction.”

---

## 7. Stacking meta-learner + XGBoost classifier (optional sections)

| | Pros | Cons |
|---|-----|-----|
| **Impact** | Aligns second-level model with direction; compares regression vs classification. | Report doesn’t emphasize these; likely similar or below Ridge Dir.Acc. |
| **Report/notebook** | Optional “we also tried” in report; can omit from PPT. | Extra complexity; no evidence they beat 7-day MA or Ridge. |

**Verdict:** Optional. Keep in notebook for completeness; in report one short sentence or omit; omit from PPT unless you want to show “we tried classification too.”

---

## 8. Expanding-window evaluation (Section 9b)

| | Pros | Cons |
|---|-----|-----|
| **Impact** | More robust view (mean ± std across windows); less dependence on single split. | Doesn’t change the headline “best direction = 7-day MA / Ridge.” |
| **Report/notebook** | Keep in methods and results (robustness). | Don’t claim it “improves” metrics; it improves *assessment*. |

**Verdict:** Methodology improvement. Keep in report; one line in PPT is enough.

---

## 9. Error analysis (regime-conditional, calibration, temporal)

| | Pros | Cons |
|---|-----|-----|
| **Impact** | Explains *where* models fail (high vol, large moves); academically strong. | Doesn’t improve MAE or Dir.Acc. |
| **Report/notebook** | **Keep.** Valuable for interpretation and conclusions. | — |

**Verdict:** Meaningful for understanding, not for numbers. Keep in report and optionally in PPT (one slide).

---

## What to keep no matter what (you said so)

- All **bug fixes** (e.g. return-based target, LSTM scaling, sequence boundaries, numpy/pandas pins).
- **Methodology** that is correct (time split, no leakage, expanding window, Optuna as *method*).

---

## Summary: what actually improved

| Addition | Meaningful improvement? | Suggest for report/PPT/notebook |
|----------|-------------------------|----------------------------------|
| Return-based Ridge | **Yes** (MAE) | **Keep prominent** |
| 53 vs 32 features | **No** (Dir.Acc slightly worse) | Methods + ablation only; don’t hype feature count |
| XGBoost | **Yes for MAE only**; no for direction | Keep; say “best MAE, Dir.Acc &lt; 50%” |
| Ensemble | **No** (doesn’t beat Ridge) | Keep briefly; don’t feature |
| Optuna | **No** (no directional gain) | Methods only |
| LSTM improvements | **Small** (45.6% → 48.2%) | Keep; “improved but still &lt; 50%” |
| Stacking / XGB classifier | **No** | Optional or omit in report/PPT |
| Expanding window | **Methodology** | Keep in methods |
| Error analysis | **Understanding, not metrics** | **Keep** (interpretation) |

**Bottom line:** The only clear *numerical* wins are (1) return-based Ridge for MAE/RMSE and (2) LSTM going from 45.6% to 48.2% Dir.Acc. The rest are either methodology/rigor (keep but don’t sell as “improvements”) or no meaningful gain (53 features, ensemble, Optuna for direction). You can simplify the report/PPT by not emphasizing 53 features, ensemble, or Optuna as performance gains, and optionally trim stacking/classifier from the slides.

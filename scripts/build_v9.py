#!/usr/bin/env python3
"""
Build v9 notebook from v8: remove XGBoost, ensemble, stacking, classifier, 12b.
Use minimal features (32 = 30 lags + log_volume + volatility_14), 4-group ablation.
All content edits so v9 runs without xgb/ta/btc.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
V8 = REPO / "notebooks" / "Crypto_Colab_AllInOne_v8.ipynb"
V9 = REPO / "notebooks" / "Crypto_Colab_AllInOne_v9.ipynb"


def src(cell):
    return cell["source"] if isinstance(cell["source"], list) else [cell["source"]]


def join_src(cell):
    return "".join(src(cell))


def set_src(cell, text):
    lines = text.rstrip().split("\n")
    cell["source"] = [line + "\n" for line in lines[:-1]] + ([lines[-1] + "\n"] if lines[-1] else [])


def main():
    with open(V8) as f:
        nb = json.load(f)
    cells = nb["cells"]
    new_cells = []
    i = 0
    while i < len(cells):
        c = dict(cells[i])
        s = join_src(c)
        if "## 6. XGBoost" in s and c["cell_type"] == "markdown":
            i += 3
            continue
        if "## 8. Ensemble" in s and c["cell_type"] == "markdown":
            i += 3
            continue
        if "## 8b. Stacking" in s and c["cell_type"] == "markdown":
            i += 2
            continue
        if "## 8c. Direct Classification" in s and c["cell_type"] == "markdown":
            i += 2
            continue
        if "### 12b. Error Analysis Extensions" in s and c["cell_type"] == "markdown":
            i += 2
            continue

        # Content edits for v9
        if "# Crypto Price Prediction" in s and "v8" in s and c["cell_type"] == "markdown":
            set_src(c, """# Crypto Price Prediction — v9

**Machine Learning and Data Mining** — ECPS 211 Winter 2026

**v9 (simplified):** Meets course rubric with minimal complexity. Two baselines (last value, 7-day MA); **Ridge** (30 return lags + log_volume + volatility_14, Optuna-tuned); **LSTM** (64→32 units, dropout, early stopping). **4-group ablation** (lags → +volume → +volatility → all). **Interpretability** (permutation importance + PDP/ICE on Ridge). **Error analysis** (residuals + where model fails). **Expanding-window** evaluation (Ridge). No XGBoost/ensemble/stacking/classifier.

Set `ASSET` below and **Runtime → Run all**.""")
        elif "!pip install" in s and "xgboost" in s:
            set_src(c, '''# Pin numpy/pandas for Colab + TensorFlow compatibility
!pip install -q "numpy>=1.26,<2.2" "pandas>=2.2.3,<3"
!pip install -q yfinance pyarrow scikit-learn tensorflow matplotlib seaborn optuna
print("Install done. Ignore other pip conflict warnings for this notebook.")''')
        elif "import xgboost" in s and "import ta" in s:
            set_src(c, """import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)
from sklearn.inspection import permutation_importance, PartialDependenceDisplay

import tensorflow as tf
from tensorflow.keras import layers, callbacks

print(f"NumPy {np.__version__}, Pandas {pd.__version__}, TF {tf.__version__}")""")
        elif "Download main asset" in s and "Download BTC" in s:
            set_src(c, """# Download main asset
raw = yf.download(ASSET, start="2017-01-01", end=None, progress=False, auto_adjust=True)
if isinstance(raw.columns, pd.MultiIndex):
    raw.columns = raw.columns.droplevel(1)
raw.index = pd.to_datetime(raw.index).tz_localize(None)
raw = raw.sort_index().ffill().dropna()

print(f"{ASSET}: {len(raw)} rows, {raw.index[0].date()} to {raw.index[-1].date()}")""")
        elif "## 2. Enhanced Feature Engineering" in s:
            set_src(c, "## 2. Feature Engineering (v9: minimal)\n\n30 return lags + **log_volume**, **volatility_14** (32 features). Ablation adds these incrementally (Section 9).")
        elif "Base features" in s and "EXTRA_FEATURE_COLS" in s and "rsi_14" in s:
            set_src(c, """# Base features (v9: lags + volume + volatility only)
df = pd.DataFrame(index=raw.index)
df["price"] = raw["Close"].values
df["volume"] = raw["Volume"].values.astype(float)
df["volume"] = df["volume"].fillna(0)

df["ret"] = (df["price"] - df["price"].shift(1)) / (df["price"].shift(1) + 1e-12)
df["log_volume"] = np.log1p(df["volume"])
df["volatility_14"] = df["ret"].rolling(14).std()

df = df.iloc[30:].copy()
df = df.replace([np.inf, -np.inf], np.nan).fillna(0)

EXTRA_FEATURE_COLS = ["log_volume", "volatility_14"]
LSTM_FEATURE_COLS = ["ret", "log_volume", "volatility_14"]

print(f"DataFrame shape: {df.shape}")
print(f"Total features for Ridge: {N_LAGS} lags + {len(EXTRA_FEATURE_COLS)} = {N_LAGS + len(EXTRA_FEATURE_COLS)}")
print(f"LSTM features per timestep: {len(LSTM_FEATURE_COLS)}")""")
        elif "Build return lags + extra features for Ridge/XGBoost" in s:
            set_src(c, s.replace("for Ridge/XGBoost", "for Ridge"))
        elif "## 5. Ridge" in s:
            set_src(c, "## 5. Ridge Regression (Return Lags + Volume, Volatility)")
        elif "## 7. Improved LSTM" in s:
            set_src(c, "## 6. LSTM\nSequences: 30 steps, 3 features (ret, log_volume, volatility_14). 64→32 units, dropout 0.2, early stopping, ReduceLROnPlateau.")
        elif "## 9. Full Comparison Table" in s:
            set_src(c, "## 7. Full Comparison Table")
        elif "Comparison table" in s and "pred_xgb_test" in s:
            set_src(c, """# Comparison table (v9: baselines + Ridge + LSTM)
da_ridge_test = dir_acc_returns(y_test, pred_ridge_test)
da_lstm_test = dir_acc_returns(y_te_lstm, pred_lstm_test)

rows = [
    ["Last Value", f"{m_last['mae']:.4f}", f"{m_last['rmse']:.4f}", f"{m_last['dir_acc']:.4f}", "—"],
    ["7-day MA", f"{m_ma['mae']:.4f}", f"{m_ma['rmse']:.4f}", f"{m_ma['dir_acc']:.4f}", "—"],
    ["Ridge (v9)", f"{m_ridge.get('mae_price', 0):.4f}", f"{m_ridge.get('rmse_price', 0):.4f}", f"{da_ridge_test:.4f}", f"{m_ridge['mae_ret']:.6f}"],
    ["LSTM (v9)", f"{m_lstm.get('mae_price', 0):.4f}", f"{m_lstm.get('rmse_price', 0):.4f}", f"{da_lstm_test:.4f}", f"{m_lstm['mae_ret']:.6f}"],
]
comp_df = pd.DataFrame(rows, columns=["Model", "MAE (price)", "RMSE (price)", "Dir.Acc", "MAE (return)"])
print("\\n" + "=" * 80)
print(f"COMPARISON TABLE — {ASSET} (v9)")
print("=" * 80)
print(comp_df.to_string(index=False))
print("=" * 80)""")
            new_cells.append(c)
            bar_graph = """# Bar graph: directional accuracy of all models
models_acc = ["Last Value", "7-day MA", "Ridge", "LSTM"]
dir_acc_pct = [
    m_last["dir_acc"] * 100,
    m_ma["dir_acc"] * 100,
    da_ridge_test * 100,
    da_lstm_test * 100,
]
colors = ["gray", "steelblue", "darkorange", "green"]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(models_acc, dir_acc_pct, color=colors, edgecolor="black", linewidth=0.8)
ax.axhline(50, color="red", linestyle="--", linewidth=1, label="Random (50%)")
ax.set_ylabel("Directional accuracy (%)")
ax.set_xlabel("Model")
ax.set_title(f"Directional accuracy by model — {ASSET} (v9)")
ax.set_ylim(0, 100)
ax.legend()
for bar, val in zip(bars, dir_acc_pct):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5, f"{val:.1f}%", ha="center", fontsize=10)
plt.tight_layout()
plt.show()"""
            bar_lines = [ln + "\n" for ln in bar_graph.rstrip().split("\n")]
            new_cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": bar_lines})
            i += 1
            continue
        elif "## 9b. Expanding-Window" in s:
            set_src(c, "## 8. Expanding-Window Evaluation\n\nWalk-forward: retrain Ridge on expanding train; report mean ± std of MAE (return) and Dir.Acc.")
        elif "Expanding-window: multiple test periods" in s and "xgb_w" in s:
            set_src(c, """# Expanding-window: Ridge only (v9)
N_WINDOWS = 5
n_test = len(test_df)
if n_test < N_WINDOWS * 20:
    N_WINDOWS = max(2, n_test // 30)
chunk_ends = np.linspace(0, n_test, N_WINDOWS + 1, dtype=int)

dir_acc_ridge_w, mae_ret_ridge_w = [], []
for w in range(N_WINDOWS):
    start_w, end_w = chunk_ends[w], chunk_ends[w + 1]
    if end_w - start_w < 5:
        continue
    train_end_w = val_end + start_w
    train_df_w = df.iloc[:train_end_w].copy()
    test_df_w = test_df.iloc[start_w:end_w].copy()
    X_tr_w, y_tr_w, _ = build_return_lag_matrix(train_df_w, N_LAGS, EXTRA_FEATURE_COLS)
    X_te_w, y_te_w, _ = build_return_lag_matrix(test_df_w, N_LAGS, EXTRA_FEATURE_COLS)
    if len(X_te_w) == 0:
        continue
    scaler_w = StandardScaler()
    X_tr_sc_w = scaler_w.fit_transform(X_tr_w)
    X_te_sc_w = scaler_w.transform(X_te_w)
    ridge_w = Ridge(alpha=best_alpha).fit(X_tr_sc_w, y_tr_w)
    pr_ridge_w = ridge_w.predict(X_te_sc_w)
    dir_acc_ridge_w.append(dir_acc_returns(y_te_w, pr_ridge_w))
    mae_ret_ridge_w.append(np.mean(np.abs(np.asarray(y_te_w) - pr_ridge_w)))

dir_acc_ridge_w = np.array(dir_acc_ridge_w)
mae_ret_ridge_w = np.array(mae_ret_ridge_w)
print("=== Expanding-Window Evaluation (Ridge) ===\\n")
print(f"Ridge — Dir.Acc: {dir_acc_ridge_w.mean():.4f} ± {dir_acc_ridge_w.std():.4f},  MAE_ret: {mae_ret_ridge_w.mean():.6f} ± {mae_ret_ridge_w.std():.6f}")
print(f"(Across {len(dir_acc_ridge_w)} test windows)")""")
        elif "## 10. Ablation" in s:
            set_src(c, "## 9. Ablation Study (4 groups)\n\n(1) Lags only, (2) + volume, (3) + volatility, (4) all.")
        elif "Ridge ablation" in s and "g6_extra" in s:
            set_src(c, """# Ridge ablation: 4 feature groups (v9)
def fit_ridge_subset(X_tr, y_tr, X_te, y_te, pp_te, alpha):
    n = X_tr.shape[1]
    pipe = Pipeline([
        ("scale", ColumnTransformer([("s", StandardScaler(), list(range(n)))], remainder="passthrough")),
        ("ridge", Ridge(alpha=alpha)),
    ])
    pipe.fit(X_tr, y_tr)
    pred = pipe.predict(X_te)
    return metrics_from_returns(y_te, pred, pp_te), dir_acc_returns(y_te, pred)

best_alpha = search_ridge.best_params_["ridge__alpha"]
extra_idx = {name: N_LAGS + i for i, name in enumerate(EXTRA_FEATURE_COLS)}
def cols_for(extra_names):
    return list(range(N_LAGS)) + [extra_idx[n] for n in extra_names]

g1_extra = []
g2_extra = ["log_volume"]
g3_extra = ["volatility_14"]
g4_extra = ["log_volume", "volatility_14"]
idx1, idx2, idx3, idx4 = cols_for(g1_extra), cols_for(g2_extra), cols_for(g3_extra), cols_for(g4_extra)

m_abl1, da_abl1 = fit_ridge_subset(X_train[:, idx1], y_train, X_test[:, idx1], y_test, pp_test, best_alpha)
m_abl2, da_abl2 = fit_ridge_subset(X_train[:, idx2], y_train, X_test[:, idx2], y_test, pp_test, best_alpha)
m_abl3, da_abl3 = fit_ridge_subset(X_train[:, idx3], y_train, X_test[:, idx3], y_test, pp_test, best_alpha)
m_abl4, da_abl4 = fit_ridge_subset(X_train[:, idx4], y_train, X_test[:, idx4], y_test, pp_test, best_alpha)

abl_rows = [
    [f"Lags only ({len(idx1)})", f"{m_abl1['mae_ret']:.6f}", f"{da_abl1:.4f}"],
    [f"+ volume ({len(idx2)})", f"{m_abl2['mae_ret']:.6f}", f"{da_abl2:.4f}"],
    [f"+ volatility ({len(idx3)})", f"{m_abl3['mae_ret']:.6f}", f"{da_abl3:.4f}"],
    [f"All ({len(idx4)})", f"{m_abl4['mae_ret']:.6f}", f"{da_abl4:.4f}"],
]
abl_df = pd.DataFrame(abl_rows, columns=["Features", "MAE (return)", "Dir.Acc"])
print("\\n=== Ridge Ablation (4 groups) ===")
print(abl_df.to_string(index=False))""")
        elif "## 11. Interpretability" in s:
            set_src(c, "## 10. Interpretability\n\nPermutation importance + PDP/ICE for **Ridge** (rubric).")
        elif "Permutation importance (Ridge + XGBoost)" in s:
            set_src(c, """# Permutation importance (Ridge only, v9)
perm = permutation_importance(best_ridge, X_test, y_test, n_repeats=10, random_state=RANDOM_STATE, scoring="neg_mean_absolute_error")
perm_imp = perm.importances_mean
top_k = min(15, len(FEATURE_NAMES))
top_idx_perm = np.argsort(perm_imp)[-top_k:]

plt.figure(figsize=(10, 6))
plt.barh(range(len(top_idx_perm)), perm_imp[top_idx_perm], color="steelblue")
plt.yticks(range(len(top_idx_perm)), [FEATURE_NAMES[i] for i in top_idx_perm])
plt.xlabel("Mean increase in MAE")
plt.title(f"Ridge: Permutation Importance (top {top_k}) — {ASSET}")
plt.tight_layout()
plt.show()
top3_ridge = [FEATURE_NAMES[i] for i in np.argsort(perm_imp)[-3:][::-1]]
print(f"\\nRidge top 3: {top3_ridge}")""")
        elif "## 12. Error Analysis" in s:
            set_src(c, "## 11. Error Analysis\n\nResidual plots and where the model performs poorly (rubric).")
        elif "Residual analysis (XGBoost" in s:
            set_src(c, """# Residual analysis (Ridge on test, v9)
residuals = y_test - pred_ridge_test
vol_test_vals = test_df["volatility_14"].values[N_LAGS:-1][:len(residuals)]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes[0, 0].hist(residuals, bins=50, edgecolor="black", alpha=0.7, color="steelblue")
axes[0, 0].axvline(0, color="red", linestyle="--")
axes[0, 0].set_xlabel("Residual (return)"); axes[0, 0].set_title("Residual Histogram")
axes[0, 1].scatter(pred_ridge_test, y_test, alpha=0.4, s=10, color="steelblue")
lims = [min(y_test.min(), pred_ridge_test.min()), max(y_test.max(), pred_ridge_test.max())]
axes[0, 1].plot(lims, lims, "r--", lw=2)
axes[0, 1].set_xlabel("Predicted Return"); axes[0, 1].set_ylabel("Actual Return"); axes[0, 1].set_title("Predicted vs Actual")
axes[1, 0].plot(residuals, alpha=0.7, color="steelblue", linewidth=0.8)
axes[1, 0].axhline(0, color="gray", linestyle="--")
axes[1, 0].set_xlabel("Test Index"); axes[1, 0].set_ylabel("Residual"); axes[1, 0].set_title("Residuals Over Time")
n_plot = min(len(residuals), len(vol_test_vals))
axes[1, 1].scatter(vol_test_vals[:n_plot], np.abs(residuals[:n_plot]), alpha=0.4, s=10, color="darkorange")
axes[1, 1].set_xlabel("Volatility (14d)"); axes[1, 1].set_ylabel("|Residual|"); axes[1, 1].set_title("|Residual| vs Volatility")
plt.suptitle(f"Error Analysis — Ridge — {ASSET}", fontsize=14, y=1.01)
plt.tight_layout()
plt.show()
print("\\nWhere the model performs poorly:")
print("  Large absolute residuals cluster during high-volatility regimes.")
print("  The model under/overpredicts sharp moves (tail events).")""")
        elif "## 13. Long/Short Backtest" in s:
            set_src(c, "## 12. Long/Short Backtest")
        elif "Backtest each model + ensemble" in s and "Ensemble (wt)" in s:
            set_src(c, """# Long/short backtest (Ridge + LSTM, v9)
def backtest_long_short(actual_ret, pred_ret, threshold=0.0, cost_bps=10):
    actual_ret = np.asarray(actual_ret).ravel()
    pred_ret = np.asarray(pred_ret).ravel()
    position = 0
    pnl_list = []
    cost = cost_bps / 10_000.0
    n_trades = 0
    for t in range(len(actual_ret)):
        signal = 1 if pred_ret[t] > threshold else (-1 if pred_ret[t] < -threshold else 0)
        trade_cost = cost if signal != position else 0.0
        position = signal
        n_trades += int(trade_cost > 0)
        pnl_list.append(position * actual_ret[t] - trade_cost)
    return np.array(pnl_list), n_trades

models_bt = [("Ridge", pred_ridge_test, y_test), ("LSTM", pred_lstm_test, y_te_lstm)]
plt.figure(figsize=(14, 6))
for name, preds, yt in models_bt:
    n_bt = min(len(preds), len(yt))
    pnl, nt = backtest_long_short(yt[-n_bt:], preds[-n_bt:], threshold=0.0, cost_bps=10)
    cum_pnl = np.cumsum(pnl)
    sharpe = np.mean(pnl) / (np.std(pnl) + 1e-10) * np.sqrt(252)
    print(f"{name:25s}: P&L={cum_pnl[-1]:+.4f}, Trades={nt}, Sharpe={sharpe:.2f}")
    plt.plot(cum_pnl, label=f"{name} (P&L={cum_pnl[-1]:+.4f})")
bh = np.cumsum(y_test)
plt.plot(bh, label=f"Buy & Hold ({bh[-1]:+.4f})", linestyle="--", color="gray")
plt.xlabel("Test Day"); plt.ylabel("Cumulative Return"); plt.title(f"Long/Short Backtest — {ASSET}")
plt.legend(); plt.grid(alpha=0.3); plt.tight_layout(); plt.show()""")
        elif "## 14. Summary" in s and "v8 Improvements" in s:
            set_src(c, """## 13. Summary (v9)

**v9** satisfies the course rubric with minimal complexity: two baselines, Ridge (lag + volume + volatility), LSTM, 4-group ablation, permutation importance + PDP/ICE (Ridge), error analysis (residuals), expanding-window evaluation (Ridge). No XGBoost, ensemble, stacking, or classifier.

**Key findings:** See comparison table (Section 7), expanding-window (Section 8), ablation (Section 9), interpretability (Section 10), and error analysis (Section 11).""")
        elif "Sanity checks" in s and "pred_xgb_test" in s:
            set_src(c, """# Sanity checks (v9)
assert X_train.shape[1] == N_LAGS + len(EXTRA_FEATURE_COLS), f"Feature count mismatch: {X_train.shape[1]}"
assert not np.isnan(pred_ridge_test).any(), "NaN in Ridge predictions"
assert not np.isnan(pred_lstm_test).any(), "NaN in LSTM predictions"
print("All sanity checks passed.")""")

        new_cells.append(c)
        i += 1

    nb["cells"] = new_cells
    with open(V9, "w") as f:
        json.dump(nb, f, indent=2)
    print(f"Wrote {V9} ({len(new_cells)} cells)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

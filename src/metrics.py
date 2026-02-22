"""Metrics for crypto price prediction: MAE, RMSE, directional accuracy."""
import numpy as np


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Compute MAE, RMSE, and directional accuracy. Reuse for all models."""
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    n = len(y_true)
    if n != len(y_pred) or n == 0:
        raise ValueError("y_true and y_pred must have same non-zero length")

    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))

    # Directional: correct when (y_true[t] - y_true[t-1]) and (y_pred[t] - y_true[t-1]) have same sign
    # For next-day prediction: direction correct if (y_true[t] > y_true[t-1]) == (y_pred[t] > y_true[t-1])
    # We need true direction vs predicted direction; we have y_pred for "next", so direction_pred = y_pred > y_prev
    # and direction_true = y_true > y_prev. So we need y_prev = price the day before each target.
    # Simpler: direction correct if sign(y_true[t] - y_true[t-1]) == sign(y_pred[t] - y_true[t-1])
    # So we need y_true and a lagged version. For a single (y_true, y_pred) we don't have prev; assume caller passes
    # aligned arrays where indices match. So directional = sign(y_true[1:] - y_true[:-1]) == sign(y_pred[1:] - y_true[:-1])
    if n > 1:
        true_dir = np.sign(np.diff(y_true))
        pred_dir = np.sign(y_pred[1:] - y_true[:-1])
        dir_acc = np.mean(true_dir == pred_dir)
    else:
        dir_acc = np.nan

    return {"mae": float(mae), "rmse": float(rmse), "directional_accuracy": float(dir_acc)}

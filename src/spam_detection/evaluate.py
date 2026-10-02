"""Metrics shared by model comparison, final evaluation, and reporting."""

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def classification_metrics(model: Any, features: Any, labels: Any) -> dict[str, Any]:
    """Return supporting metrics with spam (1) as the positive class."""
    predictions = model.predict(features)
    probabilities = (
        model.predict_proba(features)[:, 1] if hasattr(model, "predict_proba") else None
    )
    return {
        "accuracy": float(accuracy_score(labels, predictions)),
        "spam_precision": float(precision_score(labels, predictions, zero_division=0)),
        "spam_recall": float(recall_score(labels, predictions, zero_division=0)),
        "spam_f1": float(f1_score(labels, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(labels, probabilities))
        if probabilities is not None
        else float("nan"),
        "confusion_matrix": confusion_matrix(labels, predictions).tolist(),
    }


def summarize_cv_scores(scores: dict[str, np.ndarray]) -> dict[str, dict[str, float]]:
    """Summarize fold-level scores as mean and standard deviation."""
    return {
        metric: {"mean": float(values.mean()), "std": float(values.std(ddof=1))}
        for metric, values in scores.items()
    }

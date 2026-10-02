"""Evaluate the already-selected model once on the untouched test split."""

import json

import joblib

from .config import MODELS_DIR
from .data import load_dataset, remove_duplicate_rows, split_dataset
from .evaluate import classification_metrics


def evaluate_saved_model() -> dict:
    """Load the saved winner and write its one-time test metrics."""
    frame = load_dataset()
    cleaned, _ = remove_duplicate_rows(frame)
    _, test_x, _, test_y = split_dataset(cleaned)
    model = joblib.load(MODELS_DIR / "spam_detector.joblib")
    metrics = classification_metrics(model, test_x, test_y)
    (MODELS_DIR / "final_test_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    return metrics


if __name__ == "__main__":
    print(json.dumps(evaluate_saved_model(), indent=2))

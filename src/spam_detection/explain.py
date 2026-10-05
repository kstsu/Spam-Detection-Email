"""Held-out permutation explanations for the selected spam detector."""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import f1_score

from .config import MODELS_DIR, RANDOM_STATE, feature_columns
from .data import load_dataset, remove_duplicate_rows, split_dataset


def _group_columns(columns: list[str]) -> dict[str, list[str]]:
    """Return feature-family columns using the shared prefix definitions."""
    return {
        "words": feature_columns(columns, "words"),
        "symbols": feature_columns(columns, "symbols"),
        "capitals": feature_columns(columns, "capitals"),
    }


def calculate_permutation_importance(
    model: object,
    test_features: pd.DataFrame,
    test_labels: pd.Series,
    repeats: int = 10,
) -> dict[str, object]:
    """Calculate individual and grouped F1 importance on the held-out test set.

    This is an explanation step performed after model selection. It does not
    alter the selected model or feed information back into training.
    """
    individual = permutation_importance(
        model,
        test_features,
        test_labels,
        scoring="f1",
        n_repeats=repeats,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    individual_results = [
        {
            "feature": column,
            "mean_f1_decrease": float(mean),
            "std_f1_decrease": float(std),
        }
        for column, mean, std in zip(
            test_features.columns,
            individual.importances_mean,
            individual.importances_std,
            strict=True,
        )
    ]
    individual_results.sort(
        key=lambda result: result["mean_f1_decrease"], reverse=True
    )

    baseline = float(f1_score(test_labels, model.predict(test_features)))
    grouped_results = []
    for group, columns in _group_columns(test_features.columns.tolist()).items():
        permuted = test_features.copy()
        values = permuted[columns].to_numpy(copy=True)
        permutation = pd.Series(range(len(permuted))).sample(
            frac=1, random_state=RANDOM_STATE
        ).to_numpy()
        permuted.loc[:, columns] = values[permutation]
        score = float(f1_score(test_labels, model.predict(permuted)))
        grouped_results.append(
            {
                "feature_group": group,
                "mean_f1_decrease": baseline - score,
                "permuted_f1": score,
            }
        )
    grouped_results.sort(
        key=lambda result: result["mean_f1_decrease"], reverse=True
    )
    return {
        "metric": "spam_f1",
        "repeats": repeats,
        "baseline_f1": baseline,
        "individual": individual_results,
        "grouped": grouped_results,
    }


def explain_saved_model(
    output_path: Path = MODELS_DIR / "feature_importance.json",
) -> dict[str, object]:
    """Explain the saved model against the same held-out split used for testing."""
    frame = load_dataset()
    cleaned, _ = remove_duplicate_rows(frame)
    _, test_features, _, test_labels = split_dataset(cleaned)
    model = joblib.load(MODELS_DIR / "spam_detector.joblib")
    results = calculate_permutation_importance(model, test_features, test_labels)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


if __name__ == "__main__":
    print(json.dumps(explain_saved_model(), indent=2))

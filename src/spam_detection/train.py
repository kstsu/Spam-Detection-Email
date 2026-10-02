"""Train, compare, and save the final model without using the test set for selection."""

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedKFold

from .config import CV_FOLDS, MODELS_DIR, RANDOM_STATE, feature_columns
from .data import load_dataset, remove_duplicate_rows, split_dataset
from .pipeline import MODEL_NAMES, build_pipeline

PRIMARY_METRIC = "f1"


def compare_models(
    train_features: pd.DataFrame, train_labels: pd.Series
) -> tuple[dict, str]:
    """Tune the three approved models on training folds and select by spam F1."""
    folds = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    grids = {
        "logistic_regression": {"model__C": [0.1, 1.0, 10.0]},
        "naive_bayes": {"model__var_smoothing": [1e-9, 1e-8, 1e-7]},
        "random_forest": {
            "model__max_features": ["sqrt", 0.5],
            "model__min_samples_leaf": [1, 2],
        },
    }
    results = {}
    for model_name in MODEL_NAMES:
        search = GridSearchCV(
            build_pipeline(model_name),
            grids[model_name],
            scoring=PRIMARY_METRIC,
            cv=folds,
            n_jobs=-1,
            return_train_score=False,
        )
        search.fit(train_features, train_labels)
        results[model_name] = {
            "best_params": search.best_params_,
            "cv_f1_mean": float(search.best_score_),
            "cv_f1_std": float(
                search.cv_results_["std_test_score"][search.best_index_]
            ),
            "estimator": search.best_estimator_,
        }
    selected = max(results, key=lambda name: results[name]["cv_f1_mean"])
    return results, selected


def train_and_save(output_dir: Path = MODELS_DIR) -> dict:
    """Run model selection, fit the winner on training data, and save artifacts."""
    frame = load_dataset()
    cleaned, report = remove_duplicate_rows(frame)
    train_x, test_x, train_y, test_y = split_dataset(cleaned)
    results, selected = compare_models(train_x, train_y)
    final_model = results[selected]["estimator"]
    output_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_model, output_dir / "spam_detector.joblib")
    serializable = {
        name: {key: value for key, value in result.items() if key != "estimator"}
        for name, result in results.items()
    }
    metadata = {
        "selected_model": selected,
        "primary_metric": "spam_f1",
        "duplicate_report": report.__dict__,
        "train_rows": len(train_x),
        "test_rows": len(test_x),
        "train_class_counts": train_y.value_counts().to_dict(),
        "test_class_counts": test_y.value_counts().to_dict(),
        "comparison": serializable,
        "feature_columns": feature_columns(frame.columns.tolist()),
    }
    (output_dir / "training_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=MODELS_DIR)
    args = parser.parse_args()
    print(json.dumps(train_and_save(args.output_dir), indent=2))

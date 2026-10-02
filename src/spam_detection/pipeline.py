"""The exactly-three permitted model pipelines used by training and the app."""

from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_NAMES = ("logistic_regression", "naive_bayes", "random_forest")


def build_pipeline(model_name: str, class_weight: str | None = "balanced") -> Pipeline:
    """Build one of the three approved traditional ML pipelines."""
    if model_name == "logistic_regression":
        estimator: Any = LogisticRegression(
            class_weight=class_weight, max_iter=2000, random_state=42
        )
        scaler: Any = StandardScaler()
    elif model_name == "naive_bayes":
        estimator = GaussianNB()
        scaler = StandardScaler()
    elif model_name == "random_forest":
        estimator = RandomForestClassifier(
            class_weight=class_weight, n_estimators=300, random_state=42, n_jobs=-1
        )
        scaler = "passthrough"
    else:
        raise ValueError(f"Unknown model: {model_name}. Choose from {MODEL_NAMES}.")
    return Pipeline([("scaler", scaler), ("model", estimator)])

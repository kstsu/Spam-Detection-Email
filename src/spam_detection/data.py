"""Loading, validation, duplicate handling, and reproducible data splitting."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from .config import (
    DATA_PATH,
    POSITIVE_LABEL,
    RANDOM_STATE,
    TARGET_COLUMN,
    TEST_SIZE,
    feature_columns,
)


@dataclass(frozen=True)
class DatasetReport:
    """Auditable facts about the loaded and cleaned dataset."""

    input_rows: int
    duplicate_rows: int
    conflicting_duplicate_groups: int
    output_rows: int


def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load and validate the numeric Spambase CSV."""
    frame = pd.read_csv(path)
    columns = feature_columns(frame.columns.tolist())
    if len(columns) != 57:
        raise ValueError(f"Expected 57 feature columns, found {len(columns)}")
    if TARGET_COLUMN not in frame.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")
    if frame[columns].isna().any().any():
        raise ValueError("Feature values must not contain missing values")
    if not set(frame[TARGET_COLUMN].unique()).issubset({"spam", "not_spam"}):
        raise ValueError("Labels must be 'spam' or 'not_spam'")
    if (frame[columns] < 0).any().any():
        raise ValueError("Frequency and run-length features cannot be negative")
    return frame


def remove_duplicate_rows(
    frame: pd.DataFrame,
) -> tuple[pd.DataFrame, DatasetReport]:
    """Remove exact duplicate records, retaining the first occurrence.

    Conflicting labels are counted before removal so the policy is visible in
    the experiment log rather than silently changing the data.
    """
    duplicate_rows = int(frame.duplicated().sum())
    conflicting_groups = int(
        frame.groupby(feature_columns(frame.columns.tolist()), dropna=False)[
            TARGET_COLUMN
        ]
        .nunique()
        .gt(1)
        .sum()
    )
    cleaned = frame.drop_duplicates(keep="first").reset_index(drop=True)
    report = DatasetReport(
        input_rows=len(frame),
        duplicate_rows=duplicate_rows,
        conflicting_duplicate_groups=conflicting_groups,
        output_rows=len(cleaned),
    )
    return cleaned, report


def split_dataset(
    frame: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Create the required stratified 80/20 train/test split."""
    columns = feature_columns(frame.columns.tolist())
    labels = (frame[TARGET_COLUMN] == POSITIVE_LABEL).astype(int)
    train_features, test_features, train_labels, test_labels = train_test_split(
        frame[columns],
        labels,
        test_size=TEST_SIZE,
        stratify=labels,
        random_state=RANDOM_STATE,
    )
    return train_features, test_features, train_labels, test_labels

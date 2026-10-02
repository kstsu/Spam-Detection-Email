"""Shared project configuration and feature-group definitions."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
ORIGINAL_DATA_DIR = DATA_DIR / "original"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"

DATA_PATH = ORIGINAL_DATA_DIR / "spam_all.csv"
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
TARGET_COLUMN = "label"
POSITIVE_LABEL = "spam"

FEATURE_GROUP_PREFIXES = {
    "words": "word_freq_",
    "symbols": "char_freq_",
    "capitals": "capital_run_length_",
}


def feature_columns(columns: list[str], group: str = "all") -> list[str]:
    """Return feature columns for one family or for all families."""
    if group == "all":
        prefixes = tuple(FEATURE_GROUP_PREFIXES.values())
    elif group in FEATURE_GROUP_PREFIXES:
        prefixes = (FEATURE_GROUP_PREFIXES[group],)
    else:
        raise ValueError(f"Unknown feature group: {group}")
    return [column for column in columns if column.startswith(prefixes)]

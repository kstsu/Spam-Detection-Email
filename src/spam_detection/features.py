"""Feature-group helpers and approximate Spambase-style text extraction."""

import re

import pandas as pd

from .config import feature_columns

WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
CAPITAL_RUN_PATTERN = re.compile(r"[A-Z]+")


def text_to_features(text: str, columns: list[str] | None = None) -> pd.DataFrame:
    """Convert pasted email text into one approximate Spambase feature row."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Email text must not be empty")
    columns = columns or _default_feature_columns()
    words = WORD_PATTERN.findall(text.lower())
    word_count = max(len(words), 1)
    character_count = max(len(text), 1)
    values: dict[str, float] = {}
    for column in columns:
        if column.startswith("word_freq_"):
            term = column.removeprefix("word_freq_")
            values[column] = 100.0 * sum(word == term for word in words) / word_count
        elif column.startswith("char_freq_"):
            character = column.removeprefix("char_freq_")
            values[column] = 100.0 * text.count(character) / character_count
        elif column == "capital_run_length_average":
            runs = [len(run) for run in CAPITAL_RUN_PATTERN.findall(text)]
            values[column] = float(sum(runs) / len(runs)) if runs else 0.0
        elif column == "capital_run_length_longest":
            values[column] = float(
                max((len(run) for run in CAPITAL_RUN_PATTERN.findall(text)), default=0)
            )
        elif column == "capital_run_length_total":
            values[column] = float(
                sum(len(run) for run in CAPITAL_RUN_PATTERN.findall(text))
            )
        else:
            raise ValueError(f"Unsupported feature column: {column}")
    return pd.DataFrame([values], columns=columns)


def validate_feature_frame(
    frame: pd.DataFrame, columns: list[str] | None = None
) -> pd.DataFrame:
    """Validate and return a numeric feature frame in the training column order."""
    columns = columns or _default_feature_columns()
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")
    values = frame.loc[:, columns].apply(pd.to_numeric, errors="coerce")
    if values.isna().any().any():
        raise ValueError("All feature values must be numeric and non-empty")
    if (values < 0).any().any():
        raise ValueError("Feature values cannot be negative")
    frequency_columns = [
        column for column in columns if column.startswith(("word_freq_", "char_freq_"))
    ]
    if (values[frequency_columns] > 100).any().any():
        raise ValueError("Word and character frequencies must be between 0 and 100")
    return values


def _default_feature_columns() -> list[str]:
    return feature_columns(
        [
            "word_freq_make",
            "word_freq_address",
            "word_freq_all",
            "word_freq_3d",
            "word_freq_our",
            "word_freq_over",
            "word_freq_remove",
            "word_freq_internet",
            "word_freq_order",
            "word_freq_mail",
            "word_freq_receive",
            "word_freq_will",
            "word_freq_people",
            "word_freq_report",
            "word_freq_addresses",
            "word_freq_free",
            "word_freq_business",
            "word_freq_email",
            "word_freq_you",
            "word_freq_credit",
            "word_freq_your",
            "word_freq_font",
            "word_freq_000",
            "word_freq_money",
            "word_freq_hp",
            "word_freq_hpl",
            "word_freq_george",
            "word_freq_650",
            "word_freq_lab",
            "word_freq_labs",
            "word_freq_telnet",
            "word_freq_857",
            "word_freq_data",
            "word_freq_415",
            "word_freq_85",
            "word_freq_technology",
            "word_freq_1999",
            "word_freq_parts",
            "word_freq_pm",
            "word_freq_direct",
            "word_freq_cs",
            "word_freq_meeting",
            "word_freq_original",
            "word_freq_project",
            "word_freq_re",
            "word_freq_edu",
            "word_freq_table",
            "word_freq_conference",
            "char_freq_;",
            "char_freq_(",
            "char_freq_[",
            "char_freq_!",
            "char_freq_$",
            "char_freq_#",
            "capital_run_length_average",
            "capital_run_length_longest",
            "capital_run_length_total",
        ],
    )

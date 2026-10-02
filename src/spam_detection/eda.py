"""Generate the required, decision-oriented EDA figures and summary."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .config import PROCESSED_DATA_DIR, feature_columns
from .data import load_dataset, remove_duplicate_rows


def run_eda(output_dir: Path = PROCESSED_DATA_DIR / "eda") -> list[str]:
    """Write five readable figures, cleaned data, and findings text."""
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = load_dataset()
    data, report = remove_duplicate_rows(raw)
    columns = feature_columns(data.columns.tolist())
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    data.to_csv(PROCESSED_DATA_DIR / "spam_cleaned.csv", index=False)
    sns.set_theme(style="whitegrid")
    findings: list[str] = []

    plt.figure(figsize=(6, 4))
    sns.countplot(data=data, x="label", order=["not_spam", "spam"])
    plt.title("Class distribution after duplicate removal")
    plt.tight_layout()
    plt.savefig(output_dir / "01_class_distribution.png", dpi=160)
    plt.close()
    findings.append(
        "The cleaned data remains mildly imbalanced, so stratification and spam-class F1 are used."
    )

    family_means = pd.Series(
        {
            "words": data.filter(like="word_freq_").to_numpy().mean(),
            "symbols": data.filter(like="char_freq_").to_numpy().mean(),
            "capitals": data.filter(like="capital_run_length_").to_numpy().mean(),
        }
    )
    plt.figure(figsize=(7, 4))
    family_means.plot(kind="bar", color=["#2f6690", "#3caea3", "#f6ae2d"])
    plt.ylabel("Mean feature value in native units")
    plt.title("Average signal by feature family")
    plt.tight_layout()
    plt.savefig(output_dir / "02_feature_family_means.png", dpi=160)
    plt.close()
    findings.append(
        "Feature families use different units and scales, supporting scaling inside the linear and probabilistic pipelines."
    )

    class_means = data.groupby("label")[columns].mean().T
    top_columns = (
        (class_means["spam"] - class_means["not_spam"]).abs().nlargest(10).index
    )
    plt.figure(figsize=(8, 5))
    class_means.loc[top_columns].sort_values("spam").plot(kind="barh", figsize=(8, 5))
    plt.xlabel("Mean feature value")
    plt.title("Ten features with largest class-mean differences")
    plt.tight_layout()
    plt.savefig(output_dir / "03_top_class_differences.png", dpi=160)
    plt.close()
    findings.append(
        "Several word and symbol features differ substantially by class, motivating content-plus-symbol inputs."
    )

    correlation_columns = list(top_columns) + ["capital_run_length_total"]
    plt.figure(figsize=(9, 7))
    sns.heatmap(data[correlation_columns].corr(), cmap="vlag", center=0)
    plt.title("Correlation among discriminative and capital features")
    plt.tight_layout()
    plt.savefig(output_dir / "04_feature_correlations.png", dpi=160)
    plt.close()
    findings.append(
        "Correlated feature groups are present, so model comparison includes both a linear model and a tree ensemble."
    )

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=data, x="label", y="capital_run_length_total", showfliers=False)
    plt.yscale("log")
    plt.title("Capital-run total by class (log scale; extreme points hidden)")
    plt.ylabel("Capital run total, log scale")
    plt.tight_layout()
    plt.savefig(output_dir / "05_capital_outliers.png", dpi=160)
    plt.close()
    findings.append(
        "Capital totals are strongly skewed; extreme values are retained as potentially legitimate email style rather than deleted without evidence."
    )

    summary = [
        "# EDA Findings",
        "",
        f"Raw rows: {report.input_rows}; exact duplicate rows removed: {report.duplicate_rows}; conflicting duplicate groups: {report.conflicting_duplicate_groups}; cleaned rows: {report.output_rows}.",
        "",
    ] + [f"- {finding}" for finding in findings]
    (output_dir / "findings.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    return findings


if __name__ == "__main__":
    run_eda()

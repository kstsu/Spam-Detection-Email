from spam_detection.pipeline import MODEL_NAMES, build_pipeline
from spam_detection.train import run_feature_ablation


def test_exactly_three_approved_models_are_exposed() -> None:
    assert set(MODEL_NAMES) == {"logistic_regression", "naive_bayes", "random_forest"}
    for model_name in MODEL_NAMES:
        pipeline = build_pipeline(model_name)
        assert pipeline.steps[-1][0] == "model"


def test_feature_ablation_has_required_groups() -> None:
    import pandas as pd

    features = pd.DataFrame(
        {
            "word_freq_a": [0.0, 1.0, 0.0, 1.0, 0.0],
            "char_freq_!": [0.0, 0.0, 1.0, 1.0, 0.0],
            "capital_run_length_total": [0.0, 1.0, 2.0, 3.0, 4.0],
        }
    )
    features = pd.concat([features, features], ignore_index=True)
    labels = pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    results = run_feature_ablation(features, labels)
    assert set(results) == {
        "all",
        "words",
        "symbols",
        "capitals",
        "words_symbols",
        "words_capitals",
    }

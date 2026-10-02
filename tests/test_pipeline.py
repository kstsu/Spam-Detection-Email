from spam_detection.pipeline import MODEL_NAMES, build_pipeline


def test_exactly_three_approved_models_are_exposed() -> None:
    assert set(MODEL_NAMES) == {"logistic_regression", "naive_bayes", "random_forest"}
    for model_name in MODEL_NAMES:
        pipeline = build_pipeline(model_name)
        assert pipeline.steps[-1][0] == "model"

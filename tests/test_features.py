import pytest

from spam_detection.features import text_to_features, validate_feature_frame


def test_text_features_have_expected_shape_and_capital_statistics() -> None:
    features = text_to_features("FREE MONEY!!! BUY NOW ABCD")
    assert features.shape == (1, 57)
    assert features.loc[0, "word_freq_free"] > 0
    assert features.loc[0, "char_freq_!"] > 0
    assert features.loc[0, "capital_run_length_longest"] == 5


def test_feature_validation_rejects_bad_values() -> None:
    valid_features = text_to_features("A valid message")
    with pytest.raises(ValueError, match="negative"):
        validate_feature_frame(valid_features.assign(word_freq_make=-1))

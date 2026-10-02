from spam_detection.config import feature_columns
from spam_detection.data import load_dataset, remove_duplicate_rows, split_dataset


def test_dataset_contract_and_duplicate_policy() -> None:
    frame = load_dataset()
    assert len(feature_columns(frame.columns.tolist())) == 57
    cleaned, report = remove_duplicate_rows(frame)
    assert report.duplicate_rows == 391
    assert report.output_rows == 4210
    assert len(cleaned) == 4210


def test_split_is_stratified_and_reproducible() -> None:
    cleaned, _ = remove_duplicate_rows(load_dataset())
    train_x, test_x, train_y, test_y = split_dataset(cleaned)
    assert len(train_x) == 3368
    assert len(test_x) == 842
    assert abs(train_y.mean() - test_y.mean()) < 0.001

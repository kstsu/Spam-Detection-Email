# Spam Detection Email: Technical Documentation

## Project Information

| Item | Value |
|---|---|
| Group | [PLACEHOLDER] |
| Course | [PLACEHOLDER] |
| Instructor | [PLACEHOLDER] |
| Deadline | [PLACEHOLDER] |
| Repository | https://github.com/kstsu/Spam-Detection-Email |
| Deployed application | [PLACEHOLDER] |

## 1. Problem and Intended Use

This project classifies an email as `spam` or `not_spam` using the UCI Spambase dataset. The intended user is a person or small team that wants a second opinion about a message. The model is not an automatic mailbox filter and should not be treated as a final decision-maker.

Spam detection is suitable for supervised machine learning because the dataset provides labeled examples and spam is represented by multiple weak signals rather than one reliable rule. A false positive can hide a legitimate email, while a false negative allows spam into the inbox. The primary metric is therefore spam-class F1, which balances spam precision and recall.

## 2. Data

The dataset contains 4,601 email records, 57 numeric features, and one target label. There are 2,788 `not_spam` records and 1,813 `spam` records. The feature families are:

- 48 `word_freq_` columns: percentages of words matching listed terms.
- 6 `char_freq_` columns: percentages of characters matching `;`, `(`, `[`, `!`, `$`, and `#`.
- 3 `capital_run_length_` columns: average, longest, and total consecutive-capital run lengths.

The source files are preserved in `data/original/`. Their provenance and remaining source information are recorded in `data/original/SOURCE.md`. License confirmation remains `[PLACEHOLDER]` until the group confirms the applicable UCI terms.

### Data quality actions

| Check | Finding | Action |
|---|---|---|
| Missing values | None in the original feature matrix | No imputation required |
| Invalid labels | No labels outside `spam` and `not_spam` | Validation rejects unexpected labels |
| Negative values | None | Validation rejects negative values |
| Exact duplicates | 391 rows | Remove duplicates before splitting, retain first occurrence |
| Conflicting duplicate groups | 3 groups in the full dataset | Count and report them; apply the deterministic first-occurrence policy |
| Capital outliers | Strongly right-skewed totals | Retain as potentially legitimate email style; inspect on a log-scale plot |

After duplicate removal, 4,210 rows remain. The data is split once into 3,368 training rows and 842 test rows using an 80/20 stratified split with random state 42.

## 3. Exploratory Data Analysis

The reproducible EDA command is:

```powershell
$env:PYTHONPATH = "src"
python -m spam_detection.eda
```

It writes figures and findings to `data/processed/eda/`:

1. `01_class_distribution.png`: confirms mild class imbalance and motivates stratification and spam F1.
2. `02_feature_family_means.png`: shows that feature families use different native scales and motivates pipeline scaling where appropriate.
3. `03_top_class_differences.png`: shows word and symbol features with the largest class-mean differences.
4. `04_feature_correlations.png`: shows relationships among discriminative features and supports comparing linear and nonlinear models.
5. `05_capital_outliers.png`: shows the skewed capital-total distribution and supports retaining extreme values pending evidence of data error.

The written interpretation is in `data/processed/eda/findings.md`.

## 4. Preprocessing and Experimental Design

All duplicate handling occurs before the split. Model preprocessing is inside each scikit-learn `Pipeline`, so transformations are fitted only on the relevant training folds. Logistic Regression and Gaussian Naive Bayes use `StandardScaler`; Random Forest uses the original numeric scale. No synthetic oversampling is used. Stratification is used for both the train/test split and the five cross-validation folds.

The three compared algorithms are exactly:

1. Logistic Regression
2. Gaussian Naive Bayes
3. Random Forest

The comparison uses the same training partition, folds, primary metric, and feature set. Hyperparameter search is restricted to the training partition.

## 5. Model Comparison and Selection

| Model | Best settings | Mean spam F1 | Standard deviation |
|---|---|---:|---:|
| Logistic Regression | `C=10.0` | 0.906 | 0.019 |
| Gaussian Naive Bayes | `var_smoothing=1e-8` | 0.812 | 0.017 |
| Random Forest | `max_features=sqrt`, `min_samples_leaf=1` | 0.935 | 0.016 |

Random Forest was selected because it achieved the highest validation spam F1 and can model nonlinear interactions among word, symbol, and capital features. The saved pipeline is `models/spam_detector.joblib`; its training metadata is `models/training_metadata.json`.

## 6. Final Test Evaluation

The selected model was evaluated once on the untouched test partition after model selection:

| Metric | Result |
|---|---:|
| Accuracy | 0.945 |
| Spam precision | 0.929 |
| Spam recall | 0.935 |
| Spam F1 | 0.932 |
| ROC AUC | 0.989 |

The confusion matrix, using rows as actual classes `[not_spam, spam]` and columns as predicted classes, is:

```text
[[482, 24],
 [ 22, 314]]
```

Thus, 24 legitimate messages were classified as spam and 22 spam messages were classified as legitimate in the held-out test set. The machine-readable result is `models/final_test_metrics.json`.

## 7. Application Guide

Run the app locally from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -m streamlit run app/streamlit_app.py
```

Open `http://localhost:8501`. The app supports:

- **Pasted email text:** approximate the 57 Spambase features from the text.
- **Feature CSV upload:** provide all 57 feature columns using the names in `documentation/DATA_DICTIONARY.md`.

The app displays the predicted class and spam probability. Empty text, missing columns, non-numeric values, negative values, and out-of-range frequency values produce an understandable error. The text route is an approximation because the original email text and exact original tokenization are unavailable.

## 8. Reproducibility

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
python -m spam_detection.eda
python -m spam_detection.train
python -m spam_detection.final_evaluation
python -m pytest -q
```

The exact dependency versions should be pinned after the final clean-environment run: `[PLACEHOLDER]`.

## 9. Limitations and Responsible Use

- The data comes from the late 1990s and may not represent current spam.
- The model sees engineered numeric features, not original email text.
- The word vocabulary is fixed and cannot discover new spam terms.
- The text-to-feature app path only approximates the original feature extraction.
- The dataset source, mailbox composition, and historical collection process may limit generalization.
- A public deployment URL and deployment configuration are `[PLACEHOLDER]`.

## 10. Troubleshooting

| Problem | Resolution |
|---|---|
| `streamlit` is not recognized | Run `python -m streamlit run app/streamlit_app.py` after installing requirements |
| Model file is missing | Run `python -m spam_detection.train` with `PYTHONPATH=src` |
| Import error for `spam_detection` | Set `$env:PYTHONPATH = "src"` from the repository root |
| CSV rejected | Confirm all 57 feature columns exist, are numeric, non-negative, and frequencies do not exceed 100 |
| Deployment fails | Confirm the deployment host uses the repository root and installs `requirements.txt`; deployment URL: `[PLACEHOLDER]` |
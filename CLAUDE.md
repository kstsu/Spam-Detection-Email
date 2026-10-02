# CLAUDE.md

Guidance for AI assistants (Claude Code, etc.) working in this repository.

**Read in this order:** this file, `README.md` (goals, roadmap), `documentation/PROJECT_REQUIREMENTS.md` (course rules), `documentation/DECISIONS.md` (what is decided vs. open).

## Project in one paragraph

Spam Detection Email is a **course final group project**: an end-to-end *traditional* ML classifier on **Spambase** (4,601 emails, 57 numeric features, 39.4% spam), with strong EDA, a fair comparison of **exactly three** algorithms, a justified final model, and a **Streamlit** app. The research question: does a model need the **content** (word and symbol frequencies) or the **style** (capital-letter measures) to recognise spam? Reproducibility and honest evaluation matter more than a high score.

## Hard rules from the course (never break these)

1. **Exactly three** distinct, permitted algorithms are compared. Different hyperparameters of the same algorithm do not count. A dummy baseline may be reported but is not one of the three.
2. **Forbidden:** neural networks, deep learning (CNN/RNN/transformers), LLMs, pretrained or foundation models, AutoML. Do not suggest, import or add them for the graded comparison.
3. **80/20 stratified split.** All tuning and selection happen **inside the training set** (5-fold stratified CV). The **test set is evaluated once**, after the final model is chosen.
4. **Same split, preprocessing logic, CV folds and primary metric** for all three algorithms.
5. **Fit preprocessing on training data only** (use scikit-learn `Pipeline`).
6. Every EDA figure must lead to a written finding or decision. No decorative charts.
7. The **app and the paper must use the same model and pipeline**.
8. No passwords, API keys, credentials or absolute machine-specific paths in code.
9. Never fabricate or alter results. Every number in the paper must be reproducible from the code.

## Tech stack

| Purpose | Library |
|---|---|
| Language | Python 3.11+, type hints on public functions |
| Data | `pandas`, `numpy` |
| Modelling | `scikit-learn` (pipelines, CV, metrics, permutation importance) |
| Plots | `matplotlib`, `seaborn` |
| App | `streamlit` |
| Model saving | `joblib` |
| Notebooks | `jupyterlab` |
| Tests / lint | `pytest`, `ruff` |

Add dependencies only with a reason, and keep `requirements.txt` accurate (pinned exact versions before submission). **No NLTK/spaCy needed:** Spambase is already numeric; plain Python/regex is enough for the app's text-to-feature step. **No `imbalanced-learn` unless class weights prove insufficient** (see below).

## Repository layout (required by the course; do not rename top-level folders)

```text
app/            Streamlit application
data/original/  untouched dataset + SOURCE.md        (never edit)
data/processed/ cleaned/processed data
notebooks/      01_eda, 02_preprocessing, 03_model_comparison, 04_final_evaluation
src/spam_detection/  config, data, features, pipeline, train, evaluate, explain
models/         saved best model / full pipeline     (committed, not git-ignored)
documentation/  requirements, decisions, data dictionary, experiment log, contributions, screenshots
paper/          final IMRaD paper (DOCX + PDF)
tests/          pytest tests
```

## Data rules

- Columns: `word_freq_*` (48), `char_freq_*` (6), `capital_run_length_*` (3), `label` (`spam`/`not_spam`). Define feature groups **once** in `config.py` by prefix; never hard-code column lists elsewhere.
- Encode `spam = 1`, `not_spam = 0`; spam is the positive class for all metrics.
- **Duplicates:** `spam_all.csv` has 391 exact duplicate rows (979 in `spam_caps.csv`), including a few groups with **conflicting labels** (3 and 34). Decide and document the policy in `DECISIONS.md`, apply it **before** splitting, and report what was removed.
- Log every filter or row drop. Never silently drop data.
- One `RANDOM_STATE = 42` in `config.py`, used by every splitter and model.

## Class imbalance rules

Distribution: **1,813 spam (39.4%) vs. 2,788 not spam (60.6%)**, about 1 : 1.54. This is **mild**.

1. Log the class distribution at the start of every experiment (full data and each split).
2. Always stratify (`train_test_split(..., stratify=y)`, `StratifiedKFold`).
3. Do **not** resample by default. Run the plain model first, then `class_weight="balanced"` where the algorithm supports it. Report both.
4. If resampling is ever used, do it **only inside training folds**, never on validation/test data and never before the split.
5. Prefer class weights and threshold tuning over synthetic oversampling (SMOTE) for frequency features.
6. Tune any decision threshold on validation data, never on the test set.
7. Accuracy alone is **not sufficient**. State the cost of false positives (real email lost) vs. false negatives (spam gets through) and choose the primary metric accordingly.

## Evaluation rules

- Report for **all three** models: the primary metric, accuracy, per-class precision/recall/F1, confusion matrix, ROC AUC where appropriate, as mean ± std across the same CV folds.
- Show the majority-class baseline (60.6% accuracy) next to results.
- Keep validation results and the one-time test result clearly separate.
- Do not claim one model is better unless the gap exceeds fold-to-fold variation.
- Selection weighs performance, interpretability, speed and practical suitability.

## Modelling guidelines

- Proposed algorithms: Random Forest, Logistic Regression, Naive Bayes (confirm in `DECISIONS.md`). Check there before assuming.
- Tree-based models need no scaling; Logistic Regression does (inside the pipeline). Naive Bayes variants have input requirements: check them.
- Impurity-based `feature_importances_` is a quick look only. Confirm with permutation importance on held-out data, including **grouped** permutation by feature family.
- Feature-group experiments (all / words / symbols / capitals / combinations) run under CV on training data only. They vary features, not algorithms.

## App rules

- Load the saved model and the **same pipeline** used in training; never retrain inside the app.
- Inputs: pasted email text (converted to the 57 features with the training definitions) and/or CSV upload with the 57 columns.
- Validate everything: empty, missing columns, non-numeric, negative or out-of-range values must give clear messages, never a crash.
- Show predicted class, spam probability, model name, and a short guide to inputs and outputs.
- Use relative paths only. Test valid, invalid and boundary inputs in `tests/`.

## Coding conventions

- Reusable logic in `src/spam_detection/`; notebooks import from it and stay readable top to bottom.
- Small functions with docstrings and type hints; paths via `pathlib` built from `config.py`.
- Notebooks numbered, runnable from start to finish, outputs small before committing.
- Run `ruff format` and `ruff check` before committing.
- Branch per milestone (`m2-eda`, `m4-comparison`), PR into `main`, short imperative commit messages.

## Documentation habits

- Update the roadmap checkboxes in `README.md` when a milestone completes.
- Add a dated entry to `documentation/EXPERIMENT_LOG.md` for every experiment: question, features, model and settings, CV scheme, results, one-sentence interpretation.
- Record every decision (and reason) in `documentation/DECISIONS.md`.

## Do / Don't

**Do:** state assumptions when a task is ambiguous; keep RQ1 to RQ4 in view; flag leakage risks, duplicates and over-interpretation; point to the rubric when prioritising (EDA is worth the most).

**Don't:** touch the test set before the final model is chosen; fit scalers on the full dataset; report a single lucky split; overwrite `data/original/`; compare more or fewer than three algorithms; present Spambase findings as proof about modern spam.

## Definition of done (per milestone)

Code in `src/` with tests passing, notebook reproducible from a clean environment, results logged in `documentation/EXPERIMENT_LOG.md`, and the README checkbox ticked.

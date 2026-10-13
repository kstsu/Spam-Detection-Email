cd "R:\SCHOOL\2026-2027\1st term\MachineLearning\Project\Spam-Detection-Email"

$rows = Import-Csv ".\data\original\spam_all.csv"

$columns = $rows[0].PSObject.Properties.Name |
    Where-Object { $_ -ne "label" }

$rows[0] |
    Select-Object -Property $columns |
    Export-Csv ".\sample_email_features.csv" -NoTypeInformation

Get-Item ".\sample_email_features.csv" | Select-Object Name, Length
Get-Content ".\sample_email_features.csv" -First 2# Spam Detection Email

> **What does a machine learning model actually need to recognise spam: the words and symbols, or the style (CAPITAL LETTERS)?**

Final group project for a Machine Learning course: an end-to-end, **traditional** ML solution that classifies emails as spam or not spam, explains *which kind of evidence matters*, and ships as a **Streamlit** app.

---

## At a glance (for humans and AI agents)

| | |
|---|---|
| **Problem type** | Binary classification (`spam` = positive class, `not_spam`) |
| **Core question** | Content (words + symbols) vs. style (capital letters): which signal matters, and how much? |
| **Intended users** | People or small teams who want a second opinion on whether an email is spam, and the course instructor evaluating the method |
| **Dataset** | UCI Spambase: 4,601 emails, 57 numeric features, 39.4% spam (see `data/original/SOURCE.md`) |
| **Algorithms** | **Exactly three** traditional algorithms, compared under identical conditions (proposed: Random Forest, Logistic Regression, Naive Bayes; final choice in `documentation/DECISIONS.md`) |
| **Not allowed** | Neural networks, deep learning, transformers, LLMs, pretrained models, AutoML |
| **Split / validation** | 80/20 stratified train/test; 5-fold stratified CV on the training set only; test set used **once** |
| **Primary metric** | Spam-class F1: balances catching spam with avoiding false positives |
| **Deployment** | Streamlit app with a public URL, plus local run instructions |
| **Stack** | Python 3.11+, pandas, scikit-learn, matplotlib/seaborn, joblib, Streamlit |
| **Status** | Core training pipeline, EDA generator, final evaluation, and local app implemented |

**AI assistants:** read `CLAUDE.md` first, then `documentation/PROJECT_REQUIREMENTS.md` (the course rules in checklist form) and `documentation/DECISIONS.md` (what is decided and what is still open).

---

## Project overview

**Practical problem.** Spam wastes time and carries scams and malware. A useful filter must catch spam *without* hiding legitimate email, because losing a real message (a false positive) usually costs more than seeing one extra spam (a false negative).

**Prediction target.** `label`: is this email spam?

**Why machine learning.** Spam cannot be caught by one rule. It shows up as many weak signals at once (certain words, `$` and `!` characters, long runs of capitals). A trained model combines these signals and can be measured objectively.

**Scope.** Supervised classification on the Spambase features. In scope: EDA, preprocessing, comparing three algorithms, picking one with evidence, and a working app. Out of scope: neural networks, live mailbox integration, and training on raw-text corpora (a possible future extension).

**Background.** An earlier class simulation (slides in `documentation/background/`) trained a small neural network on this data and got 92.78% accuracy with all features but 70.87% with only the three capital-letter features. Neural networks are **not permitted** in this project, so those numbers are context only; they motivate the research question and are not one of our three models.

---

## Core goals

### Research questions

1. **RQ1: Content vs. style.** How much predictive power does each feature family (words, symbols, capitals) have on its own?
2. **RQ2: Complementarity.** Do capital-letter features add anything once words and symbols are already used?
3. **RQ3: Why are capitals weak alone?** Is it missing context, or the extreme, unscaled values (some totals exceed 15,000) that hurt the earlier model? Tree-based models ignore feature scale, which makes them a useful check.
4. **RQ4: What does the chosen model rely on?** Which individual features drive its predictions?

### Hypotheses

- **H1:** Words + symbols carry most of the signal; capitals alone land well below the full model.
- **H2:** Capitals add a small but measurable gain on top of words + symbols.
- **H3:** A tree-based model on capitals only stays weak, which would point to missing context rather than scaling as the main reason.

### Course goals (what "done" means)

Everything in `documentation/PROJECT_REQUIREMENTS.md`, in short:

- Strong **EDA** (the largest rubric item), with at least five readable visualizations that each lead to a written finding or decision.
- **Exactly three** permitted algorithms compared fairly (same split, preprocessing, CV folds, primary metric).
- A **justified final model**, confirmed **once** on the untouched test set.
- A **deployed Streamlit app** that uses the same model and pipeline reported in the paper.
- A reproducible repository, dataset package, documentation, IEEE-style **IMRaD paper**, contribution record, and signed ownership declaration.

| Rubric criterion | Points |
|---|---|
| Exploratory data analysis | 25 |
| Three-algorithm comparison | 20 |
| Evaluation and model selection | 15 |
| Deployable application | 15 |
| Preprocessing and reproducibility | 10 |
| Paper, code and documentation | 10 |
| Problem and data definition | 5 |
| **Total** | **100** |

---

## Dataset

**UCI Spambase** (Hopkins, Reeber, Forman, Suermondt; Hewlett-Packard Labs, 1999). One row per email, already converted into numbers:

| Feature family | Count | Column prefix | Meaning |
|---|---|---|---|
| Word frequencies | 48 | `word_freq_` | Percentage of words in the email that match a listed word (`free`, `money`, ...) |
| Character frequencies | 6 | `char_freq_` | Percentage of characters that are `;` `(` `[` `!` `$` `#` |
| Capital-letter runs | 3 | `capital_run_length_` | Average, longest, and total length of runs of capital letters |
| Label | 1 | `label` | `spam` or `not_spam` |

Files in `data/original/`: `spam_all.csv` (57 features + label) and `spam_caps.csv` (3 capital-run features + label). Full data dictionary: `documentation/DATA_DICTIONARY.md`. Provenance, license note and limitations: `data/original/SOURCE.md`.

**Things to know**

- **Mild imbalance:** 1,813 spam vs. 2,788 not spam (about 1 : 1.54). Accuracy of always guessing `not_spam` is 60.6%, the baseline to beat.
- **Duplicates:** 391 exact duplicate rows in `spam_all.csv` and 979 in `spam_caps.csv`. A few duplicate groups even carry *conflicting* labels (3 in `spam_all.csv`, 34 in `spam_caps.csv`). These must be handled before splitting, and the action documented.
- **Dated and specific:** late-1990s data; some word features reflect the original mailbox.
- **No raw text:** emails are numbers only, so new word features cannot be created from this dataset.

---

## Approach

Follows the seven-step workflow required by the course.

| Step | What we do | Where |
|---|---|---|
| 1. Define the problem | Target, users, scope, success criteria, why ML | this README, `documentation/DECISIONS.md` |
| 2. Acquire and document data | Source, license, collection, limits, data dictionary | `data/original/SOURCE.md`, `documentation/DATA_DICTIONARY.md` |
| 3. EDA | Quality checks, distributions, feature-target relationships, class balance, outliers; at least 5 meaningful figures | `notebooks/01_eda.ipynb` |
| 4. Prepare data | Duplicates, outliers, scaling where needed, class imbalance; fit on training data only | `src/`, `notebooks/02_preprocessing.ipynb` |
| 5. Train three algorithms | Same split, preprocessing, CV folds, primary metric; documented tuning | `notebooks/03_model_comparison.ipynb` |
| 6. Evaluate and select | Validation comparison, one-time test evaluation, error analysis | `notebooks/04_final_evaluation.ipynb` |
| 7. Deploy | Streamlit app using the saved pipeline; tested with valid, invalid and boundary inputs | `app/`, `tests/` |

### The three algorithms (proposed, to be confirmed by the group)

| Algorithm | Why it is a good fit |
|---|---|
| **Random Forest** | Handles non-linear patterns and mixed-scale features, gives feature importances, no scaling needed |
| **Logistic Regression** | Fast, interpretable linear baseline; coefficients show which features push toward spam |
| **Naive Bayes** | The classic spam-filtering model; very fast; works naturally with word-frequency features |

Alternatives if the group prefers: Gradient Boosting, SVM, K-Nearest Neighbors. Changing only the hyperparameters of one algorithm does **not** count as a different algorithm. A dummy majority-class baseline may be reported but is not one of the three.

### Fair comparison protocol

- One 80/20 stratified split (fixed `random_state`); the test set stays untouched until the final model is chosen.
- Same preprocessing logic and the same 5-fold stratified CV folds for all three models, with tuning done inside the training data only.
- One **primary metric**, justified by the cost of false positives vs. false negatives, plus supporting metrics reported for **all three** models: accuracy, per-class precision, recall, F1, confusion matrix, ROC AUC. Report mean and variability across folds.
- Selection weighs performance, interpretability, speed and practical suitability.

### Feature-group analysis (answers RQ1 to RQ3)

Using cross-validation on the training data only, the chosen setup is also run on feature subsets: all 57, words only, symbols only, capitals only, words + symbols, words + capitals. This stays within the three-algorithm rule because it varies the *features*, not the algorithms. Permutation importance (including grouped by feature family) supports RQ4.

### The app (proposed design)

Spambase features are 57 percentages, which nobody can type by hand, so the app should offer two input paths:

1. **Paste email text**: the app computes the 57 Spambase-style features (word %, character %, capital runs) with the same definitions used in training, then predicts.
2. **Upload a CSV** with the 57 feature columns.

Both paths are validated (empty, wrong columns, negative or out-of-range values give clear messages, never a crash). Output: predicted class, spam probability, the model name, and a short guide to inputs and outputs. Text-to-feature extraction can only approximate the original Spambase tokenization; this is documented as a limitation.

---

## Roadmap

Dates depend on the course deadline (not stated in the requirements; **Due: [PLACEHOLDER]**).

### Short term: deliver the course project

- [ ] **M0: Repository bootstrap.** Structure, README, `CLAUDE.md`, documentation stubs, environment
- [ ] **M1: Problem and data definition** *(5 pts)*. Confirm the three algorithms, primary metric and its justification, dedupe policy; finish data dictionary and source/license note
- [ ] **M2: Exploratory data analysis** *(25 pts)*. Data quality, duplicates and conflicting labels, distributions, feature-target relationships, correlations, class balance, outlier investigation (errors vs. legitimate extremes), at least 5 figures each with a written finding, and an EDA findings summary that drives later decisions
- [ ] **M3: Preprocessing pipeline** *(10 pts)*. Leakage-safe scikit-learn pipeline, stratified 80/20 split, fixed random state, imbalance handling, reproducible end to end
- [ ] **M4: Three-algorithm comparison** *(20 pts)*. Identical conditions, documented tuning, same metrics for all three, mean ± std across folds, feature-group analysis
- [ ] **M5: Evaluation and model selection** *(15 pts)*. Validation vs. test clearly separated, one-time test evaluation, confusion matrix, error analysis, defensible choice; save the final pipeline to `models/`
- [ ] **M6: Streamlit app and deployment** *(15 pts)*. Load the saved pipeline, validated inputs, probabilities, public URL, tests with valid/invalid/boundary inputs, screenshots
- [ ] **M7: Paper, documentation and dataset package** *(10 pts)*. IMRaD paper in IEEE format (DOCX + PDF, 6 to 10 pages), IEEE citations, technical documentation, contribution record, signed declaration
- [ ] **M8: Final QA and submission.** Walk the checklist in `documentation/PROJECT_REQUIREMENTS.md`, test in a clean environment, build the ZIP, confirm the deployed URL works

### Long term: beyond the course

- [ ] Train on a **raw-text email corpus** (candidates: SpamAssassin Public Corpus, Enron-Spam) so style and content features can be computed from scratch
- [ ] Compare hand-built style features against **TF-IDF** word features
- [ ] Test **robustness** to obfuscation (`fr33`, `M0NEY`) and to modern spam
- [ ] Add a **model card** and monitoring ideas for drift
- [ ] Explore models outside this course's rules *only* as a separate follow-up, never in the graded comparison

---

## Deliverables and where they live

| # | Deliverable | Location |
|---|---|---|
| 1 | Deployable application (URL + local) | `app/` and the deployed URL: **[PLACEHOLDER]** |
| 2 | Source code, saved model, requirements | `src/`, `notebooks/`, `models/`, `requirements.txt`; repo link + ZIP |
| 3 | Technical documentation | this README, `documentation/` (PDF or DOCX for submission) |
| 4 | Dataset package | `data/original/`, `data/processed/`, `documentation/DATA_DICTIONARY.md`, `data/original/SOURCE.md` |
| 5 | IMRaD paper (DOCX + PDF) | `paper/` |
| 6 | Contribution record | `documentation/CONTRIBUTIONS.md` (copied into the paper appendix) |
| 7 | Signed ownership and authorship declaration | signed PDF in `documentation/` and as a paper appendix |

---

## Project structure

This matches the **required submission structure**. (The submitted ZIP's top-level folder must be named `GROUPNAME_PROJECTTITLE`.)

```text
Spam-Detection-Email/
├── README.md                    # setup and run instructions (this file)
├── CLAUDE.md                    # instructions for AI assistants
├── requirements.txt             # exact dependencies (pin before submission)
├── app/                         # Streamlit application
│   └── streamlit_app.py
├── data/
│   ├── original/                # untouched dataset + SOURCE.md
│   └── processed/               # cleaned/processed data
├── notebooks/                   # EDA and model-development notebooks
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_comparison.ipynb
│   └── 04_final_evaluation.ipynb
├── src/
│   └── spam_detection/          # reusable preprocessing and modeling code
│       ├── config.py            # paths, random seed, feature groups
│       ├── data.py              # load, validate, dedupe, split
│       ├── features.py          # feature groups; text -> 57 features for the app
│       ├── pipeline.py          # preprocessing + model pipelines
│       ├── train.py             # CV training and tuning
│       ├── evaluate.py          # metrics, confusion matrices, plots
│       └── explain.py           # importance, grouped permutation importance
├── models/                      # saved best model / complete pipeline (committed)
├── documentation/
│   ├── PROJECT_REQUIREMENTS.md  # course rules + checklist
│   ├── DECISIONS.md             # decisions made and open questions
│   ├── DATA_DICTIONARY.md
│   ├── EXPERIMENT_LOG.md
│   ├── CONTRIBUTIONS.md
│   ├── screenshots/             # app screenshots
│   └── background/              # original class slides
├── paper/                       # final DOCX and PDF
└── tests/                       # pytest tests, incl. app input tests
```

`tests/` is an extra on top of the required structure; keep it only if the instructor does not object.

---

## Getting started

```bash
git clone https://github.com/kstsu/Spam-Detection-Email.git
cd Spam-Detection-Email

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

$env:PYTHONPATH = "src"             # PowerShell; use `export PYTHONPATH=src` on macOS/Linux
python -m spam_detection.eda       # writes five figures and EDA findings
python -m spam_detection.train     # compares exactly three models and saves the winner
python -m spam_detection.final_evaluation
streamlit run app/streamlit_app.py
```

The training command uses the cleaned data, a stratified 80/20 split, and 5-fold CV on training data only. It saves the selected pipeline to `models/spam_detector.joblib`; validation metadata goes to `models/training_metadata.json`, and the one-time held-out test result goes to `models/final_test_metrics.json`. The app accepts pasted text or a CSV containing all 57 feature columns.

Troubleshooting: if `streamlit` or `pytest` is not found, activate the virtual environment and rerun `python -m pip install -r requirements.txt`; if the model fails to load, retrain it from the repository root.

---

## Team and contributions

| Member | Role / responsibility | Notes |
|---|---|---|
| [PLACEHOLDER] | [PLACEHOLDER] | |
| [PLACEHOLDER] | [PLACEHOLDER] | |

The full contribution record, confirmed by all members, lives in `documentation/CONTRIBUTIONS.md`.

---

## Limitations

- Spambase is old and small by modern standards; results describe this dataset, not spam in general.
- The word list is fixed: we can say which *listed* words matter but cannot discover new ones.
- Capital-letter features are summaries (average, longest, total), not per-message ratios.
- App text-to-feature extraction approximates the original feature definitions.

---

## Credits and license

- **Dataset:** Hopkins, M., Reeber, E., Forman, G., Suermondt, J. (1999). *Spambase*. UCI Machine Learning Repository.
- **Course:** Final Group Project Requirements, Traditional Machine Learning Model and Deployable Application.
- **Ownership and authorship:** governed by the signed declaration and university policy.
- **License:** [PLACEHOLDER]. Confirm with the group and the instructor before adding a `LICENSE` file.

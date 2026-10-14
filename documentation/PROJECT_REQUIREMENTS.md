# Project requirements (course rules in checklist form)

Source: *Final Group Project Requirements: Traditional Machine Learning Model and Deployable Application*. 

## Purpose

Design, train, evaluate and deploy an end-to-end **traditional** ML solution. Emphasis: **exploratory data analysis** and **evidence-based comparison of exactly three algorithms**, a justified final model, and a simple deployed app (Streamlit). Output must be reproducible and documented.

## Scope rules

- Clear classification or regression problem with a defined target and intended user/decision context. (Ours: binary spam classification.)
- Dataset must be legitimate, ethically obtained and appropriate. Public datasets are allowed.
- Unsupervised projects need prior written approval (not applicable here).

## Permitted vs. prohibited methods

| | Rule |
|---|---|
| Classification options | Logistic Regression, KNN, Naive Bayes, Decision Tree, Random Forest, SVM, LDA/QDA, AdaBoost, Gradient Boosting |
| Select | **Exactly three distinct algorithms** |
| **Not allowed** | Neural networks, deep learning, CNNs, RNNs, transformers, LLMs, pretrained foundation models, AutoML-generated solutions |
| Counting | Prohibited methods cannot count as one of the three. Changing only hyperparameters of the same algorithm is not a different algorithm. A simple baseline may be reported but does not replace any of the three. |

## Required workflow

1. **Define the problem:** problem, target, users, scope, success criteria, why ML.
2. **Acquire and document data:** source, license/permission, collection method, unit of analysis, records, features, target, limitations.
3. **EDA:** quality, distributions, relationships, target balance, unusual values. Every figure leads to a written finding or decision.
4. **Prepare data:** missing values, duplicates, outliers, encoding, scaling, feature selection, class imbalance. **Fit preprocessing on training data only.**
5. **Train three algorithms:** same split, preprocessing, CV strategy and primary metric. Document main hyperparameters and tuning.
6. **Evaluate and select:** compare validation results, confirm the chosen model **once** on the untouched test set, justify by performance, interpretability, speed and practical suitability.
7. **Deploy:** integrate final preprocessing and prediction pipeline into a working app; test with valid, invalid and boundary inputs.

## EDA minimum evidence

- [ ] Dimensions, data types, feature definitions, units, target labels, summary statistics
- [ ] Missing values, duplicates, inconsistent entries, impossible values, **and the action taken for each**
- [ ] Univariate distributions of important variables (plots + numbers)
- [ ] Feature-target relationships (correlation/association where appropriate)
- [ ] Class distribution and imbalance concerns
- [ ] Outlier investigation separating data errors from legitimate extremes
- [ ] **At least five** meaningful, readable visualizations (decorative charts get no credit)
- [ ] Concise EDA findings summary that informs preprocessing, feature selection, algorithm choice or evaluation

## Experimental design

- **80% train / 20% test**, stratified for classification (unless a justified alternative is given).
- Model selection and tuning **only within training data**, preferably **5-fold CV**.
- Test set untouched until the final model is selected. (Time-ordered data would need a chronological split; not applicable here.)
- **Primary metric:** choose and justify one (macro/weighted F1, recall, precision, ROC AUC, accuracy). State why it matches the real problem and identify the cost of false positives vs. false negatives.
- **Supporting metrics (same for all three models):** accuracy, per-class precision/recall/F1, confusion matrix, ROC AUC when appropriate.
- **Validation:** same CV folds and preprocessing pipeline; report mean and variability across folds.
- **Final test:** selected model evaluated once; validation and test results clearly separated.
- Accuracy alone is not sufficient for an imbalanced problem.

## Application requirements

- [ ] Streamlit (or another simple framework only with instructor approval)
- [ ] Loads the saved best model and the same preprocessing pipeline used in training
- [ ] Practical input via validated form fields or a properly formatted CSV upload
- [ ] Clearly shows predicted class/value; shows probabilities when the algorithm supports them
- [ ] Identifies the model used; explains input features, expected units and output meaning
- [ ] Handles missing, invalid and out-of-range inputs without crashing; understandable errors
- [ ] Deployed URL **and** complete local setup instructions; runs in a clean environment from the submitted requirements file
- [ ] No passwords, API keys, credentials or computer-specific absolute paths in source code

## Required deliverables

| # | Deliverable | Format |
|---|---|---|
| 1 | Deployable application | Streamlit URL (or approved equivalent), runnable locally |
| 2 | Source code: notebooks/scripts for EDA, preprocessing, training, comparison, evaluation, app; saved model/pipeline; requirements file | Repository link and ZIP |
| 3 | Technical documentation: README, install steps, folder structure, dependencies, run instructions, input format, app guide, model limitations, troubleshooting | README and PDF or DOCX |
| 4 | Dataset package: original data, processed data, data dictionary, source link, license/permission, processing notes | CSV or open format |
| 5 | IMRaD-style paper with IEEE numbered citations and references | DOCX and PDF |
| 6 | Contribution record: names, responsibilities, actual contributions, confirmation by all members | Appendix in the paper |
| 7 | Ownership and authorship declaration, signed by the instructor and all group members | Signed PDF (template in the original requirements) |

## Paper (IEEE conference format, 6 to 10 pages excluding appendices)

| Section | Minimum content |
|---|---|
| Title, Abstract, Keywords | Specific title; problem, dataset, three algorithms, principal result, selected model; 3 to 5 keywords |
| Introduction | Background, practical problem, objective/question, significance, scope, related literature |
| Methods | Dataset and ethics, features and target, EDA procedure, preprocessing, split, three algorithms, tuning, metrics |
| Results | EDA findings, comparison table (all models), validation results, final test results, confusion matrix or residual plots, application evidence |
| Discussion | Interpretation, why the selected model won, link to the problem, errors and tradeoffs |
| Conclusion and Recommendations | Answer the objective, selected model and practical value, limitations, realistic improvements |
| References | Complete IEEE numbered references, cited in order of first appearance |
| Appendices | Extra figures/tables, data dictionary, sample inputs/outputs, contribution record, signed declaration |

## Required submission structure

```text
GROUPNAME_PROJECTTITLE/
  app/             Streamlit application files
  data/original/   Original dataset and source note
  data/processed/  Cleaned dataset when applicable
  notebooks/       EDA and model development notebooks
  src/             Reusable preprocessing and modeling code
  models/          Saved best model or complete pipeline
  documentation/   Technical documentation and screenshots
  paper/           Final DOCX and PDF
  README.md        Setup and run instructions
  requirements.txt Exact software dependencies
```

## Grading rubric (100 points)

| Criterion | Points |
|---|---|
| Problem and data definition | 5 |
| Exploratory data analysis | 25 |
| Preprocessing and reproducibility | 10 |
| Three-algorithm comparison | 20 |
| Evaluation and model selection | 15 |
| Deployable application | 15 |
| Paper, code and documentation | 10 |

## Minimum acceptance conditions

- All required deliverables submitted on time and opening successfully.
- **Exactly three** permitted traditional algorithms compared (otherwise no credit for comparison and evaluation criteria).
- Deployed app and submitted local version use the **same model and pipeline** reported in the paper.
- Results reproducible from submitted data and code; no fabricated, altered or unverifiable results.
- Ownership and authorship declaration complete and signed by the instructor and all members.
- Academic integrity rules apply (no undisclosed copied work, fabricated citations or misrepresented contributions).
- The instructor may ask any member to demonstrate or explain any code, analysis, model, result or app feature.

## Final submission checklist

- [ ] Deployed application URL works
- [ ] Repository link and ZIP archive are accessible
- [ ] EDA notebook or script runs from start to finish
- [ ] Exactly three traditional algorithms are compared
- [ ] Best model selected using justified evaluation metrics
- [ ] Test set used only for final evaluation
- [ ] Original and processed datasets are included
- [ ] Data dictionary and dataset source or permission are included
- [ ] README and technical documentation are complete
- [ ] IMRaD paper submitted in DOCX and PDF
- [ ] IEEE in-text citations match the numbered reference list
- [ ] Group contribution record is signed or confirmed by all members
- [ ] Ownership and authorship declaration signed by the instructor and all group members

# Experiment log

One entry per experiment, newest at the bottom. Copy the template.

## Template

### YYYY-MM-DD: short title
- **Question:**
- **Features used:**
- **Model and settings:**
- **Split / CV scheme:** (same folds for all models)
- **Preprocessing:**
- **Results (mean ± std across folds):**
- **Interpretation (one sentence):**
- **Code / notebook:**

---

### 2026-10-02: Initial three-model comparison
- **Question:** Which of the three permitted traditional classifiers gives the strongest validation spam-class F1 on cleaned Spambase data?
- **Features used:** All 57 numeric Spambase features; exact duplicates removed before splitting.
- **Model and settings:** Logistic Regression (`C` in 0.1, 1, 10), Gaussian Naive Bayes (`var_smoothing` in 1e-9, 1e-8, 1e-7), and Random Forest (`max_features` and `min_samples_leaf` grid); balanced class weights where supported.
- **Split / CV scheme:** 80/20 stratified split; 5-fold stratified CV on the training partition only; random state 42.
- **Preprocessing:** StandardScaler inside Logistic Regression and Naive Bayes pipelines; Random Forest receives the original numeric scales.
- **Results (mean +/- std across folds):** Logistic Regression 0.906 +/- 0.019; Naive Bayes 0.812 +/- 0.017; Random Forest 0.935 +/- 0.016 spam F1.
- **Interpretation (one sentence):** Random Forest was selected because it had the highest validation F1 by a margin larger than its fold variability and can model nonlinear interactions among feature families.
- **Code / notebook:** `src/spam_detection/train.py`

### 2026-10-02: Final held-out evaluation
- **Question:** How does the selected Random Forest perform on the untouched test partition?
- **Features used:** All 57 features after the same duplicate policy and split.
- **Model and settings:** Saved Random Forest selected by training-only CV.
- **Split / CV scheme:** Single 20% test partition, evaluated once after selection.
- **Preprocessing:** The saved pipeline from model selection.
- **Results:** Accuracy 0.945; spam precision 0.929; spam recall 0.935; spam F1 0.932; ROC AUC 0.989; confusion matrix [[482, 24], [22, 314]].
- **Interpretation (one sentence):** The selected model catches most spam while producing 24 false positives among 506 legitimate test emails.
- **Code / notebook:** `src/spam_detection/final_evaluation.py`

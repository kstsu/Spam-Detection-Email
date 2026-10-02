# Decisions log

Record every project decision here with the reason. AI assistants: check this file before assuming a choice; if a row says **OPEN**, ask the group instead of guessing.

## Decided

| Decision | Choice | Reason |
|---|---|---|
| Problem type | Binary classification (`spam` = positive class) | Course scope; clear target |
| Dataset | UCI Spambase | Public, well known, fits the research question |
| Split | 80/20 stratified, 5-fold stratified CV on training data | Course requirement |
| Language and app framework | Python, Streamlit | Course requirement / preferred |

## OPEN (decide in M1)

| Question | Options / notes | Decision | Date |
|---|---|---|---|
| Which three algorithms? | Proposed: Random Forest, Logistic Regression, Naive Bayes. Alternatives: Gradient Boosting, SVM, KNN. Random Forest was recommended to the group. | **OPEN** | |
| Primary metric | Candidates: F1 of the spam class, precision of the spam class, ROC AUC. Think about cost: a real email sent to spam (false positive) vs. spam reaching the inbox (false negative). Accuracy alone is not enough. | **OPEN** | |
| Duplicate policy | Remove exact duplicates before splitting? What about the 3 groups in `spam_all.csv` with conflicting labels? Report results with and without if feasible. | **OPEN** | |
| Class-imbalance handling | Default plan: stratification + `class_weight="balanced"` where supported; no resampling unless needed. Imbalance is mild (about 1 : 1.54). | **OPEN** (default plan stands) | |
| App input design | Proposed: paste email text (converted to the 57 features) and CSV upload of the 57 columns. Text extraction only approximates the original feature definitions. | **OPEN** | |
| Use of `spam_caps.csv` | Capital-letters-only experiment (RQ1/RQ3). Note it has 979 duplicate rows because it has only 3 features. | **OPEN** | |
| Deployment host | Streamlit Community Cloud is a common free option; confirm it fits the course rules. | **OPEN** | |
| License for the repo | Confirm with the group and the instructor. | **OPEN** | |
| Group members and responsibilities | See `CONTRIBUTIONS.md` | **OPEN** | |
| Project deadline | Not stated in the requirements document | **OPEN** | |

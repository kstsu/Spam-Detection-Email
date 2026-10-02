# Decisions log

Record every project decision here with the reason. Completed choices are listed above; unresolved administrative items are marked `[PLACEHOLDER]`.

## Decided

| Decision | Choice | Reason |
|---|---|---|
| Problem type | Binary classification (`spam` = positive class) | Course scope; clear target |
| Dataset | UCI Spambase | Public, well known, fits the research question |
| Split | 80/20 stratified, 5-fold stratified CV on training data | Course requirement |
| Language and app framework | Python, Streamlit | Course requirement / preferred |
| Algorithms | Logistic Regression, Gaussian Naive Bayes, Random Forest | Exactly three permitted traditional algorithms; linear, probabilistic and tree-based inductive biases are compared |
| Primary metric | Spam-class F1 | Balances catching spam with avoiding false positives; accuracy alone hides the cost of the class imbalance |
| Duplicate policy | Remove exact duplicate rows before splitting; retain the first row and report conflicting-label groups | Prevents repeated records crossing train/test while preserving an auditable, deterministic policy |
| App input | Pasted text and 57-column CSV | Text is practical for users; CSV permits exact feature-level reproduction |

## Remaining project details

| Question | Options / notes | Decision | Date |
|---|---|---|---|
| Deployment host | Streamlit Community Cloud or another instructor-approved host | [PLACEHOLDER] | [PLACEHOLDER] |
| License for the repository | Confirm with the group and instructor | [PLACEHOLDER] | [PLACEHOLDER] |
| Group members and responsibilities | See `CONTRIBUTIONS.md` | [PLACEHOLDER] | [PLACEHOLDER] |
| Project deadline | Not stated in the requirements document | [PLACEHOLDER] | [PLACEHOLDER] |
| Feature-family ablation results | Run the planned all/words/symbols/capitals combinations | [PLACEHOLDER] | [PLACEHOLDER] |

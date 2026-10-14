# Decisions log

Record every project decision here with the reason. Administrative decisions are recorded below where they have been confirmed.

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
| Deployment host | Streamlit Community Cloud | Deployed at https://spamdetection-emailb.streamlit.app/ | 2026-10-14 |
| License for the repository | No separate source-code license declared; ownership remains with the project author | Avoids declaring a license without the author's/instructor's approval | 2026-10-14 |
| Group members and responsibilities | Individual project; complete contribution record in `CONTRIBUTIONS.md` | The project has one owner responsible for the complete implementation | 2026-10-14 |
| Project deadline | October 15, 2026 | Course submission deadline | 2026-10-14 |
| Feature-family ablation results | All: 0.935 +/- 0.016; words: 0.914 +/- 0.018; symbols: 0.791 +/- 0.021; capitals: 0.739 +/- 0.013; words + symbols: 0.921 +/- 0.018; words + capitals: 0.929 +/- 0.018 | Word features provide the strongest contribution, while combining feature families performs best | 2026-10-14 |

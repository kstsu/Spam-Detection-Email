# Data source note

| Item | Detail |
|---|---|
| Dataset | Spambase |
| Source | UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/94/spambase |
| Creators | Mark Hopkins, Erik Reeber, George Forman, Jaap Suermondt (Hewlett-Packard Labs), 1999 |
| License / permission | Creative Commons Attribution 4.0 International (CC BY 4.0), as listed by the UCI Machine Learning Repository |
| Collection method | Spam emails were collected from the postmaster and individuals who had filed spam. Non-spam emails came from filed work and personal emails. |
| Unit of analysis | One email message |
| Records | 4,601 emails (1,813 spam, 2,788 not spam) |
| Features | 57 numeric (48 word frequencies, 6 character frequencies, 3 capital-letter-run measures) |
| Target | `label`: `spam` / `not_spam` |

## Files in this folder

- `spam_all.csv`: all 57 features + `label` (4,601 rows).
- `spam_caps.csv`: the 3 `capital_run_length_*` features + `label` (4,601 rows); used for the capital-letters-only experiment.

## Known limitations

- Collected in the late 1990s; modern spam looks different.
- Some word features (`george`, `hp`, `hpl`, `650`, `415`, ...) reflect the mailbox the data came from.
- Emails are provided only as numbers; the original text is not available.
- Duplicate rows exist (391 in `spam_all.csv`, 979 in `spam_caps.csv`).

Do not edit the files in this folder. Cleaned data goes in `data/processed/`.

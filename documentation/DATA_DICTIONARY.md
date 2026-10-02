# Data dictionary

Dataset: UCI Spambase. Files: `data/original/spam_all.csv` (all columns) and `data/original/spam_caps.csv` (only the three `capital_run_length_*` columns + `label`).

Unit of analysis: one email. Rows: 4,601. Missing values: none found when loaded with pandas.

## Column families

| Family | Prefix | Count | Meaning | Unit |
|---|---|---|---|---|
| Word frequency | `word_freq_` | 48 | How often the named word appears in the email | percent of all words in the email (0 to 100) |
| Character frequency | `char_freq_` | 6 | How often the named character appears | percent of all characters in the email (0 to 100) |
| Capital-letter runs | `capital_run_length_` | 3 | Length of uninterrupted sequences of capital letters (average, longest, total) | number of characters |
| Target | `label` | 1 | Whether the email is spam | `spam` / `not_spam` |

Definitions follow the UCI Spambase documentation; confirm exact wording on the UCI page when finalising the paper.

## All columns

| # | Column | Family | Description |
|---|---|---|---|
| 1 | `word_freq_make` | word | Percent of words in the email that match "make" |
| 2 | `word_freq_address` | word | Percent of words in the email that match "address" |
| 3 | `word_freq_all` | word | Percent of words in the email that match "all" |
| 4 | `word_freq_3d` | word | Percent of words in the email that match "3d" |
| 5 | `word_freq_our` | word | Percent of words in the email that match "our" |
| 6 | `word_freq_over` | word | Percent of words in the email that match "over" |
| 7 | `word_freq_remove` | word | Percent of words in the email that match "remove" |
| 8 | `word_freq_internet` | word | Percent of words in the email that match "internet" |
| 9 | `word_freq_order` | word | Percent of words in the email that match "order" |
| 10 | `word_freq_mail` | word | Percent of words in the email that match "mail" |
| 11 | `word_freq_receive` | word | Percent of words in the email that match "receive" |
| 12 | `word_freq_will` | word | Percent of words in the email that match "will" |
| 13 | `word_freq_people` | word | Percent of words in the email that match "people" |
| 14 | `word_freq_report` | word | Percent of words in the email that match "report" |
| 15 | `word_freq_addresses` | word | Percent of words in the email that match "addresses" |
| 16 | `word_freq_free` | word | Percent of words in the email that match "free" |
| 17 | `word_freq_business` | word | Percent of words in the email that match "business" |
| 18 | `word_freq_email` | word | Percent of words in the email that match "email" |
| 19 | `word_freq_you` | word | Percent of words in the email that match "you" |
| 20 | `word_freq_credit` | word | Percent of words in the email that match "credit" |
| 21 | `word_freq_your` | word | Percent of words in the email that match "your" |
| 22 | `word_freq_font` | word | Percent of words in the email that match "font" |
| 23 | `word_freq_000` | word | Percent of words in the email that match "000" |
| 24 | `word_freq_money` | word | Percent of words in the email that match "money" |
| 25 | `word_freq_hp` | word | Percent of words in the email that match "hp" |
| 26 | `word_freq_hpl` | word | Percent of words in the email that match "hpl" |
| 27 | `word_freq_george` | word | Percent of words in the email that match "george" |
| 28 | `word_freq_650` | word | Percent of words in the email that match "650" |
| 29 | `word_freq_lab` | word | Percent of words in the email that match "lab" |
| 30 | `word_freq_labs` | word | Percent of words in the email that match "labs" |
| 31 | `word_freq_telnet` | word | Percent of words in the email that match "telnet" |
| 32 | `word_freq_857` | word | Percent of words in the email that match "857" |
| 33 | `word_freq_data` | word | Percent of words in the email that match "data" |
| 34 | `word_freq_415` | word | Percent of words in the email that match "415" |
| 35 | `word_freq_85` | word | Percent of words in the email that match "85" |
| 36 | `word_freq_technology` | word | Percent of words in the email that match "technology" |
| 37 | `word_freq_1999` | word | Percent of words in the email that match "1999" |
| 38 | `word_freq_parts` | word | Percent of words in the email that match "parts" |
| 39 | `word_freq_pm` | word | Percent of words in the email that match "pm" |
| 40 | `word_freq_direct` | word | Percent of words in the email that match "direct" |
| 41 | `word_freq_cs` | word | Percent of words in the email that match "cs" |
| 42 | `word_freq_meeting` | word | Percent of words in the email that match "meeting" |
| 43 | `word_freq_original` | word | Percent of words in the email that match "original" |
| 44 | `word_freq_project` | word | Percent of words in the email that match "project" |
| 45 | `word_freq_re` | word | Percent of words in the email that match "re" |
| 46 | `word_freq_edu` | word | Percent of words in the email that match "edu" |
| 47 | `word_freq_table` | word | Percent of words in the email that match "table" |
| 48 | `word_freq_conference` | word | Percent of words in the email that match "conference" |
| 49 | `char_freq_;` | character | Percent of characters in the email that are `;` |
| 50 | `char_freq_(` | character | Percent of characters in the email that are `(` |
| 51 | `char_freq_[` | character | Percent of characters in the email that are `[` |
| 52 | `char_freq_!` | character | Percent of characters in the email that are `!` |
| 53 | `char_freq_$` | character | Percent of characters in the email that are `$` |
| 54 | `char_freq_#` | character | Percent of characters in the email that are `#` |
| 55 | `capital_run_length_average` | capitals | Average length of runs of consecutive capital letters |
| 56 | `capital_run_length_longest` | capitals | Length of the longest run of consecutive capital letters |
| 57 | `capital_run_length_total` | capitals | Total number of capital letters in the email (sum of all run lengths) |
| 58 | `label` | target | Class label: `spam` (positive class) or `not_spam` |

## Notes

- Class counts: 1,813 spam (39.4%) and 2,788 not_spam (60.6%).
- Exact duplicate rows: 391 in `spam_all.csv`, 979 in `spam_caps.csv`. Policy: see `DECISIONS.md`.
- `capital_run_length_*` values are large and heavily skewed (some totals exceed 15,000): investigate in EDA whether they are errors or legitimate extremes.

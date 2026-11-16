# `ground_truth/published_claims.csv`

The extraction: one row per claim the article and its appendix make, numeric or not ([Stage 4](../stages/04_claims.md)). Unlike the other tables, much of this one is transcribed by a person: the printed values and the classifications are read off the page. It is reviewed by hand, committed, and read by both the ground truth build and `in_text_claims.R`.

`claim_id, location, claim_type, claim, value_paper, digits, comparison, expect, needs_block, notes`

| Column | Type | Meaning |
|---|---|---|
| `claim_id` | text | A unique, readable id (`t1_mturk_within`, `disc_spillover_ratio`). The key that joins this table to the ground truth, the claims script, and the errata. |
| `location` | text | Where the claim is printed: a float (`Table 1`), a page and section, a footnote, or an appendix section. |
| `claim_type` | closed | What kind of claim it is. |
| `claim` | text | A short description of what the number or statement is, including its units. |
| `value_paper` | text | The value as printed, normalized only in typography (leading zero, minus sign, thousands separators). For a claim with no number, the statement's truth value. |
| `digits` | integer | The number of decimal places the page prints. A `descriptive` claim has `0`. |
| `comparison` | closed | How the printed value relates to the quantity. |
| `expect` | closed | The non-default verdict the claims script declares for this claim, if any. |
| `needs_block` | logical | Whether `in_text_claims.R` must have a block for this claim. |
| `notes` | text | Anything a reader needs to interpret the row. |

## Allowed values

**`claim_type`**

| Value | Meaning |
|---|---|
| `pipeline` | A number the analysis produces: an estimate, a standard error, a p-value, a sample size. |
| `descriptive` | A claim about the results, often with no number: significance, direction, order, persistence. |
| `definitional` | A number that defines the design: the number of arms, a scale's range, a wave's date. |
| `structural` | A number about the document itself: "three experiments", the number of rows in a table. |
| `transcribed` | A number quoted from another source, such as another study's estimate. |

**`comparison`**

| Value | Meaning |
|---|---|
| `==` | The printed value is the quantity, at the printed precision. The default for every row with a `value_paper`. |
| `<`, `<=`, `>`, `>=` | The sentence states a bound ("less than 5 percent"). |
| `approx` | The sentence hedges the number ("about", "roughly"). The hedge's tolerance is set in [`rules/rounding.md`](../rules/rounding.md). |
| `NA` | The row has no `value_paper`. |

**`expect`**: `NA` (the usual case: the check compares values), `range`, `derived`, `shape`, or `absent`. The meanings are the verdicts of the same names in [Stage 4](../stages/04_claims.md). The column records what the claims script declares; the script, not this column, is what decides.

## Rules

- `needs_block` is `TRUE` for every `pipeline` and `descriptive` claim, and for any `definitional` or `structural` claim the pipeline can actually reach. The claims script must print exactly the claims marked `TRUE`, no more and no fewer.
- `digits` lives here and nowhere else. Both instruments read it from this file, so they cannot disagree about a claim's precision. The build also checks that `value_paper`, formatted at `digits`, gives back the stored string, which catches a wrong precision that would otherwise pass on both sides.
- `value_paper` is read as text. A CSV reader left to guess will turn "0.020" into 0.02.
- `claim_type` is the boundary of what gets checked, and nothing downstream audits it. We compared the `descriptive` and `definitional` rows within each section by hand, because the same construction, classified two ways two paragraphs apart, once left one of a pair of identical errors uncaught.

# `ground_truth/<paper_id>_ground_truth.csv`

One row per printed value or claim checked against the code: every cell of every table, every plotted quantity we could count, and every `pipeline` and `descriptive` claim in the text ([Stage 2](../stages/02_ground_truth.md)). The table is built by `ground_truth/build_ground_truth.R` as the last step of `run_all.R`, and the only values typed into it are the printed ones.

`paper_id, claim_id, location, claim_type, claim, value_paper, digits, value_script, match, value_rewrite, match_rewrite, holds, defect_locus, disposition, disposition_reason, notes`

| Column | Type | Meaning |
|---|---|---|
| `paper_id` | text | The paper's id, the same on every row. |
| `claim_id` | text | The key into `published_claims.csv`. Table cells, which have no extraction row, get ids of their own. |
| `location` | text | Taken from the extraction where the claim is there; a float cell keeps the float's name. |
| `claim_type` | closed | Copied from the extraction, so that the table reads on its own; float cells are `pipeline`. |
| `claim` | text | What the value is. |
| `value_paper` | text | The printed value, as a string. |
| `digits` | integer | The printed precision. From the extraction where the claim is there; for a float cell, from the printed string. |
| `value_script` | number | The value the deposited code produces, recovered from the Stage 1 run; `NA` where the archive was not run or does not produce it. |
| `match` | logical | Whether `value_script` agrees with `value_paper`, compared at the coarser of the page's precision and the precision the deposited code prints. |
| `value_rewrite` | number | The value the maintained rewrite produces, read from `maintained/output/` at full precision. |
| `match_rewrite` | logical | Whether `value_rewrite` agrees with `value_paper` at the printed precision; `NA` for an unseeded value, where no single run can match. |
| `holds` | logical | For a claim that is a statement rather than a value (a `descriptive` claim, or an unseeded value judged against its distribution), whether it is true of the rewrite's output. |
| `defect_locus` | closed | Where the problem lies, on every row where a comparison fails. |
| `disposition` | closed | What was done about the problem. |
| `disposition_reason` | text | Why, for the three dispositions that are judgments. |
| `notes` | text | Anything else, including a second contributing cause. |

The rules for comparing a computed value with a printed one are in [`rules/rounding.md`](../rules/rounding.md), and for values from random draws in [`rules/stochastic.md`](../rules/stochastic.md).

## Allowed values

**`claim_type`**: `pipeline`, `descriptive`, `definitional`, `structural`, `transcribed`, as in [`published_claims.md`](published_claims.md).

**`defect_locus`**

| Value | Meaning |
|---|---|
| `paper_internal` | The printed text is wrong: the code produces one number and the page prints another. |
| `archive` | The deposited code is wrong, and the page printed what it produced. |
| `environment` | The software changed: the deposited code, run today, gives a different number than it did then. |
| `rewrite` | The rewrite is wrong. We fixed these, so none should remain. |
| `upstream` | The problem is in something the paper relied on, such as a dataset or an estimate it reused. |
| `unresolved` | We looked and could not tell. |
| `NA` | No defect. |

**`disposition`**

| Value | Meaning |
|---|---|
| `corrected_here` | An entry in this repository's errata corrects it. Computed from `errata_entries.csv`, never typed. |
| `corrected_by_journal` | A published corrigendum or erratum corrects it. |
| `documented_only` | Recorded and deliberately not corrected: a value within simulation noise, or an archive bug the rewrite repairs that never reached the page. |
| `not_corrected` | Known, and left uncorrected for a stated reason. |
| `NA` | Nobody has decided yet. |

How the dispositions map onto the decision about which errors go to a journal is in [`rules/severity.md`](../rules/severity.md).

## Rules the build enforces

- **The locus rule.** A row where `match`, `match_rewrite`, or `holds` is `FALSE` must have a `defect_locus`. A row where every comparison passes must not, with one exception: a bug the deposited code has, the page printed, and the rewrite at first reproduced, which an erratum names. Such a row carries `archive` despite matching everywhere. A row with no verdict at all may or may not carry a locus. The locus is set where each row is built, never as a default for the whole table.
- **Disposition follows locus.** Every row with a locus gets a disposition, or `NA` while undecided. The build stops on any `paper_internal` row whose disposition is `NA`; the other loci are reported as a count.
- **The printed values are the only typed values.** `value_script`, `value_rewrite`, every verdict, and `corrected_here` come from code. A typed number that agrees with a note is indistinguishable from a computed number that agrees with the data, and only the second is evidence.
- **Built from the article first.** The rows come from what the paper prints, joined to what the pipeline produces, so that a printed value with no pipeline counterpart shows up as a row with an empty `value_rewrite` rather than not at all.
- **Joins are checked in both directions.** Every join asserts that its keys are unique on both sides and that the result is one-to-one, since a join that silently matches nothing looks the same as a table with nothing wrong.
- **Rows are never selected by their printed value.** Filtering pipeline output for the number the page prints guarantees a match.

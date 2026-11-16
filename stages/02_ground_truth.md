# Stage 2: Ground truth

The ground truth is one table, built by a script, that lists every number the paper prints and compares each with the value the original code produces and the value the maintained rewrite produces. Every erratum about a number traces back to a row in it, and every claim that the rewrite reproduces the paper rests on it.

We settled on two principles for it, both learned the hard way.

**Start from the article.** We list what the paper prints first, and only then join that list to what the pipeline computes. Our earliest attempts went the other way, starting from the code's output, and they were blind to any number the code never computed. Those turned out to be some of the most error-prone numbers of all: values typed into the text by hand, or left over from an earlier draft.

**Generate it rather than type it.** The only values in the table that a person types are the printed ones, transcribed from the published page. The archive's values come from running the deposited code, the rewrite's values are read from its output files, and the verdicts are computed. In one early repository, the comparison values had been typed in by hand too, and every row "matched", which meant the table couldn't have detected a problem if there had been one.

## The table

`ground_truth/<paper_id>_ground_truth.csv` is written by `ground_truth/build_ground_truth.R`, which `run_all.R` runs last:

`paper_id, claim_id, location, claim_type, claim, value_paper, digits, value_script, match, value_rewrite, match_rewrite, holds, defect_locus, disposition, disposition_reason, notes`

- `location` says where the number is printed: a table or figure, a page and paragraph, a footnote, or an appendix section.
- `value_paper` is the number exactly as printed, stored as text. Reading it as a number throws information away: `0.80` becomes `0.8`, `-0.00` becomes `0`, and the printed precision, which is part of what the paper claims, is lost. We had this happen in several repositories before we started forcing the column to be read as text everywhere.
- `digits` is the precision the page prints, recorded for each row.
- `value_script` comes from running the deposited code in Stage 1, and is left empty where the archive couldn't be run.
- `value_rewrite` is read from the rewrite's output at full precision.
- `match`, `match_rewrite`, and `holds` take the values `TRUE`, `FALSE`, or empty.

The full definitions are in [`schemas/ground_truth.md`](../schemas/ground_truth.md).

## When two numbers match

A computed value matches a printed one when, rounded to the precision the page prints, it gives the same digits. Before comparing, both sides get the same clean-up: a missing leading zero restored, a typographic minus sign replaced, thousands separators removed, and a negative zero treated as zero. A tiny tolerance (`1e-9`) absorbs floating-point representation, and nothing else.

Three refinements came up often enough to write down:

- **Hedged numbers.** When the text itself hedges ("about 40 percent", "roughly", "nearly", "on the order of"), we compared within half a step of the sentence's own precision. When the text states an approximate number without a hedge, we held it to its printed digits: a sentence that says 40 percent about a value of 38 percent is an error.
- **Differences of printed values.** When the text reports a difference between two printed cells, we allowed one unit in the last digit, since each cell was rounded separately.
- **The archive's precision.** We compared the archive's value at the coarser of the page's precision and the precision at which the deposited code itself prints.

More detail and examples are in [`rules/rounding.md`](../rules/rounding.md).

## Numbers that come from random draws

Bootstrap intervals, randomization-inference p-values, simulated power, and anything else based on random draws can differ from run to run, and between software versions even with the same seed. Before putting a difference down to randomness, we checked that the procedure actually draws at random; more than once, a difference that looked like noise was a deterministic bug. For a value the paper reports without a seed, we compared it with the distribution of that value over many seeds, left `match_rewrite` empty, and recorded in `holds` whether the printed value was consistent with that distribution. A printed value far outside any reasonable draw counts as an error; one inside the range doesn't. See [`rules/stochastic.md`](../rules/stochastic.md).

## Where the problem is: `defect_locus`

Each row where a comparison fails (`match`, `match_rewrite`, or `holds` is `FALSE`) records where the problem lies:

| `defect_locus` | Meaning |
|---|---|
| `paper_internal` | The printed text is wrong: the code produces one number and the page prints another (a typo, a stale number, a rounding slip, a transposed cell). |
| `archive` | The deposited code is wrong: it produces a number that a corrected computation doesn't, and the page printed what the code produced. |
| `environment` | The software changed: the deposited code, run today, gives a different number than it did then. |
| `rewrite` | The maintained rewrite is wrong. We fixed these, so none should remain at the end. |
| `upstream` | The problem is in something the paper relied on, such as a dataset or an estimate it reused. |
| `unresolved` | We looked, and couldn't tell. |

The rule cuts both ways: a failing row gets a locus, and a row where everything matches doesn't. A row with no verdict, such as an unseeded value, may or may not.

One case is easy to miss. Sometimes the page, the archive, and the rewrite all agree, yet the number is wrong, because the deposited code has a bug and the rewrite faithfully reproduced it before the bug was found. Every comparison "matches", and the paper is still in error. We record those rows with the locus `archive`, and only when an erratum names them.

We set the locus where each row is built, rather than as a default for the whole table, and put any second contributing cause in `notes`.

## What was done about it: `disposition`

Each row with a defect also records what happened to it:

| `disposition` | Meaning |
|---|---|
| `corrected_here` | An entry in this repository's errata corrects it. This one is computed from the errata, never entered by hand. |
| `corrected_by_journal` | A published corrigendum or erratum corrects it. |
| `documented_only` | Recorded here and deliberately not corrected (a value within simulation noise, for example). |
| `not_corrected` | Known, and left uncorrected for a stated reason. |
| empty | Nobody has decided yet. |

The three judgment values come with a `disposition_reason`. The build stops if any `paper_internal` row has no disposition, since an error in the printed text that nobody has decided about is unfinished business.

The dispositions line up with the choice an author faces for each error: fix it in your own errata, send it to the journal, or record it and move on. [`rules/severity.md`](../rules/severity.md) describes how we made that choice.

## Coverage

Our first coverage check asked only whether every table had at least one row in the ground truth, and it passed while missing most of the numbers on some tables. We now report coverage table by table and figure by figure, as a fraction, in `ground_truth/float_coverage.csv`:

`float, published_numbers, covered, reproduced_by_rewrite, reproduced_by_archive, plotted, plotted_reproduced, note`

- The list of tables and figures comes from the article itself, and we checked it in both directions: every table and figure in the article has a row, and every row names one that the article contains.
- `published_numbers` counts the numbers printed on each table or figure, and `covered` counts how many of them have a row in the ground truth.
- For a figure that prints no numbers, what it plots is the claim, so we counted the plotted quantities and how many the rewrite reproduces. A figure never got a pass just for having no printed numbers.
- The README reports each covered fraction.

Two things caught us out when joining the article's list to the pipeline's output. A join that silently matches nothing produces empty values that look like "couldn't check" rather than "missing", and a join that matches one row to several quietly duplicates rows. We checked every join in both directions and confirmed that each matched one row to one row. We also stopped selecting rows by their published value, which guarantees a match.

Finally, we read multi-column tables from the rendered page rather than from text extracted from the PDF. Text extraction can scramble columns, and a misread cell produces an erratum that isn't real.

## Done when

The build script runs as the last step of `run_all.R`, and it stops if any printed value has been read as a number, if any failing row lacks a `defect_locus` or any matching row has one, if any `paper_internal` row lacks a disposition, if any join is not one-to-one, or if any published table or figure is missing from `float_coverage.csv`.

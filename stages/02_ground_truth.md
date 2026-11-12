# Stage 2: Ground truth

**Purpose.** Write down every number the paper prints, and compare each one with the value the original code produces and the value the maintained rewrite produces, in one table that a script builds.

The ground truth is the backbone of the whole procedure. Every erratum about a number traces to a row in it, and every claim that the rewrite reproduces the paper rests on it. Two principles govern it.

**Start from the article, not the code.** Enumerate what the paper prints, then join it to what the pipeline computes. If you start from the pipeline's output, any number the pipeline never computes is invisible, and those are exactly the numbers most likely to be wrong.

**Generate it; never type it.** The only values in the ground truth typed by a person are the printed values, transcribed from the published page. The archive's values come from running the deposited code; the rewrite's values are read from the rewrite's output; the verdicts are computed. A ground truth with typed comparison values agrees with itself by construction and can detect nothing.

## 2.1 The table

`ground_truth/<paper_id>_ground_truth.csv`, built by `ground_truth/build_ground_truth.R`, which the entry point runs last:

`paper_id, claim_id, location, claim_type, claim, value_paper, digits, value_script, match, value_rewrite, match_rewrite, holds, defect_locus, disposition, disposition_reason, notes`

- `location` says where the number is printed: a table or figure, a page and paragraph, a footnote, or an appendix section.
- `value_paper` is the number **as printed**, stored as text. Never let it pass through a numeric type: `0.80` read as a number becomes `0.8`, and `-0.00` becomes `0`, and the printed precision, which is part of the claim, is gone. Force every reader of this column to read it as a string.
- `digits` is the precision the page prints, carried per row, never inferred from the value alone.
- `value_script` comes from running the deposited code (Stage 1), and is empty where the archive could not be run. Columns are never dropped because they are empty.
- `value_rewrite` is read from the rewrite's output at full precision.
- `match`, `match_rewrite`, and `holds` are written `TRUE`, `FALSE`, or empty, never `1` and `0`.

The full column definitions and vocabularies are in [`schemas/ground_truth.md`](../schemas/ground_truth.md).

## 2.2 When two numbers match

A computed value matches a printed one when, rounded to the page's printed precision, it gives the same digits. Before comparing, normalize both sides in the same way: a missing leading zero, a typographic minus sign, thousands separators, and a signed zero. Use a small numerical tolerance (`1e-9`) only to absorb floating-point representation, never to forgive a rounding difference.

Three refinements:

- **Hedged numbers.** A number the page itself hedges ("about 40 percent", "roughly", "nearly", "on the order of") is compared within half a step of the sentence's own precision. An *unhedged* approximation is held to the printed digits: if the text says 40 percent and the value is 38, that is an error, not an approximation.
- **Differences of printed values.** A difference the text computes from two printed cells is allowed one unit in the last digit, since each cell was rounded on its own.
- **Comparing the archive.** The archive's value is compared at the coarser of the page's precision and the precision the deposited code itself prints.

The full rule, with examples, is in [`rules/rounding.md`](../rules/rounding.md).

## 2.3 Numbers that come from random draws

Bootstrap intervals, randomization-inference p-values, simulation-based power, and anything else drawn at random can differ from run to run, and between software versions even with the same seed. First confirm that the procedure really draws at random; an unexpected difference is often a deterministic bug that someone attributed to noise. Then, for a value the paper reports without a fixed seed, compare it with the distribution of the value over many seeds rather than with a single draw. Leave `match_rewrite` empty and record whether the printed value is consistent with that distribution in `holds`. A printed value far outside the range of reasonable draws is an error; one inside it is not. See [`rules/stochastic.md`](../rules/stochastic.md).

## 2.4 Where the defect is: `defect_locus`

Every row where a comparison fails (`match` or `match_rewrite` is `FALSE`, or `holds` is `FALSE`) must say where the problem lies:

| `defect_locus` | Meaning |
|---|---|
| `paper_internal` | The printed text is wrong: the code produces the right number and the page prints another (a typo, a stale number, a rounding slip, a transposed cell). |
| `archive` | The deposited code is wrong: it produces a number that a corrected computation does not, and the page faithfully printed the wrong one. |
| `environment` | The software changed: the deposited code, run today, produces a different number than it did then. |
| `rewrite` | The maintained rewrite is wrong. Fix it; this locus should not survive to the end. |
| `upstream` | The error is in something the paper relied on (a dataset, a published estimate it reused). |
| `unresolved` | You looked, and cannot tell. |

The rule is strict in both directions: a failing row **must** carry a locus, and a row where everything matches **must not**. A row with no verdict (an unseeded value, say) may. One special case is easy to get wrong. When the page, the archive, and the rewrite all agree but the agreed number is wrong because the deposited code has a bug, every comparison "matches", yet the paper is in error. That row carries `archive` as its locus, and only if an erratum names it.

Name the locus where each row is built, never as a default for the table. A second contributing cause goes in `notes`.

## 2.5 What happened to it: `disposition`

Every row with a defect also records what was done about it:

| `disposition` | Meaning |
|---|---|
| `corrected_here` | An entry in this repository's errata corrects it. Computed from the errata, never typed. |
| `corrected_by_journal` | A published corrigendum or erratum corrects it. |
| `documented_only` | Recorded here, deliberately not corrected (for example, a value inside simulation noise). |
| `not_corrected` | Known, and left uncorrected, for a stated reason. |
| empty | Nobody has decided yet. |

The three judgment values carry a `disposition_reason`. The builder stops if any `paper_internal` row has no disposition: an error in the printed text that nobody has decided about is an unfinished job.

These dispositions map onto the decision every author faces about each error: fix it in your own errata, send it to the journal, or record it and move on. See [`rules/severity.md`](../rules/severity.md).

## 2.6 Coverage: did you look at everything?

"Every table has at least one row" is not coverage. Coverage is reported per table and figure, as a fraction:

`ground_truth/float_coverage.csv`: `float, published_numbers, covered, reproduced_by_rewrite, reproduced_by_archive, plotted, plotted_reproduced, note`

- List the published tables and figures from the article itself, not from the code, and check the list in both directions: every float the article contains has a row, and every row names a float the article contains.
- `published_numbers` counts the numbers printed on each table or figure; `covered` counts how many have a ground-truth row.
- For a figure with no printed numbers, the claim is what it plots: count the plotted quantities and how many the rewrite reproduces. A figure is never exempt merely because it "prints no numbers".
- Report the covered fraction in the README.

Join the article's list to the pipeline's output in both directions, and check that every join matches one row to one row. A join that silently matches nothing produces an empty value that reads like "could not be checked", and a many-to-many join duplicates rows. Never select a row by its published value: that guarantees a match.

Read multi-column tables from the rendered page, not from text extracted from the PDF. Text extraction scrambles columns, and a misread cell manufactures an erratum.

## Gate

The builder runs as the last step of the entry point and stops if: any printed value has been read as a number; any failing row lacks a `defect_locus`, or any clean row has one; any `paper_internal` row lacks a disposition; any join is not one-to-one; or any published table or figure is missing from `float_coverage.csv`.

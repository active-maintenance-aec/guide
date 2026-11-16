# `ground_truth/float_coverage.csv`

One row per table and figure in the article and appendix, saying how much of each the ground truth actually checks ([Stage 2](../stages/02_ground_truth.md)). We added it after a coverage check that asked only whether each float had at least one row passed for months on a figure with one checked value out of more than a hundred printed.

`float, published_numbers, covered, reproduced_by_rewrite, reproduced_by_archive, plotted, plotted_reproduced, note`

| Column | Type | Meaning |
|---|---|---|
| `float` | text | The float's name as printed (`Table 2`, `Figure B.3`). |
| `published_numbers` | integer | The numbers printed on the float: every cell of a table, and any numbers printed on the face of a figure. |
| `covered` | integer | How many of those numbers have a row in the ground truth. |
| `reproduced_by_rewrite` | integer | How many of the covered numbers the rewrite reproduces. |
| `reproduced_by_archive` | integer | How many of the covered numbers the deposited code reproduces. |
| `plotted` | integer | For a figure, the number of plotted quantities (points, bars, interval endpoints); `NA` for a table. |
| `plotted_reproduced` | integer | How many plotted quantities the rewrite reproduces; `NA` for a table. |
| `note` | text | Anything a count needs, such as why a float carries no data. |

## Rules

- **The list of floats comes from the article,** not from the scripts. An article's own front matter or numbering says what it contains, and the table is checked against that list, so a float with no script still gets a row.
- **A figure that prints no numbers is not thereby covered.** Its `published_numbers` is `0`, and what it plots is the claim, so `plotted` and `plotted_reproduced` carry the check. A figure is never passed just because it prints no numbers.
- **Some figures cannot be counted.** A figure with too many points to count records what the rewrite plots and says so in `note`; a continuous surface records that it has no discrete points. A diagram that carries no data gets zero counts and a `note`.
- **Every count is computed.** A typed count once sat a few lines below the code that should have produced it, and claimed eleven covered values where there were three.
- **The README states each fraction.** Computing coverage inside a check that only stops the build leaves a reader with nothing; the report reads this table and prints it.

A paper with no tables or figures writes this table with a header and no rows.

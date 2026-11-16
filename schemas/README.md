# Schemas

Every paper's repository produces the same seven tables, with the same columns in the same order. We settled on one schema for all of them after finding that repositories built months apart had drifted into different column names for the same thing, which made it impossible to summarize the collection without a translation layer for each paper.

| Table | Path | Written in | Schema |
|---|---|---|---|
| Deposit manifest | `original_manifest.csv` | [Stage 1](../stages/01_archive_check.md) | [`original_manifest.md`](original_manifest.md) |
| Archive run | `ground_truth/archive_run_status.csv` | [Stage 1](../stages/01_archive_check.md) | [`archive_run_status.md`](archive_run_status.md) |
| Archive overwrites | `ground_truth/archive_overwrites.csv` | [Stage 1](../stages/01_archive_check.md) | [`archive_overwrites.md`](archive_overwrites.md) |
| Claims extraction | `ground_truth/published_claims.csv` | [Stage 4](../stages/04_claims.md) | [`published_claims.md`](published_claims.md) |
| Ground truth | `ground_truth/<paper_id>_ground_truth.csv` | [Stage 2](../stages/02_ground_truth.md) | [`ground_truth.md`](ground_truth.md) |
| Float coverage | `ground_truth/float_coverage.csv` | [Stage 2](../stages/02_ground_truth.md) | [`float_coverage.md`](float_coverage.md) |
| Errata | `errata_entries.csv` | [Stage 5](../stages/05_errata.md) | [`errata_entries.md`](errata_entries.md) |

## Conventions that apply to every table

- **The tables are build output.** Each is written by a script in the repository, and a change is made by changing the script, never by editing the CSV. The two exceptions are the printed values and the claim classifications in `published_claims.csv`, which a person transcribes and reviews; even there, the file is read by code and never edited to make a check pass.
- **Every table exists in every repository.** A deposit that could not be run still gets an `archive_run_status.csv` saying why, and an `archive_overwrites.csv` with a header and no rows. A paper with no tables or figures gets a header-only `float_coverage.csv`. A missing file is then always a failure, never a sign that a stage did not apply.
- **Logical columns are written `TRUE`, `FALSE`, or `NA`**, never `1` and `0`, and never left as an empty string where `NA` is meant.
- **Printed values are text.** Any column that holds a number as the page prints it (`value_paper`, `published`) is stored as the string, so that the precision survives. See [`rules/rounding.md`](../rules/rounding.md).
- **Floats are named as printed**: `Table 1`, `Figure B.2`, never `table_1`.
- **Closed vocabularies are closed.** Each schema page lists the allowed values for its categorical columns, and the build rejects anything else. A value that seems to need a new category usually means the row has been misclassified.

## Older names

If you are migrating an older repository, the main renames were `table_figure` to `location`, `operator` to `comparison`, and a handful of archive tables (`archive_script_status.csv`, `archive_generated_files.csv`, and others) folded into `archive_run_status.csv` and `archive_overwrites.csv`. Archive pass names such as `deposited` and `as_deposited` became `as_shipped`, and `clean` became `stripped`. Columns that only one repository carried were folded into `notes` or dropped.

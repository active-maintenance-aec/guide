# Stage 1 for agents: archive check

Source of truth: [`stages/01_archive_check.md`](../stages/01_archive_check.md). Schemas: [`original_manifest.md`](../schemas/original_manifest.md), [`archive_run_status.md`](../schemas/archive_run_status.md), [`archive_overwrites.md`](../schemas/archive_overwrites.md).

## Goal

A verified manifest of the deposit, a download script that stops on any discrepancy, and a record of what happens when the deposited code runs.

## Do

1. Build `original_manifest.csv` from the archive's API, not by hand, with every checksum the archive publishes and every file's byte size. For Dataverse, request each file in its original format.
2. Write `download_original.R` to download every listed file into `original/`, stop on any size or served-checksum mismatch, print any published-checksum mismatch, stop on any file in `original/` the manifest does not list (hidden files included), and unpack any zip or RAR into its own folder checked against a second manifest.
3. Make it the first step of `run_all.R`, and run it.
4. Before running any deposited code, search it for every call that writes a file, after joining continued lines.
5. Copy the deposit to a scratch folder and run each deposited script there, twice: once as shipped, and once with every intermediate file the deposit ships removed. Run under the software of the paper's day where it matters (for R code from before April 2019 that draws with `sample()`, `RNGkind(sample.kind = "Rounding")`). Capture printed output: in R, source with `print.eval = TRUE`.
6. Write one row per script per pass to `ground_truth/archive_run_status.csv`, including `not_run` rows with the reason for anything you could not run.
7. After each pass, compare every file with the manifest and write what was added, overwritten, rebuilt, withheld, or deleted to `ground_truth/archive_overwrites.csv`.

## Do not

- Run deposited code in `original/`, or edit any deposited file.
- Fix the deposited code. Record why each failure happened; the failures are part of the record.
- Treat a clean exit as reproduction. Whether the archive reproduces the paper is decided in Stage 2.
- Accept a deprecation warning, or a recorded "package removed", as the cause of a failure without testing it.

## Stop and ask the author

- When the published and served checksums disagree for a file that is not a converted tabular file.
- When a script needs software you cannot run (Stata, a licensed dataset).

## Done when

The manifest verifies, the download script stops on any mismatch, and every deposited script has a row in `archive_run_status.csv` for each pass.

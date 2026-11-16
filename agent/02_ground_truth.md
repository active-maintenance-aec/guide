# Stage 2 for agents: ground truth

Source of truth: [`stages/02_ground_truth.md`](../stages/02_ground_truth.md). Schemas: [`ground_truth.md`](../schemas/ground_truth.md), [`float_coverage.md`](../schemas/float_coverage.md). Rules: [`rounding.md`](../rules/rounding.md), [`stochastic.md`](../rules/stochastic.md).

## Goal

One generated table comparing every printed number with the archive's value and the rewrite's value, and a coverage table saying how much of each float it checks.

## Do

1. List every table and figure from the article and appendix themselves, and write a row for each in `float_coverage.csv`.
2. Transcribe every printed value from images of the published pages, as strings, with their printed precision. Read multi-column tables from the rendered page, not from extracted text. Read numbers printed on a figure by position.
3. Write `ground_truth/build_ground_truth.R`, run last by `run_all.R`. It starts from the transcribed values and joins them to the archive's values (from the Stage 1 runs) and the rewrite's values (from `maintained/output/`, at full precision).
4. Compare at the printed precision, by formatting the computed value and comparing strings, after the normalizations in `rules/rounding.md`. Compare the archive at the coarser of the page's precision and the precision the deposited code printed.
5. For values from random draws, first confirm that something draws at random. For unseeded values, compare against the distribution over many seeds, leave `match_rewrite` as `NA`, and record the verdict in `holds`.
6. On every row where a comparison fails, set `defect_locus` where the row is built, and propose a `disposition`. Compute `corrected_here` from `errata_entries.csv`.
7. Make the build stop if: a printed value has been read as a number; a failing row has no locus or a passing row has one (apart from the documented exception); a `paper_internal` row has no disposition; any join is not one-to-one; or a float is missing from `float_coverage.csv`.
8. Compute every count in `float_coverage.csv`.

## Do not

- Type any value except the printed ones.
- Select a row by its printed value.
- Read the printed values with automatic type guessing.
- Count a float as covered because it has one row, or because it prints no numbers.
- Set a default locus for the whole table.

## Stop and ask the author

- When the page, the archive, and the rewrite disagree and you cannot tell which is wrong (propose `unresolved`).
- When a value is wrong in a way that may change a conclusion.

## Done when

The build runs last in `run_all.R` and passes all of its checks.

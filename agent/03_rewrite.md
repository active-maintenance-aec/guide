# Stage 3 for agents: maintained rewrite

Source of truth: [`stages/03_rewrite.md`](../stages/03_rewrite.md). Rules: [`erratum.md`](../rules/erratum.md). Style: the repository's `STYLE.md`.

## Goal

New code, on current packages, that reproduces every table, figure, and number in the paper from the deposited data.

## Do

1. Write one script per table or figure, named for what it produces, with cleaning separate from analysis and shared functions in one helpers file. Follow `STYLE.md`.
2. Write everything to `maintained/output/`. Beside every figure, write a CSV of every quantity it plots. Beside every formatted table, write its values unrounded.
3. Keep the paper's estimator, specification, sample, standard errors, and seed.
4. Correct unambiguous coding errors (a wrong variable, index, or column; a covariate the paper's description says should or should not be there; a rank-deficient model that silently dropped a column). Record each correction for the ground truth and the errata.
5. Use the current random-number generator. Where it moves a published number, the ground truth records `environment`.
6. Compare every rendered figure with the published one by eye, in addition to its numbers.
7. Blank the timestamps in PDF output.
8. Run `run_all.R` twice from fresh sessions, check both exit statuses, and confirm the second run leaves `maintained/output/` byte-identical.

## Do not

- Use any published number as an input. If a script seems to need one, the computation upstream is missing.
- Write a script that returns early because its output already exists.
- Accept a comment saying a number "can't be computed" from the deposit without trying.
- Change an analysis choice because `STYLE.md` or current practice prefers another.
- Carry a deposited bug into the rewrite because the archive has it.

## Stop and ask the author

- When it is unclear whether a discrepancy is a coding error or an analysis choice.
- When two deposited values are both defensible and the paper does not say which was meant.

## Done when

`run_all.R` runs from a clean session, every table and figure has a script that produces it, no published value is an input, and two runs in a row leave `maintained/output/` unchanged.

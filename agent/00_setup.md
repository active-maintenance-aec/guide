# Stage 0 for agents: setup and style

Source of truth: [`stages/00_setup.md`](../stages/00_setup.md).

## Goal

A repository skeleton, the published record in hand, the deposit identified, and an approved `STYLE.md`.

## Do

1. Collect the publisher's rendered PDFs: the article (version of record), the online appendix, and any published corrigendum. Do not use a preprint or accepted manuscript as a source of published values.
2. Find the replication deposit and record its DOI. Do not copy the data into the repository.
3. Ask the author which materials outside the deposit exist (production `.tex` or `.docx`, proofs, accepted manuscript, old working scripts) and where they are. Treat a working-folder `.tex` as the published text only if its compiled PDF matches the publisher's.
4. Create the repository with the layout in the stage file: `run_all.R` (or the language's equivalent), `download_original.R`, `maintained/`, `maintained/output/`, `ground_truth/`, `errata.qmd`, `README.qmd`, a `.gitignore` that excludes `original/`, and a license.
5. Use paths relative to the repository root everywhere.
6. Read the recent code the author points you to, and draft `STYLE.md`: script organization, naming, data manipulation idioms, modeling defaults, figures (with a CSV of plotted values beside each), tables, and things to avoid. Quote examples from the author's code.
7. Give the draft to the author and revise it until they approve it. Commit the approved version.

## Do not

- Let `STYLE.md` override the paper's own choices. The rewrite keeps the original estimator, specification, sample, standard errors, and seed whatever `STYLE.md` prefers. Say so in `STYLE.md`.
- Use materials outside the deposit as inputs to the rewrite. They explain errors; they do not supply numbers.

## Stop and ask the author

- When you cannot find the deposit, or find more than one version of it.
- When a corrigendum or erratum exists and you are unsure which version of a passage is the one to check.

## Done when

The repository exists with its entry point and layout, the published PDFs are in hand, the deposit DOI is recorded, and an approved `STYLE.md` is committed.

# Active maintenance: a guide

This guide is for a researcher who has published a paper with a replication archive and wants the archive to keep working. The method is *active maintenance*: rewrite the cleaning and analysis code so it runs on current software, check every number the paper prints against both the original code and the rewrite, and publish an itemized list of any errors found, beside the maintained code. The proposal is Peer, Orr, and Coppock (2021), "Active Maintenance: A Proposal for the Long-Term Computational Reproducibility of Scientific Results," *PS: Political Science & Politics*. This guide is the procedure that came out of doing it, with AI coding agents, for 40 published books and articles.

The guide is written for people. Every stage also has an agent file in `agent/` that gives the same instructions as imperatives, so that a coding agent can follow them. Where the two disagree, the human document is right and the agent file is a bug.

## What you end up with

One public repository per paper, which:

1. fetches the original deposit from its archive and verifies every file against a checksum manifest, without redistributing the data;
2. records whether each deposited script still runs, as shipped;
3. holds a maintained rewrite that reproduces every table, figure, and number in the text from the deposited data, on current software;
4. holds a *ground truth*: one generated table comparing each printed number with the value the original code produces and the value the rewrite produces;
5. checks every claim in the text a second, independent way, by quoting the sentence and recomputing its number; and
6. publishes an itemized errata note, with corrected values computed by the code rather than typed.

The repository then gets a permanent DOI (we use Zenodo), the original deposit gets a link to it, and a scheduled job reruns the whole pipeline every few weeks so you learn when a software update moves a number.

## The stages

| Stage | What it does | What it produces |
|---|---|---|
| [0. Setup and style](stages/00_setup.md) | Gather the paper and every source that can settle a question about it; scaffold the repo; write down how *you* write code. | `STYLE.md`, the published PDFs, the repo skeleton |
| [1. Archive check](stages/01_archive_check.md) | Fetch and verify the deposit; run it as shipped. | `original_manifest.csv`, `download_original.R`, `archive_run_status.csv`, `archive_overwrites.csv` |
| [2. Ground truth](stages/02_ground_truth.md) | Write down every number the paper prints; compare each with the archive and the rewrite. | `<paper_id>_ground_truth.csv`, `float_coverage.csv` |
| 3. Maintained rewrite | Rewrite the code: one script per table or figure, current packages, no published number as an input. | `maintained/`, `maintained/output/` |
| 4. Claims | Extract every claim in the text, numeric or not, and check each one a second way. | `published_claims.csv`, `in_text_claims.R` |
| 5. Errata | Write up every error, with corrections computed at render; decide which, if any, need a journal notice. | `errata.qmd`, `<paper_id>_errata.pdf`, `errata_entries.csv` |
| 6. Report and publish | Render the README, publish the repo, archive it, link the deposit back, schedule the check. | `README.qmd`, a DOI, a scheduled check |

Stages 1 and 2 are written before the rewrite because the rewrite is judged against them. The ground truth starts from the article, not from the code, so that nothing the article prints can escape the comparison by being absent from the pipeline.

## What it costs

From the 40 papers in our collection, which ranged from short research notes to a book:

- **Agent time.** 773 commits over 49 working days, falling in 174 distinct clock-hours; the median paper had commits in 15 distinct hours, the range 5 to 24. Commit-hours are a rough proxy for how long an agent was working, not a measure of it.
- **Your time.** Reading the errata, deciding how serious each one is, and finding the materials that settle questions the deposit cannot. For most papers this took about 15 minutes; for the hardest five, about two hours each. That is roughly 19 hours for 40 papers.
- **Compute.** Most pipelines run in minutes. The slowest, a large simulation study, took about 14 hours on a laptop.

The first papers took far longer than the last ones, because the procedure was being invented as it went. Following a written procedure should be faster.

## What it finds

Across the 40 papers, 322 of 17,354 printed claims (1.9%) were wrong, 33 of the 40 papers printed at least one wrong number, and every one printed an error of some kind. Most errors were small: a stale number in the text, a rounding slip, a mislabeled panel. One changed a conclusion and was corrected in the journal. Expect to find errors in your own work, and decide in advance that finding them is the point.

## Language

The stages, schemas, gates, and decision rules do not depend on a programming language. The templates and the examples are in R, because our papers were. [`languages.md`](languages.md) maps each R tool to its Stata and Python counterparts. For claim checking, the verdict rules in Stage 4 are the specification; the R package `excheckr` is one implementation of them, and they can be reimplemented in any language.

## Repository layout

- `stages/`: one file per stage, each with its purpose, inputs, outputs, gate, and decision rules.
- `schemas/`: the column definitions and closed vocabularies for every output table.
- `rules/`: the judgments that recur (what counts as an erratum, rounding, simulation noise, severity).
- `templates/`: starting files for a new repo.
- `agent/`: the same stages as instructions for a coding agent.
- `traps.md`: failures that will happen to you, with the fix for each.
- `languages.md`: R, Stata, and Python counterparts.
- `examples/`: finished repositories, and an example `STYLE.md`.

## License

CC0. Copy anything.

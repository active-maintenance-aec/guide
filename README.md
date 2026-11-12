# Active maintenance: a guide

In 2021, Limor Peer, Lilla Orr, and I proposed that researchers "actively maintain" their replication archives, updating the code as the software around it changes, so that published results stay reproducible for years rather than months (Peer, Orr, and Coppock 2021, *PS: Political Science & Politics*). For a long time, none of us did it, because it was a lot of work. With AI coding agents the work became cheap enough that I went back and did it for my published books and articles. This repository records how we did it, in enough detail that you could do the same for your own papers.

The guide is written for people. Each stage also has a companion file in `agent/` that says the same thing as instructions a coding agent can follow. If the two ever disagree, the version written for people is the one we meant.

## What a finished repository does

Each paper ended up with its own public repository that:

1. fetches the original deposit from its archive and checks every file against a checksum manifest (the data stay where they were deposited, and are never copied into the repository);
2. records which of the deposited scripts still run;
3. holds a maintained rewrite that reproduces every table, figure, and number in the text from the deposited data, on current software;
4. holds a *ground truth*, one generated table that compares each printed number with what the original code produces and with what the rewrite produces;
5. checks every claim in the text a second, independent way, by quoting the sentence and recomputing its number; and
6. publishes an itemized errata note, whose corrected values the code computes rather than someone typing them in.

Each repository then got a permanent DOI from Zenodo, a link back from the original deposit, and a scheduled job that reruns the whole pipeline every eight weeks, so that we hear about it when a package update moves a number.

## The stages

| Stage | What happens | What it produces |
|---|---|---|
| [0. Setup and style](stages/00_setup.md) | Gather the paper and anything else that can settle a question about it; set up the repository; write down how you like your code written. | `STYLE.md`, the published PDFs, the repository skeleton |
| [1. Archive check](stages/01_archive_check.md) | Fetch and verify the deposit, and run it as it was shipped. | `original_manifest.csv`, `download_original.R`, `archive_run_status.csv`, `archive_overwrites.csv` |
| [2. Ground truth](stages/02_ground_truth.md) | List every number the paper prints, and compare each with the archive and the rewrite. | `<paper_id>_ground_truth.csv`, `float_coverage.csv` |
| [3. Maintained rewrite](stages/03_rewrite.md) | Rewrite the code, one script per table or figure, on current packages. | `maintained/`, `maintained/output/` |
| [4. Claims](stages/04_claims.md) | Extract every claim in the text, numeric or not, and check each one a second way. | `published_claims.csv`, `in_text_claims.R` |
| [5. Errata](stages/05_errata.md) | Write up each error with a computed correction, and decide which, if any, belong in a journal notice. | `errata.qmd`, `<paper_id>_errata.pdf`, `errata_entries.csv` |
| [6. Report and publish](stages/06_publish.md) | Render the README, publish and archive the repository, link the deposit to it, and schedule the check. | `README.qmd`, a DOI, a scheduled check |

The archive check and the ground truth come before the rewrite because the rewrite is judged against them. The ground truth also starts from the article rather than from the code, for a reason Stage 2 explains: a number the pipeline never computes would otherwise never be compared with anything.

## What it cost

Our papers ranged from two-page research notes to a book, and the cost varied with them:

- **Agent time.** Most of the work is done by the agent. A typical paper took a handful of working sessions spread over a few days; a long paper with a large appendix took several times that.
- **My time.** For most papers, about 15 minutes to read the errata and decide what to do about them. For the hardest few, about two hours each, mostly spent weighing how serious an error was and digging up old files that could explain it.
- **Compute.** Most pipelines run in a few minutes. Our slowest, a large simulation study, takes most of a day on a laptop.

The early papers took far longer than the later ones, because we were working out the procedure as we went. With the procedure written down, a new paper should go faster.

## What it found

Errors turned out to be common. A small share of all the claims our papers print were wrong, but most of the papers printed at least one wrong number, and nearly all of them had a mistake of some kind once typos and reference errors are counted. Most errors were small: a number in the text left over from an earlier draft, a value rounded the wrong way, two panels of a figure in the wrong order. Errors that change a conclusion were rare, and when we found one we sent a corrigendum to the journal. If your experience is like ours, you will find errors too.

## Languages other than R

Our papers were written in R, so the templates and examples are in R. The stages, the table formats, the checks, and the rules for judging errors are not tied to R, and [`languages.md`](languages.md) lists the Stata and Python counterparts of the R tools we used. Stage 4 describes how each claim gets its verdict; the R package `excheckr` implements those rules, and nothing stops anyone from implementing them in another language.

## What is in this repository

- `stages/`: one file per stage, with its purpose, inputs, outputs, checks, and the judgment calls it involves.
- `schemas/`: the columns and allowed values of every table the procedure produces.
- `rules/`: the judgments that kept coming up (what counts as an erratum, rounding, simulation noise, and when an error needs a journal notice).
- `templates/`: starting files for a new repository.
- `agent/`: the stages as instructions for a coding agent.
- `traps.md`: problems we ran into more than once, and how we got around them.
- `languages.md`: Stata and Python counterparts of the R tools.
- `examples/`: finished repositories from our collection, and an example `STYLE.md`.

## License

CC0. Take whatever is useful.

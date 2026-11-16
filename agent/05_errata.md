# Stage 5 for agents: errata

Source of truth: [`stages/05_errata.md`](../stages/05_errata.md). Schema: [`errata_entries.md`](../schemas/errata_entries.md). Rules: [`erratum.md`](../rules/erratum.md), [`severity.md`](../rules/severity.md).

## Goal

One itemized errata note per paper, rendered to PDF, with every corrected value computed at render time, and a matching `errata_entries.csv`.

## Do

1. Draft an entry for every error the earlier stages found, and for errors found by reading the article against itself, its appendix, its code, its references (checked against Crossref), and any earlier correction.
2. For each entry, set `class`, `source`, and `form`; quote the published passage and write the corrected one, marking each changed span `[[like this]]`; write a note explaining what was wrong and what the correction rests on; and list the `claim_ids` it corrects.
3. Compute every corrected value from the rewrite's output when `errata.qmd` renders.
4. Make the render check that: every claim id exists; only `quantity` entries carry corrected values, one per id; every corrected value appears in the corrected passage; no corrected value renders identically to the published one at the printed precision; and no entry corrects a claim the pipeline reproduces.
5. Check every quotation against an image of the published page.
6. Order the entries by severity, most serious first, and propose which entries, if any, change a conclusion and which meet the bar for a corrigendum.

## Do not

- Include differences within simulation noise, findings you could not judge, or analysis choices.
- Type a corrected value.
- Quote from extracted PDF text without checking the page image.
- Renumber entries once the note is public. Add new entries at the end.
- Decide whether a conclusion changes, or whether anything goes to a journal.

## Stop and ask the author

- Before finalizing the list of entries: the author decides which candidates are errors.
- For every entry that might change a conclusion.
- Before anything is sent to a journal or to coauthors.

## Done when

`errata.qmd` renders without error, every corrected value is computed, every quotation has been checked against the published page, the render's checks pass, and every `paper_internal` row in the ground truth has a disposition.

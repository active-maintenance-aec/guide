# Stage 5: Errata

Every error the earlier stages turn up is written up in one itemized errata note per paper, rendered to a PDF that sits at the top of the repository and, in our case, also on my website. The corrected values in it are computed by the code at the time the note is rendered, so if a package update ever moves a number, the errata move with it.

## What counts as an erratum

We counted any statement printed in the article, its appendix, or its references that is wrong, however small. That includes:

- a wrong number, or a number left over from an earlier draft;
- a value rounded the wrong way at the printed precision (the text printed 0.23 for a value of 0.2230);
- a description of a method, sample, or variable that doesn't match what was done;
- a label, a legend, or a panel order that is wrong;
- a cross-reference to the wrong table;
- spelling and typesetting mistakes;
- reference-list errors, which were common (much of my early bibliography came from search-engine citations that were themselves wrong).

We left out three things. A value that differs from our computation only within the estimator's own noise is not an error (see [`rules/stochastic.md`](../rules/stochastic.md)). A finding we couldn't judge either way is recorded as `unresolved` in the ground truth rather than corrected. An analysis choice we would now make differently is not an error at all (see [`rules/erratum.md`](../rules/erratum.md)).

When the prose disagreed with the paper's own table and our computation supported the table, we corrected the sentence to match the table.

## The note

`errata.qmd` renders `<paper_id>_errata.pdf` and writes `errata_entries.csv`, one row per entry:

`entry, class, source, form, title, location, published, corrected, note, claim_ids, corrected_values, values_in_spans`

- `class` says what kind of error it is: `quantity`, `description`, `interpretation`, `definition`, `label`, `float`, `cross_reference`, `wording`, `spelling`, `typography`, or `bibliographic`.
- `source` says how we found it: `pipeline` (the rewrite computed a different value), `reading` (reading the article against itself, its appendix, and its code), `reference_audit` (checking every reference against Crossref), `publisher_record` (an earlier published correction), `authors_archive` (our own files outside the deposit), or `proof` (the proofs or accepted manuscript).
- `form` is `full` (the published and corrected passages, quoted in full), `brief` (a one-line correction), or `note` (an explanation with no replacement text).
- `published` and `corrected` quote the passage before and after, with the changed values marked; `claim_ids` ties each entry to rows in the ground truth and the claims file.

Each entry's corrected values are computed from the rewrite's output when the note renders. The build checks that every claim an entry names exists, that only `quantity` entries carry corrected values, that every corrected value appears in the corrected text, and that no entry "corrects" a claim the pipeline reproduces. One rule caught several mistakes of ours: a corrected value must never render identically to the published one at the printed precision, because then there is nothing to correct.

Entries are numbered by severity, with the errors that matter most first, and once a note is public its numbering only grows: new entries are added at the end, so that anyone citing "entry 3" keeps pointing at the same thing.

Every quotation in the note was checked against an image of the published page. Text extracted from a PDF can drop characters, merge columns, or mangle symbols, and an erratum that misquotes the article is itself an error.

## Whether a conclusion changes

The pipeline can tell you that a number is wrong. Whether that changes a conclusion of the paper is a judgment, and we left it to the authors. When an entry did change a conclusion, the note says so plainly at the top.

## Which errors go to the journal

Most of the errors we found were embarrassing but trivial, and the scientific contribution of each paper stands without them. Sending dozens of journals a correction for every typo and rounding slip would bury the editors and devalue corrections as a signal. We used three tiers:

1. **Every error** goes in the errata note, beside the maintained code, where anyone reading the repository will find it.
2. **An error that changes the direction or implications of a finding a reader would rely on** also goes to the journal as a corrigendum, whether or not the finding appears in the abstract. In our experience, errors that meet this bar are rare.
3. **Retraction** is for findings that can no longer be relied on at all.

When a corrigendum was warranted, we used it to correct the related errors in the same article as well. The reasoning behind the tiers is in [`rules/severity.md`](../rules/severity.md), and the `disposition` column in the ground truth records which tier each error landed in.

## Done when

`errata.qmd` renders without error, every corrected value is computed rather than typed, every quotation has been checked against the published page, the build's checks pass, and every `paper_internal` row in the ground truth has a disposition.

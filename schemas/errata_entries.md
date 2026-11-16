# `errata_entries.csv`

One row per entry in the errata note. `errata.qmd` writes this table when it renders the note, so the table and the PDF always say the same thing ([Stage 5](../stages/05_errata.md)).

`entry, class, source, form, title, location, published, corrected, note, claim_ids, corrected_values, values_in_spans`

| Column | Type | Meaning |
|---|---|---|
| `entry` | integer | The entry's number in the note. Numbered by severity at first publication, then append-only. |
| `class` | closed | What kind of error it is. |
| `source` | closed | How we found it. |
| `form` | closed | How the note presents it. |
| `title` | text | A short heading for the entry. |
| `location` | text | Where the error is printed: main text, a section, a float, a footnote, an appendix section, or the references. |
| `published` | text | The passage as printed, with each changed span marked `[[like this]]`. |
| `corrected` | text | The passage as it should read, with the same spans marked. Corrected values in it are computed when the note renders. |
| `note` | text | The explanation: what was wrong, why, and what the correction rests on. |
| `claim_ids` | text | The ground-truth and extraction rows the entry corrects, separated by semicolons; empty for an entry with no row. |
| `corrected_values` | text | One corrected value per id in `claim_ids`, in the same order, separated by semicolons. Only `quantity` entries carry them. |
| `values_in_spans` | logical | `TRUE` when every corrected value is the token the corrected sentence prints; `FALSE` when a value is stored on the claim's scale rather than the sentence's (a proportion printed as a percentage, say); `NA` for an entry with no values. |

## Allowed values

**`class`**

| Value | Meaning |
|---|---|
| `quantity` | A wrong number. |
| `description` | A method, sample, or variable described differently from what was done. |
| `interpretation` | A conclusion that does not follow once the estimates are corrected. |
| `definition` | A wrong definition, display, or proof step. |
| `label` | A wrong axis label, legend, or panel title. |
| `float` | A float that is wrong as a whole, such as panels in the wrong order. |
| `cross_reference` | A pointer to the wrong table, figure, or section. |
| `wording` | A wrong word that changes no number or substance. |
| `spelling` | A misspelling, including of a name. |
| `typography` | A typesetting error. |
| `bibliographic` | An error in the reference list. |

**`source`**

| Value | Meaning |
|---|---|
| `pipeline` | The rewrite computed a different value. |
| `reading` | Reading the article against itself, its appendix, and its code. |
| `reference_audit` | Checking every reference against Crossref. |
| `publisher_record` | An earlier published correction. |
| `authors_archive` | The authors' own files outside the deposit. |
| `proof` | The proofs or the accepted manuscript. |

**`form`**

| Value | Meaning |
|---|---|
| `full` | The published and corrected passages, quoted in full. |
| `brief` | A one-line correction. |
| `note` | An explanation with no replacement text. |

## Checks the render runs

- Every id in `claim_ids` exists in the ground truth or the extraction.
- Only `quantity` entries carry `corrected_values`, and there is one value per id.
- Every corrected value appears in the corrected passage (or `values_in_spans` says why not).
- No corrected value renders identically to the published one at the printed precision, since then there is nothing to correct.
- No entry corrects a claim the pipeline reproduces.
- Every quotation in `published` has been checked against an image of the printed page.

The ground truth's `corrected_here` disposition is computed from `claim_ids`, which is why this table carries them.

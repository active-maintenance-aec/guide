# `ground_truth/archive_overwrites.csv`

One row per file that running the archive created, changed, or removed, in either pass ([Stage 1](../stages/01_archive_check.md)). We found these by comparing every file's checksum and modification time with the manifest after each run.

`pass, file, effect, matches_deposit`

| Column | Type | Meaning |
|---|---|---|
| `pass` | closed | `as_shipped` or `stripped`, as in [`archive_run_status.md`](archive_run_status.md). |
| `file` | text | The file's path within the deposit. |
| `effect` | closed | What the run did to the file. |
| `matches_deposit` | logical | Whether the file the run wrote is byte-identical to the deposited one; `NA` for an added or withheld file, which has nothing to compare with. |

## Allowed values of `effect`

| Value | Pass | Meaning |
|---|---|---|
| `added` | either | The run wrote a file the deposit does not contain. |
| `overwritten` | `as_shipped` | The run rewrote a file the deposit shipped. |
| `rebuilt` | `stripped` | The run regenerated an intermediate file that had been removed for the stripped pass. |
| `withheld` | `stripped` | An intermediate file removed for the stripped pass that the run did not rebuild. |
| `deleted` | either | The run removed a deposited file. |

## Reading it

`overwritten` or `rebuilt` with `matches_deposit = FALSE` is the informative row. It means the deposited code, run today, does not produce the file the authors deposited: either the deposited file came from different code than the code that was deposited, or the software has moved since. The ground truth then has to say which ([Stage 2](../stages/02_ground_truth.md)).

`withheld` marks an intermediate that no deposited script produces. Any script that reads it can only run in the as-shipped pass, which leans on a file nobody can regenerate.

A deposit that could not be run writes this table with a header and no rows.

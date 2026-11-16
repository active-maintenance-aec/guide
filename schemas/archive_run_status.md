# `ground_truth/archive_run_status.csv`

One row per deposited script per pass: what happened when we ran the archive ([Stage 1](../stages/01_archive_check.md)).

`pass, script, role, exit_status, outcome, stopped_at`

| Column | Type | Meaning |
|---|---|---|
| `pass` | closed | Which copy of the deposit the script ran in. |
| `script` | text | The script's path within the deposit. |
| `role` | closed | What the script does. |
| `exit_status` | integer | The process exit status; `0` is success, `NA` if the script was not run. |
| `outcome` | closed | How the run ended. |
| `stopped_at` | text | The error message (or the first lines of it) where the script stopped; for `not_run`, the reason it was not run; `NA` for a clean run. |

## Allowed values

**`pass`**

| Value | Meaning |
|---|---|
| `as_shipped` | The deposit exactly as downloaded, intermediate files and all. |
| `stripped` | Only the raw data and the code, with every intermediate file the deposit shipped removed, so that each script has to rebuild what it reads. |

The table is long: a script run in both passes has two rows.

**`role`**

| Value | Meaning |
|---|---|
| `cleaning` | Turns raw data into analysis data. |
| `analysis` | Produces tables, figures, or reported numbers. |
| `other` | Anything else the deposit runs directly. |

A helper file that is only ever sourced by other scripts gets no row, since it never runs on its own.

**`outcome`**

| Value | Meaning |
|---|---|
| `clean` | Ran to the end without error. |
| `error` | Stopped with an error. |
| `timeout` | Did not finish in the time allowed. |
| `not_run` | Not run, for a reason given in `stopped_at` (it needs Stata, say, or a proprietary dataset). |

## What this table does not say

`clean` means the script ran. Whether it reproduced the paper's numbers is a separate question, answered by the ground truth. A script can run cleanly and reproduce nothing, and a script that errors halfway through can still have printed the numbers we needed. The table answers the first question only.

A deposit we could not run at all still writes this table, with one `not_run` row per script.

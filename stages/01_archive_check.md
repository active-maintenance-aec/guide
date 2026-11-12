# Stage 1: Archive check

**Purpose.** Pin down exactly what the deposit contains, and find out whether its code still runs, before writing a line of the rewrite.

Two questions get two separate answers in this stage and the next. *Does the archive run?* is answered here, by executing it. *Does the archive reproduce the paper?* is answered in Stage 2, by comparing what it produces with what the paper prints. An archive can run cleanly and reproduce nothing, or fail on its first line and reproduce everything once the failure is fixed. Keep the two apart in your notes and in your README.

## 1.1 The manifest and the download script

Write `original_manifest.csv`, one row per deposited file, from the archive's own API, never by hand. For Dataverse:

`file, directory_label, dataverse_file_id, file_persistent_id, bytes, md5_served, md5_published, unf, served_as`

For OSF:

`file, directory_label, osf_file_id, bytes, md5_served, md5_published, sha256_published`

`md5_served` is the checksum of the bytes the archive actually sends you; `md5_published` is the checksum the archive's metadata declares. They usually agree. When they do not (Dataverse converts some tabular uploads, and serves the converted file unless you ask for the original), record both and request the original format.

Then write `download_original.R` (or its equivalent), which:

1. downloads every file in the manifest into `original/`, which is git-ignored;
2. **stops** if any file's size or served checksum differs from the manifest;
3. prints, but does not stop on, a disagreement with the published checksum;
4. **stops** if `original/` contains any file the manifest does not list, including hidden files;
5. unpacks any zip or RAR archive into a separate, regenerated folder, and verifies its members against a second manifest.

The entry point runs this script first. It is the only check in the pipeline with a deadline: if a deposit ever fails verification, either the archive changed the files, released a new version, or withdrew them, and the time to find out which is the day it happens. Your manifest is then the only public record of what the deposit held.

## 1.2 Run the archive as shipped

Run each deposited script, in a scratch copy of the deposit and never in place, and record what happened:

`ground_truth/archive_run_status.csv`: `pass, script, role, exit_status, outcome, stopped_at`

- `pass` is `as_shipped` (the deposit exactly as downloaded) or `stripped` (only the raw data and the code, with every intermediate file the deposit included removed). Run both. A deposit that ships its own intermediates can make a script look healthy when the script that should have produced those intermediates is broken; the stripped pass shows it.
- `role` is `cleaning`, `analysis`, `helper`, or `other`.
- `outcome` is `clean`, `error`, `timeout`, or `not_run`. An archive you cannot run (it needs software you do not have) still gets rows, with `outcome = not_run` and the reason in `stopped_at`.

Run under the conditions of the paper's day where they matter. In R, the default random-number sampler changed in version 3.6.0 (April 2019); for code written before then, set `RNGkind(sample.kind = "Rounding")` when checking whether the archive reproduces its own published draws. The maintained rewrite in Stage 3 uses the current default, and records any number that moves as a consequence (see the `environment` locus in [Stage 2](02_ground_truth.md)).

## 1.3 What the run writes

Before running, search the deposited code for write calls (joining continuation lines first, since a call split across lines is easy to miss). After running, compare every file's modification time and checksum against the manifest, and record what changed:

`ground_truth/archive_overwrites.csv`: `pass, file, effect, matches_deposit`

`effect` is `added`, `overwritten`, `rebuilt`, or `deleted`; `matches_deposit` says whether an overwritten or rebuilt file came out identical to the deposited one. A run that overwrites a deposited output with something different is a finding: either the deposited output came from different code, or the environment has moved. Running in a scratch copy is what makes this table possible, and what keeps a run from silently altering the evidence.

## 1.4 Diagnose, but do not fix, the archive

Record why each failing script fails. Do not edit the deposit to make it run; the deposit is the published record, and its failures are part of what you are documenting. Common causes, roughly in order of frequency: a function removed or renamed in a package update; a package that no longer installs; a hard-coded absolute path; a missing file the authors never deposited; a dependency on an intermediate the code does not create. A deprecated-function warning is a hypothesis about the cause, not a diagnosis; check it.

## Gate

The manifest verifies, the download script stops on any mismatch, and every deposited script has a row in `archive_run_status.csv` for each pass.

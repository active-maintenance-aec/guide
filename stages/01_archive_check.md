# Stage 1: Archive check

In this stage we pinned down exactly what each deposit contains and found out whether its code still runs, before starting the rewrite.

It helped to keep two questions apart. *Does the archive run?* is answered here, by executing it. *Does the archive reproduce the paper?* is answered in Stage 2, by comparing what it produces with what the paper prints. The two come apart more often than you might expect: some of our archives ran cleanly and reproduced little, and others failed on the first line yet reproduced everything once that line was fixed.

## The manifest and the download script

For each deposit we wrote `original_manifest.csv`, one row per file, from the archive's own API rather than by hand. For Dataverse:

`file, directory_label, dataverse_file_id, file_persistent_id, bytes, md5_served, md5_published, unf, served_as`

For OSF:

`file, directory_label, osf_file_id, bytes, md5_served, md5_published, sha256_published`

`md5_served` is the checksum of the bytes the archive actually sends, and `md5_published` is the checksum in the archive's metadata. They usually agree. They don't when Dataverse has converted a tabular upload to its own format and serves the converted version by default; in that case we recorded both and asked for the original format.

Then `download_original.R`:

1. downloads every file in the manifest into `original/`, which git ignores;
2. stops if any file's size or served checksum differs from the manifest;
3. prints, without stopping, any disagreement with the published checksum;
4. stops if `original/` contains a file the manifest doesn't list, hidden files included;
5. unpacks any zip or RAR file into its own regenerated folder and checks the contents against a second manifest.

`run_all.R` runs this script first. It's the one check in the whole pipeline that comes with a deadline. If a deposit ever stops verifying, the archive has changed the files, released a new version, or withdrawn the deposit, and the sooner you find out which, the better. At that point the manifest may be the only public record of what the deposit held.

## Running the archive as shipped

We ran each deposited script in a scratch copy of the deposit (never in the downloaded folder itself) and recorded what happened in `ground_truth/archive_run_status.csv`:

`pass, script, role, exit_status, outcome, stopped_at`

- `pass` is `as_shipped` (the deposit exactly as downloaded) or `stripped` (only the raw data and the code, with any intermediate files the deposit included removed). We ran both, because a deposit that includes its own intermediate files can make a script look fine when the script that should have produced those files is broken.
- `role` is `cleaning`, `analysis`, `helper`, or `other`.
- `outcome` is `clean`, `error`, `timeout`, or `not_run`. Scripts we couldn't run at all (several needed Stata, which we didn't have) still got rows, with `not_run` and the reason in `stopped_at`.

Where it mattered, we ran under the conditions of the paper's day. R changed its default random-number sampler in version 3.6.0 (April 2019), so for older code we set `RNGkind(sample.kind = "Rounding")` when checking whether the archive reproduced its own published draws. The rewrite uses the current default, and any number that moves because of it is recorded as an `environment` difference (see [Stage 2](02_ground_truth.md)).

## What the run writes

Before running, we searched the deposited code for anything that writes a file, joining lines first, since a write call split across two lines is easy to miss. After running, we compared every file's modification time and checksum with the manifest and recorded what had changed in `ground_truth/archive_overwrites.csv`:

`pass, file, effect, matches_deposit`

`effect` is `added`, `overwritten`, `rebuilt`, or `deleted`, and `matches_deposit` says whether a file the run rewrote came out identical to the deposited one. When a run overwrote a deposited output with something different, that told us something: either the deposited output came from different code than what was deposited, or the software had moved. Running in a scratch copy is what made this table possible, and it also kept the runs from quietly altering the deposit we were trying to document.

## Diagnosing failures

When a script failed, we recorded why, and left the deposit as it was: the deposit is the published record, and its failures are part of what we were documenting. The causes we saw most often, roughly in order: a function removed or renamed in a package update; a package that no longer installs; an absolute path from the author's computer; a file the authors never deposited; and a script that depends on an intermediate file no deposited script creates. We learned to treat a "deprecated function" warning as a hypothesis about the cause; several times it turned out not to be the real problem.

## Done when

The manifest verifies, the download script stops on any mismatch, and every deposited script has a row in `archive_run_status.csv` for each pass.

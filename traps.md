# Traps

The failures we hit more than once, or hit once at real cost, with what we did about them. Most are silent: the code runs, the checks pass, and the answer is wrong. They are grouped by the stage where they bite. The examples are R, because our code was R; the shapes carry over to any language (see [`languages.md`](languages.md)).

## Fetching and running the archive

- **Running the archive in place.** A deposited script that saves a figure to a bare relative path overwrote a file the deposit ships, so the working copy no longer matched the archive, and the checksum check passed only because it had run first. Run every deposited script in a scratch copy, never in the downloaded folder.
- **Write calls split across lines.** A search for code that writes files misses a `write.csv(` whose file argument is on the next line. Join continued lines before searching.
- **Shipped intermediates.** A script ran cleanly against the deposit as downloaded while the script that should have produced its input had failed; it was reading the deposited copy. One deposit went from "four of six scripts run" to "five of six fail" once its intermediates were removed. Run a second pass on a copy stripped to raw data and code ([`schemas/archive_run_status.md`](schemas/archive_run_status.md)).
- **The archive that runs and writes nothing.** One deposit had every write commented out, so it ran without error and left nothing to compare. A clean exit is not evidence of anything; check what the run produced.
- **Printing nothing.** In R, `source()` prints nothing unless told to (`print.eval = TRUE`), so a harness that sources the deposited scripts records exit statuses correctly while capturing an empty log. We concluded that no archive values were recoverable from one paper until we turned printing on and recovered over a hundred. A deposit that builds a table object and comments out the print call can still be made to print it.
- **A single container file.** When the deposit is one zip or RAR, the "no unlisted files" check runs on a folder holding one file and checks nothing. Unpack into a folder of its own and check the members against a second manifest.
- **A reason for skipping work that was never tested.** We skipped one analysis because its package was "unmaintained"; it had been updated the day before, and installing it surfaced the paper's only real reproducibility failure. Three other packages we had recorded as removed turned out to install and run. Test the reason before accepting it.

## Software that changed underneath the code

- **Dispatch drift.** A test function from one package, given a model fit from another, used to fall through to a classical test. A later version of the second package added the method it was looking for, and the identical line began returning a robust test: 17 of 18 cells in one table moved, with no error or warning. Nothing but comparison with the printed numbers catches this. Expect it wherever deposited code combines two packages.
- **A package that changes another package on load.** Loading one package replaced fourteen functions in base R and `stats`, and broke an unrelated package's estimator for the rest of the session. To find such a package, record every function in the loaded namespaces, attach the deposit's packages one at a time, and see which attach changes something. Bisecting by the failure finds only the first culprit.
- **The random-number sampler.** R 3.6.0 changed how `sample()` draws. Seeded code from before April 2019 needs `RNGkind(sample.kind = "Rounding")` to reproduce itself ([`rules/stochastic.md`](rules/stochastic.md)), and the setting has to be restored explicitly afterwards, since `on.exit()` does not reliably restore it when scripts are sourced in sequence.
- **Sort order.** dplyr 1.1 sorts character keys in the C locale by default, which puts every capitalised word ahead of every lowercase one. Every value stayed correct and the rows moved, and a cell-by-cell comparison against the published table reported 172 of 717 cells wrong when none were. Pass the locale explicitly, or compare by key rather than by position.
- **Weights that quietly disappear.** Refitting a weighted model from its own `model.frame()` drops the weights, which pairs weighted coefficients with unweighted standard errors; it moved one coefficient's sign. Pass the weights explicitly.

## Writing the rewrite

- **A modern equivalent that is not equivalent.** Replacing base R's `expand.grid()` with tidyr's `expand_grid()` transposed a grid, because the two vary their arguments in opposite orders. Every number still matched; only the figure was wrong, and it stayed wrong for months until someone laid the rendered figure beside the published one. Compare every figure by eye, as well as its numbers.
- **Factor order in a deposited data file.** A treatment variable stored as a factor whose first level was a treatment arm, not the control, reversed the sign of every contrast taken without releveling. The standard errors looked normal, the script ran cleanly and deterministically, and only the comparison with the published numbers caught it. Set the reference level explicitly.
- **A column name that shadows an argument.** A helper written `mutate(outcome = outcome)` on a table that already had an `outcome` column assigned the column to itself, so the labels were wrong while every cell was right, and a later filter silently dropped a whole experiment. Name arguments so they cannot collide with columns.
- **A script that skips its own work.** An `if (file.exists(out))` guard returns the committed output instead of recomputing it, so the run passes while the code may be broken ([Stage 3](stages/03_rewrite.md)).
- **An output file that exists is not a render that worked.** A loop that checked for `README.md` passed on stale files after a column rename had broken three reports. Check the exit status.
- **Unseeded draws.** A pipeline with an unseeded random draw gives a different answer on the second run, and nothing downstream means anything until it is fixed. Run everything twice and diff the outputs.

## Building the ground truth

- **The printed value read as a number.** A CSV reader that guesses types turns "0.80" into 0.8 and "-0.00" into 0, and the precision needed for the comparison is gone. Force the column to text, and check that the file on disk still stores the string ([`rules/rounding.md`](rules/rounding.md)).
- **Hand-typed comparison values.** A typed number that agrees with a note looks exactly like a computed number that agrees with the data. One repository had a typed coverage count of 11 a few lines below code that would have said 3. Generate everything except the printed values.
- **Selecting a row by the number you expect.** Filtering pipeline output for the value the page prints guarantees a match. Select by key.
- **Joins that match nothing.** A join on a column that was missing for two of the studies left 72 of 130 rows unmatched, and the table read as if nothing were wrong. Route every join through one helper that checks keys are unique on both sides and the result is one-to-one.
- **Building from the pipeline instead of the article.** A ground truth built from what the rewrite produces cannot see what the rewrite does not produce. One paper's first ground truth had 40 rows, all matching, covering little more than a third of the paper. Start from the printed page.
- **"At least one row per float."** A figure with one checked value out of more than a hundred printed passed that test for months. Report coverage as a fraction for each float ([`schemas/float_coverage.md`](schemas/float_coverage.md)).
- **Rounding a value before comparing it.** A value stored as 0.0115 rounds to 0.011, while the full-precision 0.01150090 rounds to the printed 0.012. Compare from full precision.

## Reading the published article

- **PDF text extraction.** Text pulled from a PDF changes characters silently. In one paper `=` came out as `5` and the minus sign as `2`, so a printed −1.5 arrived as 21.5. Multi-column regression tables were mis-aligned by a column, which produced a phantom erratum that survived two reviews. Check every quoted sentence and every transcribed cell against an image of the page, and read numbers printed on a figure by position rather than in reading order.
- **Numbers written as words.** A sweep for digits misses "five successive elections" and "in all but one study". Run a second pass for number words.
- **The preprint.** A preprint's numbers are not the published numbers. Transcribe from the published version.
- **Testing a document against the wrong materials.** A corrigendum restated one paper's original confidence intervals differently from the article's appendix. We first wrote that up as an error in the corrigendum. It was not: the corrigendum had redrawn the original analysis from its own working files, whose inputs differed, and on those inputs it was right. Check a printed number under the conditions of the document that printed it.

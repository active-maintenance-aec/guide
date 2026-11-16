# Stage 3: Maintained rewrite

The rewrite is new code that reproduces every table, figure, and number in the paper from the deposited data, on current software, written the way `STYLE.md` describes. It is the part of the project that keeps the paper usable: when a package changes next year, this is the code that gets updated.

## Shape

We wrote one script per table or figure, named for what it produces, with cleaning kept separate from analysis and shared functions in a single `maintained/helpers.R`. Every script writes to `maintained/output/`. Next to each figure we also save a CSV of every quantity it plots, because a figure file can't be compared with anything, while a CSV of its points can. Tables are written both formatted and unrounded, so that later stages compare full-precision values rather than what a table package chose to print.

## Three rules we held to

**No published number goes in.** The rewrite computes everything from the deposited data. When a script seemed to need a number from the paper (a threshold, a sample size, a cut point), that was nearly always a sign that the computation upstream of it was missing. The one exception is a number that is itself a claim about the data, such as "fewer than 5 percent of respondents failed the attention check", which a dedicated script checks rather than uses.

**No script skips its own work.** A script that checks whether its output already exists and returns early can pass every test while being broken. Ours always recompute.

**Every "can't be computed" is a claim to test.** Several times a comment in the archive, or in an early draft of our own rewrite, said that some number couldn't be reproduced from the deposit, and it turned out it could. We treated such comments as hypotheses, and checked them.

## Errors versus choices

The rewrite corrects unambiguous coding errors: a typo in a variable name, a wrong index, the wrong column, a covariate left out of a specification the paper describes. It does not revisit analysis decisions. If the paper used a particular estimator, specification, sample, or set of standard errors, the rewrite uses the same one, even where we would now choose differently. A choice we'd make differently today isn't an error, and treating it as one would turn the errata into a second paper.

The line isn't always sharp. One case that came up repeatedly: a regression silently dropped collinear covariates, so the model actually estimated differed from the one the paper describes. We counted that as an error, because the paper's own description says what was intended. When we couldn't tell which of two deposited values the authors meant, we wrote the finding up as a note for the authors to decide, rather than picking one.

Each correction the rewrite makes shows up in the ground truth as a row where the rewrite disagrees with the archive (`match_rewrite = FALSE`, locus `archive`), and in the errata in Stage 5. We were careful not to carry a typo forward into the new code just because the old code had it; the point is that the rewrite is right.

## Software changes

The rewrite uses current packages and the current random-number generator. When either moves a published number, the ground truth records it with the locus `environment`. A few of these surprised us. A function can keep its name and arguments while changing what it computes: one test function, given a regression fit from a newer package, quietly began using a different variance estimator, with no warning. Converting an old grid-building function to its modern equivalent transposed a grid, which showed up only when we laid the new figure beside the published one. We now compare every rendered figure with the published version by eye, in addition to comparing the numbers.

## The same answer twice

We ran `run_all.R` twice from fresh sessions, checked that both runs exited cleanly, and confirmed that the second run left the output folder byte-for-byte unchanged. PDFs embed a creation timestamp, so we blank it when writing figures; otherwise every run "changes" every figure. A pipeline that gives a different answer on the second run has an unseeded random draw or depends on something outside the repository, and both need fixing before the comparisons mean anything.

## Done when

`run_all.R` runs from a clean session, every table and figure in the paper has a script that produces it, no published value is an input, and two runs in a row leave `maintained/output/` unchanged.

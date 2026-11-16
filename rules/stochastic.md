# Numbers that come from random draws

Bootstrap intervals, randomization-inference p-values, simulated power, permutation tests, and anything else built on random draws can print a different number on every run. A difference between such a number and the page is not, by itself, evidence of an error. It is not evidence of no error either, and the rule below exists to keep the second mistake from hiding behind the first.

## First, confirm that something draws

Before putting a difference down to randomness, we checked that the procedure actually draws at random. A `set.seed()` call at the top of a script is not evidence of that. One paper set a seed twice and never drew a random number; its results were identical at any seed. An earlier pass had explained a real mismatch in that paper as bootstrap noise from a function that, on inspection, uses the jackknife, which is deterministic. More than once, a difference that looked like noise was a bug.

The check is cheap: run the procedure at two or three very different seeds. If nothing moves, nothing draws, and the difference needs another explanation.

## Seeded procedures

When the deposited code sets a seed, the archive check in [Stage 1](../stages/01_archive_check.md) tries to reproduce the printed value exactly, under the software of the paper's day. For R, the date that matters most is April 2019: R 3.6.0 changed the default algorithm behind `sample()`, so code that draws with `sample()` and was run before then needs `RNGkind(sample.kind = "Rounding")` to reproduce its own output. We tested the old sampler before concluding that a seeded archive was broken, and it often turned out not to be.

The maintained rewrite keeps the current sampler, because it is the code we would write now. Where the current sampler moves a published number, the ground truth records `defect_locus = environment`. Neither the paper nor the archive is wrong; the software changed underneath them.

Two practical notes. Setting the sampler inside a script and expecting `on.exit()` to restore it does not work reliably when scripts are sourced in sequence from `run_all.R`, so we restored it explicitly and asserted the result. A published number should also be checked under the conditions of the document that printed it: a corrigendum published years after the article may have been computed with different software, or different inputs, from the article it corrects.

## Unseeded procedures

When the deposited code sets no seed, the printed value is a single unlabelled draw, and no run can be expected to match it. We reran the procedure across many seeds (a few hundred was usually enough) and asked whether the printed value was consistent with the resulting distribution. Two illustrations:

- A chi-squared p-value ran from 0.0005 to 0.004 over 500 replications, and about a quarter of the draws rounded to the printed value. The printed value holds.
- The endpoints of a simulated interval were printed as $1.70 and $13.71. Over 200 seeds the endpoints ranged from $1.66 to $1.73 and from $11.79 to $15.19. Both printed values hold.

A printed value far outside any reasonable draw is an erratum. A printed value inside the distribution is not, even when no single run reproduces it.

In the ground truth, such a row leaves `match_rewrite` empty, since there is no single value to match, and records the verdict in `holds`. Filling in `match_rewrite = TRUE` beside a `value_rewrite` that visibly differs would make the row contradict itself. The same encoding applies whatever the claim type: a `pipeline` claim whose printed value comes from an unseeded procedure needs it just as much as a `descriptive` one.

## Unseeded figures

The same problem arises in figures, where it is easier to miss. A figure whose layout depends on random draws (a jittered scatter, simulated intervals, labels placed by a stochastic algorithm) can change with every run. In one paper with no seed, 9 of 20 seeds moved at least one published label. The archive runs without error and still cannot reproduce its own figure, even in principle. Where we found this, we measured how much the figure moved at the printed precision and reported it, rather than calling the figure reproduced or not.

## In the errata

A value inside the distribution is not an erratum and does not appear in the note. Where such a row carries a locus anyway (a seeded value that the current sampler moves, say, but only within the range over seeds), its disposition is `documented_only`, with the range as the reason. A value far outside the distribution is an ordinary erratum, and its corrected value is computed from the rewrite in the usual way, with the seed recorded so that the correction itself reproduces.

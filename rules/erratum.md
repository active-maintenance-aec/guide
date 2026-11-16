# What counts as an erratum

An erratum is a statement printed in the article, its appendix, or its references that is wrong. The [Stage 5](../stages/05_errata.md) list of what that covers is long on purpose: wrong numbers, numbers rounded the wrong way, misdescriptions, bad labels, wrong cross-references, typos, and bad references all count, however small. Most of the work of applying the rule was in the cases at its edges, which this page collects.

## Errors versus choices

The line we drew is between implementation and analysis. An erratum is a place where the paper did not do what it says it did, or says something its own analysis does not support. A choice we would make differently today is not an erratum, however strongly we now prefer the alternative.

Errors, in our usage:

- a typo in a variable name, a wrong index, or the wrong column;
- a standardization that divides by the wrong group's standard deviation;
- a covariate left in (or out of) a specification the paper describes differently, such as wave 2 outcomes copied into a wave 3 model;
- a number in the text left over from an earlier draft of the analysis;
- a sentence that describes the sample, the estimator, or a variable differently from what the code does.

Choices, which we left alone:

- the estimator, the standard errors, and the covariate set the paper used;
- the sample definition, including exclusions we would not make now;
- the outcome scaling, the plotting decisions, and the tables a paper chose to show.

The rewrite keeps every one of those choices (see [Stage 3](../stages/03_rewrite.md)). An errata note that relitigated them would become a second paper, and a reader could no longer tell the mistakes from the second thoughts.

## The gray area: collinear covariates

A regression with collinear covariates is rank-deficient, and the software drops a column to fit it. Which column it drops depends on column order and on the software version, so the printed estimate depends on an accident rather than on a decision anyone made. The paper's own description of the model says what was intended, and the fitted model is not that model. We ruled that these count as errata and corrected them.

## When everything matches and the paper is still wrong

Agreement among the page, the archive, and the rewrite shows consistency, not correctness. A paper can print exactly what its code produced while the code has a bug, and a rewrite written against the archive can inherit the same bug. One paper summed vote shares across merged precincts instead of recomputing them, and every comparison matched. Reading the deposited code, rather than only running it, found that error and others like it. Such an error is still an erratum; in the ground truth it carries the locus `archive` even though every comparison reads `TRUE`.

## The text against its own tables

When a sentence disagreed with the paper's own table and our computation supported the table, we corrected the sentence. When we could not tell which of two deposited values the authors meant (two versions of a variable, say, each defensible), we did not pick one. We wrote the finding up as a note for the authors to decide.

## Approximations

A number the text hedges ("about", "roughly", "nearly", "on the order of") is held to what the hedge could reasonably mean. A number the text states without a hedge is held to its printed digits, even when the true value is close. A sentence that says effects run "between 0.30 and 0.50 standard deviations", about estimates of 0.283 and 0.522, is an erratum: both estimates fall outside the interval as written. The details, including how wide a hedge is allowed to be, are in [`rounding.md`](rounding.md).

## What we left out

- **Differences within simulation noise.** A value from a random procedure that falls inside the distribution of that value over seeds is not an error. See [`stochastic.md`](stochastic.md).
- **Findings we could not judge.** When we looked and could not tell whether the paper was wrong, the ground truth records `defect_locus = unresolved` and the errata say nothing. An erratum we were not sure of would itself be an error.
- **Defects the reader never sees.** A bug in the deposited code that the rewrite repairs but that never reached a printed number is recorded in the ground truth (`documented_only`) and is not an erratum, because nothing on the page is wrong.

## Who decides

The agent proposes and the author decides. Whether a discrepancy is an error or a choice, and whether a correction changes a conclusion, were the author's calls in every case, and for any correction sent to a journal they were the coauthors' calls too. For most papers these decisions took about a quarter of an hour; the hardest took a couple of hours each.

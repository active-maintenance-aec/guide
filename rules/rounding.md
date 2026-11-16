# Rounding

The rule in one sentence: a computed value matches a printed one when, formatted to the precision the page prints, it gives the same digits. Everything below is about applying that rule without fooling yourself in either direction.

## Keep the printed value as a string

A printed number carries its precision in its digits. "0.80" says two decimal places, "0.8" says one, and as floating-point numbers the two are identical. Once a printed value has been read in as a number, the comparison at printed precision can no longer be made, because the precision is gone.

We therefore stored every printed value as the string the page prints, in the extraction and in the committed ground truth, and compared strings: the computed value is formatted with the printed number of decimals (`sprintf("%.2f", x)` in R), and the two strings are compared after the clean-up below. A comparison by numeric tolerance fails in both directions. Too loose a tolerance passed a value that the row's own note said disagreed; values sitting exactly on a rounding boundary were reported as mismatches when they were not.

The string is easy to lose by accident. A CSV reader that guesses column types will read a column of numeric-looking strings as numbers, turning "0.020" into 0.02 and "-0.00" into 0. We forced the column type to character everywhere the printed value is read, and checked that the file on disk still stores the string, since a script can carry the string internally and then write a number at the end.

## Clean-up before comparing

Both sides get the same treatment:

- restore a missing leading zero (".23" becomes "0.23");
- replace a typographic minus sign with a hyphen;
- remove thousands separators;
- treat a negative zero as zero.

A tolerance of `1e-9` absorbs floating-point representation, and nothing else.

## Rounding errors are errors

A value rounded the wrong way at the printed precision is an erratum. The text that prints 0.23 for a value of 0.2230 is wrong at the precision it chose, and so is a value truncated rather than rounded (0.699 printed for 0.6996). These errata are small, and most of them are hand-typed numbers in the body text, where nothing generated them from the code.

The computed side must be compared at full precision. If the rewrite stores a value already rounded (an R-squared kept as 0.0115) and that value is rounded again for comparison, the result can disagree with the page (0.011 against a printed 0.012) when the full-precision value (0.01150090) agrees. Every table in the rewrite is written unrounded beside its formatted version for this reason.

## Hedged numbers

When the sentence itself hedges, we compared within half a step of the sentence's own precision. We treated the following words as hedges: "approximately", "about", "roughly", "around", "nearly", "close to", "on the order of".

- "about 37" tolerates 36.5 to 37.5;
- "about 40 percent" tolerates 35 to 45 percent.

A hedge needs that bound. Our first version of the rule simply returned no verdict for a hedged number, and it hid one paper's largest error: an appendix said one effect was "about 37 percentage points" when the estimate was 29.7, and the hedge exempted it from every check. A hedge excuses a rounding difference, not an arbitrary one.

The hedge has to be on the page. A sentence that states a bare figure or a bare interval asserts it exactly, and the fact that the true value is close is not a defence. An effect described as running "between 0.30 and 0.50 standard deviations", about estimates of 0.283 and 0.522, is an erratum, even though both estimates round to the endpoints at one decimal place.

## Differences of printed cells

When the text reports a difference between two printed values, each value was rounded on its own, so the difference can legitimately be off by one unit in the last printed digit. We allowed exactly that, with the tolerance set slightly wider than one unit so that it never sits on a floating-point boundary. Without that margin, a gap of exactly one unit can fail: 0.8 minus 0.7 computes as 0.10000000000000009, which is not at most 0.1.

## The archive's precision

The deposited code often prints its own output at a fixed precision (a tibble shows three significant digits, a Stata log a few decimals). The archive's value is compared at the coarser of the page's precision and the precision the deposited code printed. Any finer comparison manufactures disagreement between two numbers that agree as far as either was ever printed.

Sometimes rounding twice is the deposit's own convention: a table that rounds to three places and then formats to two prints 0.55 for a rate of 0.5449. The rewrite declines to round twice and computes 0.54, while the archive reproduces the page exactly. We recorded both values and explained in the notes which was which, so that the rewrite's choice did not read as a failure to reproduce.

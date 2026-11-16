# Languages other than R

> **Needs review.** Our code was R, so the R column below is what we used, and the Stata and Python columns are not. We drafted them from each language's documentation, not from running the procedure in it. If you work in Stata or Python and find something wrong or missing, please open an issue.

The procedure does not depend on R. What it needs from a language is a short list of capabilities: build paths from the project root, run everything from one entry point, fix the random-number generator, compute the paper's standard errors, write unrounded output beside every table and figure, verify downloads by checksum, read printed values as text, and format a number at a given precision. This page maps each one.

## Counterparts

| Need | R (what we used) | Stata | Python |
|---|---|---|---|
| Paths from the project root | `here::here()`, anchored by `here::i_am()` | A global set once in the master do-file (`global root "..."`), with every path built from it; no `cd` inside scripts | `pathlib.Path`, anchored at the repository root (for example with `pyprojroot`) |
| One entry point that stops at the first failure | `run_all.R`, sourcing scripts in order | A master `.do` file calling each script with `do`; Stata stops on the first error unless told otherwise | `run_all.py` calling each step with `subprocess.run(..., check=True)`, or a `Makefile` |
| Fixed package versions | `renv` lockfile | Ship the user-written commands in the repository and point `sysdir set PLUS` at them; set `version` at the top of the master file | A pinned lockfile (`requirements.txt` with exact versions, or `uv.lock`) |
| Seeds and the generator | `set.seed()`; `RNGkind(sample.kind = "Rounding")` to reproduce pre-3.6 draws | `set seed`; the generator depends on `version` (`version 13` and earlier give the old KISS generator, later versions Mersenne Twister); `set sortseed` for ties | `numpy.random.default_rng(seed)`, passed explicitly; the legacy `np.random.seed()` and the standard library's `random` keep separate global states |
| Robust standard errors | `estimatr::lm_robust()`, HC2 by default | `vce(robust)` is HC1; `vce(hc2)` and `vce(hc3)` exist for `regress`; `vce(cluster)` is CR1 | `statsmodels` `cov_type="HC2"` (or `HC1`, `HC3`); `cov_type="cluster"` for clustering |
| Unrounded table output | `write_csv()` of the estimates beside the formatted table | `export delimited` or `putexcel` from stored results, beside the `esttab` or `collect` table | `DataFrame.to_csv()` beside `to_latex()` |
| A CSV beside every figure | `write_csv()` of the plotted values next to `ggsave()` | `export delimited` of the plotted variables next to `graph export` | `to_csv()` of the plotted values next to `savefig()` |
| Deterministic figure files | Blank the PDF `CreationDate` and `ModDate` after writing | Check whether `graph export` embeds a date; if it does, compare the CSVs only | `savefig(..., metadata={"CreationDate": None})` for PDF |
| Downloads verified by checksum | `download_original.R`: `curl` then `tools::md5sum()` | `copy` the file, then shell out to a checksum tool; Stata's own `checksum` is a CRC, not MD5 | `requests` and `hashlib.md5()` / `hashlib.sha256()` |
| Printed values read as text | `read_csv(col_types = cols(value_paper = col_character()))` | `import delimited, stringcols(_all)` | `pd.read_csv(..., dtype=str, keep_default_na=False)` |
| A number at the printed precision | `sprintf("%.2f", x)` | `string(x, "%9.2f")` (then trim) | `f"{x:.2f}"` |
| The claims check | `excheckr` | Not yet written | Not yet written |

Two cautions about the table.

**Default standard errors differ across languages.** Stata's `robust` is HC1, `estimatr`'s default is HC2, and `statsmodels` makes you choose. A rewrite in a different language from the original, or a port between packages in the same language, can move every standard error in a paper without anything being wrong in the code. The rewrite keeps the paper's estimator ([Stage 3](stages/03_rewrite.md)), which includes its variance estimator.

**Use the formatting function, not a rounding function.** Rounding functions differ on exact halves across languages (and some round half to even), while a format string applied to the full-precision value is what produces the digits the comparison needs. Whatever you use, test it on values that sit on a rounding boundary.

## The claims check

[Stage 4](stages/04_claims.md) describes the verdicts. Rewriting the check in another language means reproducing this behaviour; `excheckr` is one implementation of it, not the definition.

For each claim in `published_claims.csv` with `needs_block = TRUE`, a block in the claims script computes a value from the rewrite's output and declares it with the claim's id and, where the claim needs one, an expectation (`range`, `derived`, `shape`, or `absent`). The check looks up the claim's printed value and precision in the extraction, and the corrected value from any errata entry whose `claim_ids` name it. It formats the computed value at the printed precision, normalizing a negative zero, and then takes the first verdict that applies:

1. The block produced no value: `absent` if it declared `absent`, otherwise `MISSING`. (A block that declares `absent` and then produces a value is an error in the script, not a verdict.)
2. The block declared `range`, `derived`, or `shape`: that verdict. The declaration is the block's own statement that it has tested the condition, so the block's code must do the testing.
3. The claim has no printed value: `shape`.
4. An erratum corrects the claim: `STALE` if the computed value agrees with the printed value (the pipeline reproduces what the erratum says is wrong), `DRIFT` if it agrees with neither the printed nor the corrected value, and `corrected` if it agrees with the corrected value.
5. The computed value agrees with the printed value at the printed precision: `match`.
6. The claim's type is `descriptive`: `hedged`.
7. Otherwise: `MISMATCH`.

Each claim prints one line: `CLAIM <claim_id> = <computed value> || [verdict] <label>`. At the end the check prints a summary counting each verdict and stops with an error on any `MISMATCH`, `STALE`, `DRIFT`, or `MISSING`. Two counts are checked separately: the claims printed must be exactly the claims with `needs_block = TRUE`, and every claim that a `quantity` erratum names must score `corrected`.

`excheckr` also has an optional band for values from simulations: a failing value within a stated distance of its target scores `MEDIUM` and passes. Whether to carry that over depends on how your rewrite handles the cases in [`rules/stochastic.md`](rules/stochastic.md).

## Traps specific to Stata and Python

These are well-known hazards of each language rather than things we hit ourselves; they belong in [`traps.md`](traps.md) once someone has met them in practice.

**Stata**

- `sort` is not stable: observations with tied keys come out in an order that depends on the sort seed. Code that relies on the order of ties (taking the first observation in a group, say) can give different answers from run to run. Use `sort, stable` or break the ties.
- A missing numeric value is larger than every number, so `if x > 5` includes missing values.
- `generate` creates a 4-byte `float` by default, so `x == 0.1` can be false for a variable assigned 0.1. Use `double` (or `set type double`) for anything compared or reported.
- `merge m:m` does not do what its name suggests; it pairs observations by order within groups. Use `joinby` for a many-to-many join, and check `_merge` after every merge.
- `version` changes behaviour well beyond the random-number generator. Set it once in the master file to the version the paper used for the archive check, and to the current version for the rewrite.

**Python**

- `pandas` guesses column types on read, which turns "0.80" into 0.8 and can turn an identifier like "007" into 7. Read anything printed as text.
- `groupby` drops groups whose key is missing unless told otherwise (`dropna=False`), and sorts groups by default.
- `statsmodels`' array interface (`sm.OLS(y, X)`) does not add an intercept, while its formula interface does.
- Library defaults change between versions more often than in R or Stata. Pin every version, and expect dispatch drift of the kind described in [`traps.md`](traps.md).

# Stage 4: Claims

The ground truth checks numbers against the pipeline. Stage 4 checks the *text*: every claim the article makes, numeric or not, gets extracted, classified, and checked a second way, by code that quotes the sentence and recomputes what it says.

We added this stage after finding that the ground truth alone missed a large share of the errors. Rerunning the code found 239 of the 599 errata in our collection; reading the articles against themselves, their appendices, and their code found another 238. A pipeline that reproduces every table can still sit under a paper whose text says something the tables don't.

## Extracting the claims

`ground_truth/published_claims.csv` lists every claim in the article and appendix:

`claim_id, location, claim_type, claim, value_paper, digits, comparison, expect, needs_block, notes`

We built it in two passes. The first extracts every numeric token from the text mechanically, and a second sweep catches numbers written as words ("two-thirds of respondents", "in all but one study"). Each candidate is then classified by hand:

| `claim_type` | What it is |
|---|---|
| `pipeline` | A number the analysis produces: an estimate, a standard error, a p-value, a sample size. |
| `descriptive` | A claim about the results that may print no number at all (see below). |
| `definitional` | A number that defines the design: the number of treatment arms, a scale's range, a survey wave's date. |
| `structural` | A number about the paper itself: "three experiments", "Table 2 shows". |
| `transcribed` | A number quoted from somewhere else, such as another study's estimate. |

`needs_block` is `TRUE` for every `pipeline` and `descriptive` claim, and for the `definitional` and `structural` claims the pipeline can actually reach. `value_paper` is stored as text, for the reasons given in [Stage 2](02_ground_truth.md).

## Claims without numbers

The claims most likely to change a reader's conclusion often print no number. A numeric sweep can't see them, so we read for them directly, looking for the verbs and phrases of comparison and inference:

- **significance**: "statistically significant", "cannot be distinguished from zero";
- **direction**: "larger among Republicans", "the effect reverses";
- **order**: "the largest effect", "smaller than the misinformation effect";
- **persistence**: "remains detectable after two weeks";
- **counts in words**: "most of the 24 experiments", "in every study".

Each becomes a `descriptive` claim, and its check tests the statement against the rewrite's output: is the interval clear of zero, is one estimate larger than the other, does the effect still appear at the later wave. The one error in our collection that changed a conclusion was a claim of this kind. An article reported that the effects of fact-checks remained detectable more than two weeks after exposure; once a coding error was corrected, the two-week estimate could not be distinguished from zero. No single number in that sentence was the problem. The claim was.

## The second check

`maintained/in_text_claims.R` has one block for each claim that needs one. Each block quotes the sentence verbatim and recomputes the claim from the rewrite's output files or its cleaned data. It never refits a model, and it never reads the ground truth, so that the two checks are independent: the ground truth compares tables with the pipeline, while this file compares the prose with the pipeline. When both agree that a number is wrong, we can be confident it is.

Each block prints one line in a fixed format:

`CLAIM <claim_id> = <computed value> || [verdict] <label>`

The verdicts that pass are:

| verdict | meaning |
|---|---|
| `match` | The computed value, at the printed precision, equals the printed value. |
| `corrected` | The printed value is wrong, and an erratum already corrects it (so the check expects the corrected value). |
| `range` | The claim states a range or a bound, and the computed value falls within it. |
| `derived` | The printed number is computed from other printed numbers, and the arithmetic holds. |
| `hedged` | The text hedges ("about", "roughly"), and the value is within half a step of its precision. |
| `shape` | A descriptive claim (direction, order, significance) holds. |
| `absent` | The claim refers to something the pipeline was never going to produce, and this is recorded. |

The verdicts that fail are `MISMATCH` (the value is wrong and no erratum covers it), `STALE` (an erratum says the value is wrong, but the pipeline now reproduces the printed one), `DRIFT` (the value has moved since the claim was last checked), and `MISSING` (a claim that needs a block has none). The file ends with a summary line that counts each verdict, and the run fails on any failing verdict.

In R, the package `excheckr` implements these verdicts (`claim_start()`, `claim()`, and `claim_summary()`). The table above is the specification, and the logic is simple enough to rewrite in Stata or Python; see [`languages.md`](../languages.md).

## Making sure every claim is checked

An early lesson: a claims file can look complete while checking nothing. In R, a script run with `source()` prints nothing unless told to, so dozens of blocks appeared to cover their claims while producing no output at all. The check that caught it was simple, and we now run it every time: run the file on its own, count the `CLAIM` lines it prints, and confirm that the count equals the number of `needs_block` rows in `published_claims.csv`, and that the printed IDs are exactly the declared ones.

We also reconcile the two instruments with each other. Every claim that appears in both the ground truth and the claims file must have the same printed value and the same classification, and where both compute a value, they must agree. Agreement has a limit worth stating: two checks can agree on a number and still both compute the wrong quantity for the sentence. The sentence-by-sentence quotes in the claims file are there so that a person can read each block and confirm that it computes what the sentence actually says.

## Text with no counterpart in the output

Some claims refer to something the rewrite doesn't produce. We sorted these into a few cases:

- **A gap in the rewrite**: the quantity should have been written out. We added it to the relevant script.
- **The deposited code contradicts the claim**, or never computed it: the claim gets the locus `archive`.
- **Nothing in the paper or the deposit identifies the quantity**: we recorded that, and did not invent a computation to check it against.
- **The deposit was never going to contain it** (a date, a design detail): it is `definitional`, with no locus.

## Done when

Every claim in the article and appendix is in `published_claims.csv`, every claim that needs a check has one, the printed count equals the declared count, the two instruments agree, and the summary line shows no failing verdicts.

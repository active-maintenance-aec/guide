# Stage 4 for agents: claims

Source of truth: [`stages/04_claims.md`](../stages/04_claims.md). Schema: [`published_claims.md`](../schemas/published_claims.md). Verdict logic: [`languages.md`](../languages.md#the-claims-check).

## Goal

Every claim in the article and appendix, numeric or not, extracted, classified, and checked by code that quotes the sentence and recomputes it.

## Do

1. Extract every numeric token from the article and appendix, then sweep again for numbers written as words.
2. Read for claims with no number: significance, direction, order, persistence, and counts in words.
3. Classify each claim (`pipeline`, `descriptive`, `definitional`, `structural`, `transcribed`), store the printed value as text with its precision, and set `comparison` and `needs_block`. Write `ground_truth/published_claims.csv`.
4. Compare the `descriptive` and `definitional` classifications within each section, and make the same sentence construction get the same type.
5. Write `maintained/in_text_claims.R` with one block per claim with `needs_block = TRUE`. Each block quotes the sentence verbatim in a comment and recomputes the claim from `maintained/output/` or the cleaned data.
6. Where a block declares `range`, `derived`, or `shape`, make the block's code test the condition. For a hedged number, make the block test the half-step bound in `rules/rounding.md`, since the check does not.
7. Run the file on its own, and check that the printed claim ids are exactly the `needs_block` ids.
8. Reconcile with the ground truth: every claim in both must have the same printed value, precision, and type, and where both compute a value, they must agree.

## Do not

- Read the ground truth from the claims script. The two checks must be independent.
- Refit models in the claims script.
- Declare a verdict a block has not tested.
- Treat an unhedged approximation as hedged.
- Invent a computation for a quantity nothing in the paper or deposit identifies.

## Stop and ask the author

- When a claim with no number appears not to hold.
- When the two instruments disagree and you cannot tell which is wrong.

## Done when

Every claim is in `published_claims.csv`, every claim that needs a check has one, the printed count equals the declared count, the two instruments agree, and the summary line shows no failing verdicts.

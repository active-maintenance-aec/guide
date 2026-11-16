# Which errors go to the journal

Active maintenance finds errors in bulk, and nearly all of them are trivial: a 2.9 that should have been a 3.0, panels of a figure in the wrong order, a misspelled name in a reference. The scientific contribution of the paper stands without the fix. A few are not trivial. This page describes how we decided which was which, and what we did with each.

## Three tiers

1. **Every error goes in the errata note**, beside the maintained code, where anyone reading the repository will find it. The note is public, itemized, and computed from the code (see [Stage 5](../stages/05_errata.md)).
2. **An error that changes the direction or implications of a finding a reader would rely on also goes to the journal**, as a corrigendum. In our experience these are rare.
3. **Retraction is for findings that can no longer be relied on at all.**

## Why not send everything

Sending every author's list of small corrections to every journal would bury the editors in notices that change nothing a reader would act on. A corrigendum is a signal that something important changed. Spent on typos and rounding slips, it stops being one. The errata note takes the volume, so that the journal notice can carry the weight.

## Where the line comes from

Existing policies say a good deal about the line between correction and retraction and little about the line between a corrigendum and no notice at all. We borrowed from both ends. The Committee on Publication Ethics reserves retraction for articles whose findings and conclusions cannot be relied upon, whatever the cause. Some medical journals ask for only a correction, even for pervasive errors, when the errors do not change the direction or implications of the results. Our second tier takes that phrase and applies it one level down: an error that changes the direction or implications of a finding warrants a notice in the journal, and one that does not can live in the errata.

## The abstract is not the test

It is tempting to send a corrigendum only for errors that touch the abstract. We did not use that test. The first error we sent to a journal concerned a persistence claim: the paper said the effect of fact-checks on factual beliefs was still detectable more than two weeks later at half its original size, and the corrected estimate was about a third of the original and could not be distinguished from zero. The claim was not the paper's central finding and was not in the abstract. The article made it three times in the main text, though, and the durability of fact-checking effects is a question readers of that literature care about. A reader could rely on it, so it went to the journal.

## When a corrigendum goes, related errors go with it

Once a corrigendum was warranted, we used it to correct the related errors in the same article too, so that the published record and the errata note do not disagree. Unrelated trivial errors stayed in the note.

## Errors an earlier correction already fixed

Some errors had been corrected already, by a corrigendum published years before. Those are recorded with `disposition = corrected_by_journal`. Reading the article against the old corrigendum also turned up sentences that went on restating a finding the corrigendum had withdrawn. Each of those sentences is an erratum of its own, and they went into the note.

## Who decides

Whether an error changes a conclusion is a judgment the pipeline cannot make. The agent drafted the errata and flagged the candidates; the author decided, and for anything sent to a journal the coauthors decided together. When an entry changes a conclusion, the errata note says so at the top.

## How the tiers appear in the data

The `disposition` column of the ground truth records what happened to each error ([Stage 2](../stages/02_ground_truth.md)):

| `disposition` | Tier |
|---|---|
| `corrected_here` | Tier 1: an entry in this repository's errata corrects it. Computed from the errata, never typed. |
| `corrected_by_journal` | Tier 2 (or an earlier correction): a published corrigendum or erratum corrects it. |
| `documented_only` | Recorded and deliberately not corrected, such as a value within simulation noise or an archive bug that never reached the page. |
| `not_corrected` | Known, and left uncorrected for a stated reason. |

Every error in the printed text must have a disposition before the build passes, since an error nobody has decided about is unfinished.

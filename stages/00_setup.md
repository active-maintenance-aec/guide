# Stage 0: Setup and style

**Purpose.** Assemble everything that can settle a question about the paper, scaffold the repository, and write down how you write code, before any code is written.

## 0.1 The published record

Collect, as the publisher's rendered PDFs:

- the article (the version of record, not the preprint or the accepted manuscript);
- the online appendix or supplementary materials;
- any published corrigendum or erratum, which is itself a published analysis to be checked against its own materials.

Every published value in later stages is read from these files. A value taken from a preprint is a value from a different document: preprints differ from the version of record in numbers, tables, and wording, and comparing against one manufactures errata.

## 0.2 The deposit

Find the replication deposit (Dataverse, OSF, ICPSR, a journal archive) and record its DOI. You will not copy the data into your repository. Stage 1 writes a script that downloads the deposit and checks every file against a manifest, so there is exactly one source of truth for the data: the archive the journal points to.

## 0.3 Your own materials outside the deposit

Look for what you kept that the deposit does not contain:

- the final production files (the `.tex` or `.docx` you sent to the publisher);
- the proofs, and your marked-up corrections to them;
- the accepted manuscript;
- older scripts and intermediate files from your working folders.

None of these is an input to the rewrite. Their job is to settle questions the deposit cannot. Was a wrong number in the text a typo, or a number left over from an earlier run? Did an error enter in typesetting, or was it already in your manuscript? What did the code look like when the paper was written? An erratum found this way records its source (`authors_archive` or `proof`; see [the errata schema](../schemas/errata_entries.md)).

Two cautions. A `.tex` in a working folder may be a draft from before copyediting, so do not treat it as the published text unless you can show it is (the strongest evidence is a compiled PDF identical to the publisher's). And materials that were never public cannot be the only basis for a correction a reader is asked to trust; use them to explain an error, and keep the correction itself grounded in the published record and the deposited data.

## 0.4 Scaffold

Create the repository with:

- a single entry point (`run_all.R`, a master `.do` file, or a Python script) that runs every stage in order and stops on the first failure;
- a project file or root marker, so that every path is relative to the repository root (`here` in R, a root global in Stata, `pathlib` in Python), with no absolute paths and no `setwd`;
- a `.gitignore` that excludes the downloaded deposit;
- a license. We use CC0 for the code, and we do not redistribute the data.

The folder layout we use:

```
run_all.R
download_original.R
original_manifest.csv
STYLE.md
maintained/            # the rewrite, one script per table or figure
maintained/output/     # everything the rewrite writes
ground_truth/          # the comparison tables and their builders
errata.qmd
README.qmd
```

## 0.5 Style investigation

A maintained rewrite is code you will read, and others will read, for years. It should look like code you would write today. The agent cannot know what that means until it has read your code.

1. **Gather recent code you wrote** and are happy with, ideally from more than one project. Recent matters: most of us write very differently than we did ten years ago, and the rewrite is a chance to bring old work up to current practice.
2. **Have the agent draft `STYLE.md`** from what it reads. It should cover, with examples from your own code:
   - how scripts are organized (one per table or figure, separate cleaning and analysis, a shared helpers file, a header comment);
   - naming (files, objects, columns);
   - data-frame idioms (the pipe, how you reshape, how you join, how you recode);
   - modeling defaults (which estimator, which standard errors, which packages);
   - figures (theme, how intervals are drawn, file formats, and the habit of writing a CSV of every plotted quantity beside the figure);
   - tables (which package, which format);
   - anything you never do.
3. **Read it, correct it, and approve it.** The draft will get some things wrong, and the corrections are the most valuable part. Commit the approved `STYLE.md`; every later stage follows it.

`STYLE.md` governs *how the code looks*. It never overrides what the rewrite must do, which is fixed for everyone:

- reproduce every number, table, and figure the paper prints, or document why not;
- run on current versions of every package;
- read the data exactly as deposited, never an edited copy;
- keep the original estimator, specification, sample, and seed, even where you would now choose differently (a choice you would make differently today is not an error; see [what counts as an erratum](../rules/erratum.md));
- never use a published number as an input.

Where a style preference and one of these rules conflict, the rule wins. A common case: if your current default is a different robust variance estimator than the one the paper used, the rewrite uses the paper's.

An example `STYLE.md`, from the papers in our collection, is in [`examples/STYLE_example.md`](../examples/STYLE_example.md). It is one person's taste, included to show the level of detail that works, not as a recommendation.

## Gate

Stage 0 is done when the repository exists with its entry point and layout, the published PDFs are in hand, the deposit DOI is recorded, and `STYLE.md` is committed with your approval.

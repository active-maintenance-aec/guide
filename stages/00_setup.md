# Stage 0: Setup and style

Before writing any code, we gathered everything that might help answer a question about the paper, set up the repository, and wrote down how we wanted the new code to look.

## The published record

We worked from the publisher's rendered PDFs: the article itself (the version of record), the online appendix, and any corrigendum already published. A published corrigendum is an analysis too, and we checked it against its own materials like everything else.

We learned to avoid preprints and accepted manuscripts as sources for published values. They often differ from the final article in small ways (a number updated in proofs, a table reordered, a sentence reworded), and comparing against the wrong version produced errata that weren't real.

## The deposit

Next we found the replication deposit (ours were on Dataverse and OSF) and recorded its DOI. We left the data where they were. Stage 1 writes a script that downloads the deposit and checks each file against a manifest, so the journal's archive stays the single source for the data.

## Materials outside the deposit

Some of the most useful evidence was not in the deposit at all. Depending on the paper, we had:

- the final production files sent to the publisher (`.tex` or `.docx`);
- the proofs, with our marked-up corrections;
- the accepted manuscript;
- older scripts and intermediate files from our working folders.

None of these fed into the rewrite. What they did was settle questions the deposit couldn't. When the text printed a wrong number, was it a typo, or a number left over from an earlier run? Did an error enter during typesetting, or was it already in our manuscript? What did the code look like when we wrote the paper? When one of these files settled a question, the erratum records it as its source (`authors_archive` or `proof`; see [the errata schema](../schemas/errata_entries.md)).

Two lessons from using them. A `.tex` file from a working folder can be a draft from before copyediting; we treated one as the published text only when its compiled PDF matched the publisher's byte for byte. And because files that were never public can't be checked by a reader, we used them to explain errors, and kept each correction itself grounded in the published article and the deposited data.

## The repository

Each repository has:

- a single entry point (`run_all.R` for us; a master `.do` file or a Python script would do the same job) that runs everything in order and stops at the first failure;
- paths relative to the repository root (we used the `here` package), so the code runs on anyone's machine;
- a `.gitignore` that keeps the downloaded deposit out of version control;
- a license. We used CC0 for the code and did not redistribute the data.

Our folder layout:

```
run_all.R
download_original.R
original_manifest.csv
STYLE.md
maintained/            # the rewrite, one script per table or figure
maintained/output/     # everything the rewrite writes
ground_truth/          # the comparison tables and the scripts that build them
errata.qmd
README.qmd
```

## Style investigation

A rewrite is code that you and others will be reading for years, so it should look like code you'd write today. My own habits have changed a lot since graduate school, and the rewrite was a chance to bring old projects up to how I work now. An agent can't know what that means without reading some of your code, so we made the question an explicit step.

1. **Gather some recent code** that you're happy with, ideally from more than one project.
2. **Have the agent draft a `STYLE.md`** from what it reads. Ours covered, with examples drawn from the code itself:
   - how scripts are organized (one per table or figure, cleaning separate from analysis, a shared helpers file, a short header comment);
   - naming of files, objects, and columns;
   - how data get reshaped, joined, and recoded;
   - modeling defaults (estimators, standard errors, packages);
   - figures (theme, how intervals are drawn, file formats, and a CSV of the plotted values saved next to each figure);
   - tables;
   - anything to avoid.
3. **Read the draft, fix it, and approve it.** The draft gets some things wrong, and fixing those turned out to be where most of the value was. The approved file is committed, and the rewrite follows it.

`STYLE.md` covers how the code *looks*. A few things about what the rewrite *does* stay the same whatever your style:

- it reproduces every number, table, and figure the paper prints, or documents why it can't;
- it runs on current versions of every package;
- it reads the data exactly as deposited;
- it keeps the paper's original estimator, specification, sample, and seed, even where you'd now choose differently (a choice you would make differently today isn't an error; see [what counts as an erratum](../rules/erratum.md));
- it never uses a published number as an input.

When a style preference and one of these conflict, the paper's choices win. The case we hit most often: my current default standard errors differ from what some of the older papers used, and the rewrites kept the originals.

There's an example `STYLE.md` from our collection in [`examples/STYLE_example.md`](../examples/STYLE_example.md). It is one person's taste, and is there to show the level of detail that worked for us.

## Done when

The repository exists with its entry point and layout, the published PDFs are in hand, the deposit DOI is recorded, and an approved `STYLE.md` is committed.

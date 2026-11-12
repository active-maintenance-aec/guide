# Stage 6: Report and publish

The last stage makes the work findable and keeps it working: a README that explains the repository to a stranger, a permanent DOI, a link from the original deposit, and a scheduled check that reruns everything.

## The README

`README.qmd` renders to the repository's `README.md` (and, for us, to a PDF report as well). We wrote it for someone who has never heard of the project and has just landed on the repository from the article. Ours cover, in order: what the repository is, with a table of verified DOIs (article, deposit, and this repository's own); how to run it; an overview of the paper; whether the deposited archive runs; the errata, with a pointer to the PDF; the ground truth and how much of each table and figure it covers; the two claim checks; the rewrite; and the software environment.

Every quantity in the README's prose is computed by an inline chunk rather than typed. Ours started out with typed numbers, and they went stale quickly: one README misstated a subset count by 150,000 after the pipeline changed underneath it.

We kept the README about the paper, and left out the history of the project: no "an earlier version of this repository found", no dates of earlier passes. A reader who never saw an earlier mistake doesn't need to hear about its correction.

## The repository

Each paper got its own public repository, licensed CC0, with `run_all.R` as the entry point. The deposit itself is never copied in; `download_original.R` fetches it. Before publishing, we ran the whole pipeline once more and confirmed that it left no stray or changed files, and we checked file paths against a case-sensitive file system, since one repository worked on a Mac and failed on Linux over the capitalization of a single file name.

## A permanent DOI

GitHub isn't an archive, and neither is a personal website. We archived each repository at Zenodo, which mints a *concept DOI* that always resolves to the latest version, plus a version DOI for each release. Zenodo makes a new version only when you publish a GitHub release, so routine maintenance doesn't mint new DOIs; we cut a release when the errata or the maintained code changed in a way worth archiving.

A `.zenodo.json` in the repository sets the record's title, creators, license, and related identifiers: the article (`isSupplementTo`), the original deposit (`isDerivedFrom`), and the GitHub repository itself. One thing caught us: once `.zenodo.json` lists related identifiers, Zenodo stops adding the link to the GitHub repository on its own, so it has to be listed explicitly.

The concept DOI then goes in the README and in the errata note, so that the PDF, wherever it travels, points back to the maintained code.

## Linking the deposit back

A reader who starts from the article follows its DOI to the original deposit. For them to find the maintained version, the deposit has to point to it. On Dataverse we added a line to each deposit's *Related Material* field, giving the Zenodo DOI and the repository URL. A metadata-only change publishes a minor version (1.1, say) with the files untouched. On OSF, which has no such field, the line went into the project description.

Some details from doing this for all of our deposits:

- Deposits in your own Dataverse collection can be published directly. Deposits in a journal's collection usually go to the journal's curators for review, which on Harvard Dataverse means agreeing to a short attestation and waiting.
- Some older deposits lacked fields that Dataverse now requires (a subject, a contact email), and couldn't be saved until those were filled in.
- Deposits made by a coauthor or by the journal can only be edited by them.
- Harvard Dataverse runs an automated metadata check on publication, and it held one of ours for staff review.

## The scheduled check

Active maintenance only works if someone notices when the code stops working. Each repository carries a short GitHub Actions workflow that calls a shared one in [`active-maintenance-aec/maintenance`](https://github.com/active-maintenance-aec/maintenance), which reruns `run_all.R` on current R and current packages, every eight weeks, with the repositories staggered so that a handful run each week. The check fails if the pipeline breaks or if any committed file it judges changes.

A few choices made the check useful rather than noisy:

- **Numbers are judged; figure files are not.** A PDF or PNG drawn on Linux is never byte-identical to one drawn on a Mac, so figure files are counted but don't fail the check. Every figure's plotted values are saved as a CSV, and those are judged.
- **Floating-point noise is forgiven.** Linux and macOS differ in the last bits of some floating-point results, so a CSV whose only differences fall within a relative tolerance of one in a million is counted as noise.
- **The schedule stays alive.** GitHub disables a scheduled workflow after 60 days without activity in the repository, which a maintained repository can easily go. The workflow re-enables itself every week.
- **Very slow pipelines get a shorter run.** GitHub limits a job to six hours. One of our pipelines takes far longer than that, so on GitHub it skips its slowest deposited scripts and judges everything else, and the full run happens locally.

When the check fails, the cause is usually a package update. The rewrite is meant to be current code, so the response is to update the rewrite, not to pin the old package version; if a published number moves, the ground truth records it as an `environment` difference and the errata note updates when it next renders.

## Done when

The README renders with every number computed, the repository is public, its Zenodo DOI resolves and appears in the README and the errata, the original deposit links to it, and the scheduled check has passed at least once.

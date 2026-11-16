# Stage 6 for agents: report and publish

Source of truth: [`stages/06_publish.md`](../stages/06_publish.md).

## Goal

A README a stranger can follow, a public repository with a permanent DOI, a link from the original deposit, and a scheduled check.

## Do

1. Write `README.qmd` for someone arriving from the article: what the repository is, a table of verified DOIs (article, deposit, repository), how to run it, an overview of the paper, whether the archive runs, the errata, the ground truth and each float's coverage, the two claim checks, the rewrite, and the software environment.
2. Compute every quantity in the README's prose with inline code.
3. Run the whole pipeline once more and confirm it leaves no stray or changed files. Check file names against a case-sensitive file system.
4. Write `.zenodo.json` with the title, creators, license, and related identifiers: the article (`isSupplementTo`), the deposit (`isDerivedFrom`), and the repository URL, listed explicitly.
5. Prepare the line that links the deposit to the maintained version (the Zenodo concept DOI and the repository URL), for Dataverse's Related Material field or the OSF project description.
6. Add the scheduled check workflow, and confirm it passes once.

## Do not

- Write the history of the project into the README.
- Copy the deposit into the repository.
- Pin old package versions to make a failing check pass; update the rewrite instead.

## Stop and ask the author

- Before making the repository public, creating a GitHub release, or publishing at Zenodo. Each is visible to others and hard to undo.
- Before editing any deposit's metadata. Deposits in a journal's collection, or made by a coauthor, need their curators or owners.

## Done when

The README renders with every number computed, the repository is public, its Zenodo DOI resolves and appears in the README and the errata, the original deposit links to it, and the scheduled check has passed at least once.

# `original_manifest.csv`

One row per file in the replication deposit. The manifest is the repository's record of what the deposit held, and `download_original.R` checks every download against it ([Stage 1](../stages/01_archive_check.md)). We built each manifest from the archive's API rather than by hand.

The columns differ by archive, because the archives publish different things about each file.

## Dataverse

`file, directory_label, dataverse_file_id, file_persistent_id, bytes, md5_served, md5_published, unf, served_as`

| Column | Type | Meaning |
|---|---|---|
| `file` | text | The file's original name, as the authors uploaded it. |
| `directory_label` | text | The folder the file sits in within the deposit; empty for a file at the top level. |
| `dataverse_file_id` | integer | Dataverse's numeric file id, used to download it. |
| `file_persistent_id` | text | The file's own DOI, where the installation assigns one; empty otherwise. |
| `bytes` | integer | Size of the original file in bytes. |
| `md5_served` | text | MD5 of the bytes the download actually returns. |
| `md5_published` | text | MD5 that Dataverse publishes in the file's metadata. |
| `unf` | text | Dataverse's Universal Numerical Fingerprint, for tabular files it has ingested; empty otherwise. |
| `served_as` | text | The file name the download returns. |

`md5_served` and `md5_published` usually agree. They part when Dataverse has ingested a tabular upload (a `.dta` or `.csv`, say) and serves its own `.tab` version by default: the published checksum describes the original upload and the served bytes are the conversion. We downloaded with `?format=original` so that the original is what arrives, and recorded both checksums so that a disagreement is visible rather than silent.

## OSF

`file, directory_label, osf_file_id, bytes, md5_served, md5_published, sha256_published`

| Column | Type | Meaning |
|---|---|---|
| `file` | text | The file's name. |
| `directory_label` | text | The folder within the OSF storage; empty at the top level. |
| `osf_file_id` | text | OSF's id for the file. |
| `bytes` | integer | Size in bytes. |
| `md5_served` | text | MD5 of the bytes the download returns. |
| `md5_published` | text | MD5 that OSF publishes for the file. |
| `sha256_published` | text | SHA-256 that OSF publishes for the file. |

OSF stores one set of bytes and publishes two checksums of it, with no converted version, so the served-versus-published problem above cannot arise.

## Other archives

The rule that carries over: record every checksum the archive publishes, record the byte size, and have the download stop on any disagreement with an independent claim about the bytes.

## Checks

The download stops if a file's size or served checksum differs from the manifest, or if `original/` contains a file the manifest does not list (hidden files included). A disagreement with the published checksum is printed without stopping. Zip and RAR files are unpacked into their own folders and checked against a second manifest of their contents.

# Agent instructions

These files restate the guide as instructions a coding agent can follow. They add nothing to it. If one of them disagrees with the stage, rule, or schema it points to, the document written for people is correct, and the agent file should be fixed.

- [`session_start.md`](session_start.md): a prompt to begin each working session.
- [`00_setup.md`](00_setup.md) to [`06_publish.md`](06_publish.md): one file per stage.

They are written for no particular model or tool. To use them, point the agent at `session_start.md` and at the file for the stage you are working on, and keep the guide's `rules/`, `schemas/`, and `traps.md` where the agent can read them.

Two points apply to every stage. The author decides what counts as an error, whether a correction changes a conclusion, and what goes to a journal; the agent proposes. Every number the agent reports about the paper (a count, a coverage fraction, a verdict) must come from code it ran, not from memory of an earlier run.

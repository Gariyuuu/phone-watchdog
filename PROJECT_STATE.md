# PROJECT_STATE.md — Exact Handoff Snapshot

**This file describes the state of the repository at one specific moment.**
It will go stale the instant more work happens — update it after every
meaningful session (see `CLAUDE.md` → Permanent rules).

## 2026-08-17 update [Verified] — current task `T-002` — read this before the rest of the file

A documentation-sweep session (no feature work) found two things:

1. **The checked-out branch is `chore/venv-fix`, not `main`** — but it
   has **zero commits beyond what `main` already has**
   (`git log --oneline main..chore/venv-fix` is empty). This is
   consistent with someone having fixed the local `venv/` (see below)
   under that branch name, but since `venv/` is gitignored, that fix
   left no git trace — there's nothing to diverge. No application code
   or docs changed on this branch that isn't already on `main`.
2. **`TASK-001` ("rebuild the broken local `venv/`") is done.** Verified
   directly: `venv/bin/python3` now resolves to a real interpreter
   (`/opt/homebrew/Cellar/python@3.11/.../bin/python3.11`, dated Aug 13
   on disk) rather than the symlink-into-another-project's-venv chain
   the 2026-08-06 audit found. `./venv/bin/python3 -c "import cv2,
   ultralytics"` succeeds (`cv2` 5.0.0.93, `ultralytics` 8.4.118) —
   confirmed by running it directly this sweep. This was **not**
   accompanied by a live webcam smoke test (`TASK-002`), which remains
   the new current task — it requires a human physically present.

Nothing else changed: still 2 real application/doc commits total on
`main` (`d2c04e6`, `6631562`) plus the 2026-08-07 doc-correction commit
(`eb595f5`, current `HEAD`), working tree clean. The rest of this file
(written 2026-08-06/07) is preserved below as history — its "`venv/` is
broken" framing is now outdated per the above.

## Audit timestamp

- **Audit performed:** 2026-08-06 (documentation/handoff audit — no
  application code was changed during this audit; only documentation
  files were added, all 17 net-new). No product behavior was modified.

## Git state

- **Branch:** `main` (the only branch — confirmed via `git branch -a`;
  no other local or remote branches, no tags)
- **Tracking:** `origin/main`
  (`https://github.com/Gariyuuu/phone-watchdog.git`), up to date with
  the remote as of this audit (`git status` reports "up to date")
- **Latest commit:** `6631562` — "docs: add full handoff documentation
  system" (Gary Wang, 2026-08-06T20:20:25-07:00), on top of `d2c04e6` —
  "Initial commit: phone watchdog monitor script" (Gary Wang,
  2026-08-03T14:07:49-07:00). Two commits total in the repository's
  history, both pushed to `origin/main` (confirmed via `git rev-parse
  HEAD` == `git rev-parse origin/main` during the 2026-08-07 verification
  pass below).
- **Working tree:** **Clean.** `git status --porcelain` returns nothing.
- **Correction (2026-08-07 verification pass):** this file previously
  stated the 17 documentation files added by the 2026-08-06 audit were
  "untracked until committed" / "none of these have been committed."
  That was stale — they *were* committed later that same session
  (`6631562`, timestamped 20:20:25, after this file's own audit-timestamp
  narrative was written) and the commit is pushed to `origin/main`. Fixed
  here; see `SESSION_LOG.md` Session 2 for the correction record.
- **Tracked repo contents:** `.gitignore`, `monitor.py`,
  `requirements.txt` (from `d2c04e6`) plus the 17 documentation files and
  now `README.md` (added 2026-08-07, filling the one gap the 17-file set
  didn't originally include). `venv/` exists on disk but is gitignored
  and was never tracked.

## Active objective

There was no user-directed feature objective in progress before this
audit — the repository had zero documentation and this session's task
was explicitly to build the full 17-file handoff documentation system
from a first-principles audit of the actual code, matching the
structural depth of `~/Projects/chamber-seven` and
`~/Projects/buildstrike-arena` (but with facts drawn only from this
repo).

## Last completed task (before this audit)

The single initial commit (`d2c04e6`) that created `monitor.py`,
`requirements.txt`, and `.gitignore`. No further application-code
history exists.

## Current task (this audit)

**Documentation/handoff audit — in progress, this session.** Build all
17 standard memory files from scratch, based on a full read of
`monitor.py`, `requirements.txt`, `.gitignore`, and the git history, plus
direct verification of the local `venv/`'s actual health.

- **What's completed:** Full read of `monitor.py` (all 165 lines), full
  read of `requirements.txt` and `.gitignore`, full git history review
  (one commit, clean tree, single branch), a repo-wide search for
  TODO/FIXME/HACK/placeholder/hardcoded-secret patterns (none found), a
  syntax-only verification (`python -m py_compile monitor.py` — passed),
  and a direct inspection of `venv/`'s actual interpreter and installed
  packages (found broken — see below). All 17 documentation files
  created.
- **What remains:** None for this pass. Future sessions should keep
  these files updated per `CLAUDE.md`'s permanent rules.

## What works (verified this audit)

- `monitor.py` is syntactically valid Python: `python -m py_compile
  monitor.py` (run via the broken venv's borrowed interpreter, Python
  3.9.6) completed with no errors.
- `tkinter` (the GUI toolkit `monitor.py` depends on) imports
  successfully through that same borrowed interpreter.
- The code, read line-by-line, is internally consistent: the
  producer/consumer queue pattern between `detector_loop()` and the
  Tkinter `poll()` function is correctly structured for Tkinter's
  single-threaded GUI requirement (all GUI mutation happens on the main
  thread via `root.after`, never from the detector thread directly).
- `git log`/`git status`/`git branch -a` all behave normally; the repo
  itself is not corrupted.

## What fails / is unverified (verified or flagged this audit)

- **`./venv/bin/python monitor.py` (the script's own documented run
  command) will fail immediately** with `ModuleNotFoundError: No module
  named 'cv2'`. Directly verified: `venv/bin/python3 -m pip list` shows
  only `pip` and `setuptools` installed — neither `opencv-python` nor
  `ultralytics` is present. Root cause: `venv/bin/python3` is a symlink
  to `/Users/gariyuu/Projects/hyperliquid-bot/.venv/bin/python3`, which
  is itself a symlink to
  `/Users/gariyuu/Projects/sports-betting-project/.venv/bin/python3` —
  this venv does not actually belong to (or contain the dependencies of)
  this project. See `CLAUDE.md` → Known issues #1 for the full
  explanation and the fix (`rm -rf venv && python3 -m venv venv &&
  ./venv/bin/pip install -r requirements.txt`).
- **Whether the actual phone-detection behavior works correctly is
  Unable to verify.** Per this task's explicit safety instructions, the
  webcam/detection/GUI loop was **not launched** during this audit (it
  would open a real camera and, once dependencies are installed, begin
  actively analyzing real video). The code was instead fully read and
  reasoned about manually. Whoever next has a working `venv/` and is
  physically present at the machine should do a real, human-supervised
  smoke test (see `TESTING.md`) before trusting this in daily use.
- **First real run will additionally require internet access** the
  first time (`ultralytics` auto-downloads `yolov8n.pt`, ~6MB, on first
  `YOLO("yolov8n.pt")` call — no such file is committed to this repo,
  confirmed via `find . -iname "*.pt"`).
- **Cross-platform behavior:** the alarm path (`afplay` +
  `/System/Library/Sounds/Sosumi.aiff`) is macOS-only; unverified (and
  expected to fail) on any other OS.

## Blockers

1. **`venv/` must be rebuilt before this script can run at all.** This
   is the single highest-priority blocker — see above and
   `CLAUDE.md` → Known issues #1.
2. No other blockers identified — the code itself does not appear to
   depend on anything else unresolved.

## Assumptions currently in effect (not independently re-verified beyond
what's stated above)

- It is assumed the author previously ran this successfully in some
  *other*, correctly-configured environment before committing it (the
  code reads as a deliberate, complete first draft, not experimental/
  broken code) — but this is **Inferred**, not confirmed; no evidence in
  the repo (no `CHANGELOG`, no commit beyond the initial one, no test
  output) proves it was ever actually run successfully anywhere.
- It is assumed `ultralytics`/`opencv-python`, once actually installed,
  will work without further code changes on this machine's default
  webcam (`cv2.VideoCapture(0)`) and default audio output — not verified
  this audit (would require running the full script).
- It is assumed no relationship to `phone-watchdog-web` exists (see
  `CLAUDE.md`), based on a full read of `monitor.py` finding zero
  network-related imports or code. This is a **Verified negative** (the
  absence of a relationship, confirmed by exhaustive code read), not an
  assumption about a positive integration that wasn't checked.

## Next three recommended actions

1. **Rebuild `venv/` from scratch** (`rm -rf venv && python3 -m venv venv
   && ./venv/bin/pip install -r requirements.txt`) and confirm `cv2` and
   `ultralytics` import successfully in the new environment.
2. **Do one human-supervised smoke test**: run `./venv/bin/python
   monitor.py`, hold a phone in front of the webcam for a few seconds,
   confirm the overlay + alarm fire, put the phone down, confirm it
   auto-clears after ~3 seconds, and confirm Ctrl+C cleanly stops the
   process. See `TESTING.md` for the full checklist.
3. **Decide and document intent** on the ESC-dismiss behavior (see
   `CLAUDE.md` → Known issues #3 — right now ESC only hides the overlay
   momentarily if the phone is still in frame, which may or may not be
   the intended UX) — either confirm it's intentional or file it as a
   real fix in `TASKS.md`.

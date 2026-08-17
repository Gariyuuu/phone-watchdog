# TASKS.md — Active Execution Queue

Update this file after every meaningful session. Move completed tasks to
"Recently completed" rather than deleting them.

## Current task: `T-002` (a.k.a. `TASK-002`, this repo's pre-existing ID)

**`TASK-001` is done** — re-verified 2026-08-17 (documentation sweep):
`venv/bin/python3` now resolves to a real interpreter
(`/opt/homebrew/Cellar/python@3.11/.../bin/python3.11`, dated Aug 13 on
disk), not a symlink into another project's venv, and
`./venv/bin/python3 -c "import cv2, ultralytics"` succeeds (`cv2`
5.0.0.93, `ultralytics` 8.4.118). **Since `venv/` is gitignored, this
fix left no git trace** — no commit exists for it (the checked-out
branch `chore/venv-fix` has zero commits beyond what `main` already has,
consistent with a venv-only fix that git never saw). This is inferred
from disk state, not a specific session's account — nobody's
`SESSION_LOG.md` entry claims credit for it.

The new current task is **`T-002`/`TASK-002`** — the real,
human-supervised smoke test — now unblocked (its only dependency,
`TASK-001`, is done) but still requires a human physically present with
a webcam and a phone; not something to run unattended. See its full
description below.

## Next up (superseded — see "Current task" above)

### TASK-001 — Rebuild the broken local `venv/` — **DONE, verified 2026-08-17**
- **Priority:** High (blocking everything else) — no longer blocking,
  see above.
- **Exact objective:** Get a working local Python environment so
  `monitor.py` can actually be run and tested.
- **Why:** Verified 2026-08-06 audit — `venv/bin/python3` was a symlink
  into `~/Projects/hyperliquid-bot/.venv`, itself symlinked into
  `~/Projects/sports-betting-project/.venv`. Neither `opencv-python` nor
  `ultralytics` was installed in the resolved environment.
- **Resolution verified 2026-08-17:** `venv/bin/python3` is now a real
  `python3.11` interpreter with both packages installed and importable.
  Not re-run against a live webcam as part of this fix confirmation
  (that's `TASK-002`) — only the import itself was confirmed.
- **Files:** `venv/` (not tracked by git — safe to delete/rebuild
  freely).
- **Acceptance criteria:** `cv2` and `ultralytics` both importable from
  `venv/bin/python3`; `venv/bin/python3` resolves to a real interpreter
  belonging to this project, not a symlink into another project's venv.
  **Both met.**

### TASK-002 (`T-002`) — Real, human-supervised smoke test — **current task, unblocked**
- **Priority:** High — now the top of the queue (`TASK-001` is done).
- **Exact objective:** Confirm the detection → alarm → overlay → clear
  pipeline actually works against a real webcam and a real phone — this
  has never been confirmed in this environment (see `TESTING.md`).
- **Depends on:** TASK-001 — **done, see above.**
- **Steps:** See `TESTING.md` → Manual smoke-test checklist in full.
- **Blockers:** Requires a human physically present at the machine with
  a webcam and a phone — not something an AI agent can do unattended per
  this project's own safety constraints (opens a real camera). This is
  the only remaining blocker as of 2026-08-17.
- **Acceptance criteria:** Overlay + alarm fire within ~2-3s of holding a
  phone in frame; overlay + alarm clear within ~3-4s of putting it away;
  Ctrl+C cleanly stops the process with no hung threads.

## Blocked

`T-002`/`TASK-002` is blocked only by needing a human physically present
(see above) — its former dependency, `TASK-001`, is done as of
2026-08-17. Not blocked by any missing information.

## Bugs

- **Possible bug, not confirmed as unwanted behavior — needs a decision:**
  ESC-dismissing the overlay does not stop detection; if the phone is
  still in frame, the very next qualifying detection frame re-queues
  `phone_detected` and the overlay reappears almost immediately (within
  roughly one detection cycle, ~3 captured frames). See `CLAUDE.md`
  Known issues #3, `ARCHITECTURE.md`. **Action needed:** confirm with the
  project owner whether this is intended ("keep nagging until the phone
  is actually put down") or a bug (expected: ESC should give a grace
  period). Not fixed this audit — flagging only, per the audit's
  documentation-only scope.
- **Unhandled-exception risk in the detector thread:** no `try`/`except`
  exists anywhere in `monitor.py`. An uncaught exception inside
  `detector_loop()` (e.g. a transient `cv2`/`ultralytics` error) would
  silently kill background detection for the rest of the process's life,
  with no error surfaced to the user. Not confirmed to have ever
  happened (no logs exist) — flagged as a latent risk, not an observed
  bug.

## Technical debt

- `requirements.txt` has no version pins (`opencv-python`, `ultralytics`)
  — a future `pip install` could pull a materially different version
  than whatever was originally used, with no lockfile to fall back to.
- No logging anywhere beyond one `print()` on webcam-open failure — makes
  it hard to confirm the watchdog is alive/working without visually
  testing with a real phone every time.
- `venv/` being broken (see TASK-001) is itself a form of debt — nothing
  currently prevents this from recurring if the venv is ever recreated
  carelessly (e.g. with a `python3` on `PATH` that itself resolves into
  another project's environment).
- No `.gitignore` entry exists for a potential future `yolov8n.pt`
  weights file if `ultralytics` is ever configured to cache it into the
  project directory instead of its default cache location.

## Testing needed

- No automated tests exist at all — see `TESTING.md`. The single
  highest-value thing to verify (manually, since there's no test
  framework) is the full detect → trigger → overlay → alarm → clear
  cycle against a real webcam, which has never been done in this
  environment (see TASK-002).

## Documentation needed

- None outstanding beyond what this audit just produced — keep it
  updated going forward per `CLAUDE.md`'s permanent rules.

## Recently completed

- **2026-08-07 — Verification pass + README.md added (17/17 docs
  complete).** Re-verified all 16 existing docs against the live repo
  and git state (venv still broken, exactly as documented; `monitor.py`
  still compiles; no secrets found). Wrote `README.md`, the one missing
  file. Fixed a staleness bug: `PROJECT_STATE.md`, `TASKS.md` (this
  entry), and `CHANGELOG.md` previously said the 2026-08-06 doc batch
  was "not committed" — it actually was, later that same session
  (`6631562`, pushed to `origin/main`). Corrected.
- **2026-08-06 — Full documentation/handoff audit.** Built all 17
  standard memory files (`CLAUDE.md` through `HANDOFF.md`) from a
  first-principles read of `monitor.py`, `requirements.txt`,
  `.gitignore`, and the git history. Discovered and documented the
  broken `venv/` (previously unknown/undocumented). No application code
  was changed. Committed and pushed as `6631562` later the same session
  (this was not yet true at the moment this file was originally
  written — see the 2026-08-07 correction entry above).
- **2026-08-03 — Initial commit (`d2c04e6`).** `monitor.py`,
  `requirements.txt`, `.gitignore` — the entire application as it exists
  today.

## Deferred

None recorded — no explicit deferrals were found in code comments or
commit history (there is only one commit).

## Rejected ideas

None recorded — no explicit rejections were found in code comments or
commit history.

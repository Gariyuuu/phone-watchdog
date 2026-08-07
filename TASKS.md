# TASKS.md — Active Execution Queue

Update this file after every meaningful session. Move completed tasks to
"Recently completed" rather than deleting them.

## Current task

**None in progress.** This session's task was the documentation audit
itself (building this 17-file memory system from scratch) — see
`PROJECT_STATE.md` for its exact status (complete as of this writing).
No application-code task is currently active. The highest-priority next
pick, if the user wants to continue, is `TASK-001` below.

## Next up

### TASK-001 — Rebuild the broken local `venv/`
- **Priority:** High (blocking everything else)
- **Exact objective:** Get a working local Python environment so
  `monitor.py` can actually be run and tested.
- **Why:** Verified this audit — `venv/bin/python3` is a symlink into
  `~/Projects/hyperliquid-bot/.venv`, itself symlinked into
  `~/Projects/sports-betting-project/.venv`. Neither `opencv-python` nor
  `ultralytics` is installed in the resolved environment (`pip list`
  shows only `pip`/`setuptools`). Running `./venv/bin/python monitor.py`
  as documented fails immediately with `ModuleNotFoundError: No module
  named 'cv2'`.
- **Steps:** `rm -rf venv && python3 -m venv venv && ./venv/bin/pip
  install -r requirements.txt`, then confirm `./venv/bin/python -c
  "import cv2, ultralytics"` succeeds.
- **Files:** `venv/` (not tracked by git — safe to delete/rebuild
  freely).
- **Blockers:** None.
- **Acceptance criteria:** `cv2` and `ultralytics` both importable from
  `venv/bin/python3`; `venv/bin/python3` resolves to a real interpreter
  belonging to this project, not a symlink into another project's venv.

### TASK-002 — Real, human-supervised smoke test
- **Priority:** High (depends on TASK-001)
- **Exact objective:** Confirm the detection → alarm → overlay → clear
  pipeline actually works against a real webcam and a real phone — this
  has never been confirmed in this environment (see `TESTING.md`).
- **Depends on:** TASK-001.
- **Steps:** See `TESTING.md` → Manual smoke-test checklist in full.
- **Blockers:** TASK-001 must be done first. Also requires a human
  physically present at the machine with a webcam and a phone — not
  something an AI agent can do unattended per this project's own safety
  constraints (opens a real camera).
- **Acceptance criteria:** Overlay + alarm fire within ~2-3s of holding a
  phone in frame; overlay + alarm clear within ~3-4s of putting it away;
  Ctrl+C cleanly stops the process with no hung threads.

## Blocked

Nothing is blocked by an external dependency — TASK-002 is blocked only
by TASK-001 and by needing a human present (see above), not by any
missing information.

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

- **2026-08-06 — Full documentation/handoff audit.** Built all 17
  standard memory files (`CLAUDE.md` through `HANDOFF.md`) from a
  first-principles read of `monitor.py`, `requirements.txt`,
  `.gitignore`, and the git history. Discovered and documented the
  broken `venv/` (previously unknown/undocumented). No application code
  was changed; nothing was committed.
- **2026-08-03 — Initial commit (`d2c04e6`).** `monitor.py`,
  `requirements.txt`, `.gitignore` — the entire application as it exists
  today.

## Deferred

None recorded — no explicit deferrals were found in code comments or
commit history (there is only one commit).

## Rejected ideas

None recorded — no explicit rejections were found in code comments or
commit history.

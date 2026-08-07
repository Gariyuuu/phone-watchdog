# CHANGELOG.md

This changelog is reconstructed from `git log` (two commits total) plus
each session's documentation work. No dates are invented — only what
`git log` and each session's own timestamp support.

## Unreleased

### 2026-08-07 — Verification pass + README added
- Added `README.md` — the one file missing from the 17-file standard
  documentation set (16/17 → 17/17).
- Re-verified `PROJECT_STATE.md`/`TASKS.md`/`FEATURES.md`/`SECURITY.md`/
  `DATABASE.md` against the live repo and git state; confirmed `venv/`
  is still broken exactly as previously documented (no change), and
  `monitor.py` still compiles cleanly.
- **Fixed staleness:** `PROJECT_STATE.md`, `TASKS.md`, and this file
  previously stated the 2026-08-06 documentation batch was "not
  committed." That was true when originally written but went stale
  later the same session, when commit `6631562` actually committed and
  pushed all 17 files. Corrected across all three files; see
  `SESSION_LOG.md` Session 2.
- No secrets found in tracked files or documentation (placeholders only,
  where present).

### 2026-08-06T20:20:25-07:00 — `6631562` "docs: add full handoff documentation system"
- Committed and pushed the full 17-file handoff documentation system
  (`CLAUDE.md`, `PROJECT_STATE.md`, `ARCHITECTURE.md`, `FILE_MAP.md`,
  `FEATURES.md`, `TASKS.md`, `ROADMAP.md`, `DECISIONS.md`, `DATABASE.md`,
  `API_REFERENCE.md`, `UI_SYSTEM.md`, `SECURITY.md`, `TESTING.md`,
  `DEPLOYMENT.md`, `CHANGELOG.md` (this file), `SESSION_LOG.md`,
  `HANDOFF.md`), built from a first-principles audit of the actual
  repository earlier that day — no prior documentation existed before
  this commit.
- **Discovered (not fixed by this commit):** the committed `venv/` is
  broken — its `python3` is a symlink chain into two unrelated sibling
  projects' virtualenvs, and neither `opencv-python` nor `ultralytics`
  is actually installed. This means `./venv/bin/python monitor.py`,
  exactly as the script's own docstring instructs, currently fails
  immediately. See `CLAUDE.md` → Known issues #1 and `TASKS.md` →
  TASK-001. Still unfixed as of the 2026-08-07 verification pass above.
- No application (`monitor.py`) code was changed by this commit —
  documentation only.

## 2026-08-03 — Initial commit (`d2c04e6`)

- "Initial commit: phone watchdog monitor script"
- Added `monitor.py` (webcam-based phone-use watchdog: YOLOv8n detection
  + Tkinter fullscreen overlay + `afplay` alarm), `requirements.txt`
  (`opencv-python`, `ultralytics`), and `.gitignore` (`venv/`,
  `__pycache__/`, `*.pyc`, `.DS_Store`).
- This is the entire commit history of the repository as of this audit
  — no other commits exist.

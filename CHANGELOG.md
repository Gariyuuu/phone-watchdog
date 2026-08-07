# CHANGELOG.md

This changelog is reconstructed from `git log` (one commit total) plus
this session's documentation work. No dates are invented — only what
`git log` and this session's own timestamp support.

## Unreleased

### 2026-08-06 — Documentation/handoff audit
- Added the full 17-file handoff documentation system (`CLAUDE.md`,
  `PROJECT_STATE.md`, `ARCHITECTURE.md`, `FILE_MAP.md`, `FEATURES.md`,
  `TASKS.md`, `ROADMAP.md`, `DECISIONS.md`, `DATABASE.md`,
  `API_REFERENCE.md`, `UI_SYSTEM.md`, `SECURITY.md`, `TESTING.md`,
  `DEPLOYMENT.md`, `CHANGELOG.md` (this file), `SESSION_LOG.md`,
  `HANDOFF.md`), built from a first-principles audit of the actual
  repository — no prior documentation existed.
- **Discovered (not fixed):** the committed `venv/` is broken — its
  `python3` is a symlink chain into two unrelated sibling projects'
  virtualenvs, and neither `opencv-python` nor `ultralytics` is actually
  installed. This means `./venv/bin/python monitor.py`, exactly as the
  script's own docstring instructs, currently fails immediately. See
  `CLAUDE.md` → Known issues #1 and `TASKS.md` → TASK-001.
- No application code was changed. Nothing was committed, pushed,
  deployed, reset, or discarded — this was a read-and-document-only
  pass, per explicit instructions.

## 2026-08-03 — Initial commit (`d2c04e6`)

- "Initial commit: phone watchdog monitor script"
- Added `monitor.py` (webcam-based phone-use watchdog: YOLOv8n detection
  + Tkinter fullscreen overlay + `afplay` alarm), `requirements.txt`
  (`opencv-python`, `ultralytics`), and `.gitignore` (`venv/`,
  `__pycache__/`, `*.pyc`, `.DS_Store`).
- This is the entire commit history of the repository as of this audit
  — no other commits exist.

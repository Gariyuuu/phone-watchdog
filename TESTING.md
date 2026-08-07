# TESTING.md

## Current test strategy: none exists.

Verified via a repo-wide search: no `tests/` directory, no `test_*.py` /
`*_test.py` files, no `pytest`/`unittest` reference anywhere, and no
testing library listed in `requirements.txt`. There is no CI
configuration (no `.github/workflows/`) either. The only verification
performed anywhere in this repo's history is whatever the original
author did manually and unrecorded before the single initial commit.

## What was verified during this audit (2026-08-06)

- **Syntax check only:** `python -m py_compile monitor.py` (run via the
  local, borrowed-but-functional-enough-for-this-one-check interpreter)
  completed with no errors. This confirms the file parses as valid
  Python 3 — it says nothing about runtime correctness.
- **`tkinter` importability:** confirmed importable through the same
  interpreter.
- **`cv2` / `ultralytics` importability:** confirmed **NOT** importable
  through the current `venv/` — `ModuleNotFoundError` for both (see
  `PROJECT_STATE.md`). This means even a basic "does the app's own
  imports resolve" check currently fails until `venv/` is rebuilt.
- **The full webcam/detection/GUI/alarm pipeline was deliberately NOT
  run** during this audit, per the task's explicit safety instructions —
  it would open a real webcam and begin actively analyzing real video
  before the dependency situation was even confirmed working. This is
  documented as **Unable to verify** rather than assumed working.

## Manual smoke-test checklist (for whoever next has a working `venv/`
and is physically present at the machine)

Run this only when you can personally sit in front of the webcam — it
is not something to script/automate unattended, and not something an AI
agent should run on your behalf without you being present.

1. **Setup:** `rm -rf venv && python3 -m venv venv && ./venv/bin/pip
   install -r requirements.txt`. Confirm no install errors.
2. **Import check:** `./venv/bin/python -c "import cv2; import
   ultralytics; print('OK')"` — should print `OK` with no traceback.
3. **Launch:** `./venv/bin/python monitor.py`. Expected: no console
   output (the happy path prints nothing), no window appears yet.
   - If you instead see `Error: Could not open webcam.` printed and the
     process exits: check camera permissions for the terminal/Python
     app in System Settings → Privacy & Security → Camera, and confirm
     no other app is holding the camera exclusively.
   - If this is the very first run, expect a pause while `yolov8n.pt` is
     downloaded (requires internet) — not surfaced as visible progress
     anywhere in the script's own output.
4. **Baseline (no phone):** with no phone in view, confirm nothing
   happens — no overlay, no sound — for at least 10-15 seconds.
5. **Trigger:** hold a phone clearly in view of the webcam. Expect the
   fullscreen red "PUT YOUR PHONE DOWN" overlay to appear, and the alarm
   sound to start, within roughly 2-3 seconds of the phone becoming
   continuously visible (`TRIGGER_SECONDS = 2.0`, plus some detection
   latency from the every-3rd-frame sampling).
6. **Alarm repeat:** confirm the alarm sound repeats roughly every 2.5
   seconds (`ALARM_INTERVAL_SECONDS`) while the overlay stays up.
7. **Clear:** put the phone out of view. Expect the overlay to
   disappear and the alarm to stop within roughly 3-4 seconds
   (`CLEAR_SECONDS = 3.0`, plus detection latency).
8. **ESC dismiss:** trigger the overlay again, then press ESC while
   still holding the phone in view. Expected (per current code, see
   `CLAUDE.md` Known issues #3): the overlay disappears and the alarm
   stops **momentarily**, then likely reappears within about a second if
   the phone is still visible. Confirm whether this matches your
   expectation — if not, this is a real fix candidate, not just
   documentation (see `TASKS.md` → Bugs).
9. **Clean shutdown:** press Ctrl+C in the terminal. Confirm the process
   exits and no orphaned Python process is left running (`ps aux | grep
   monitor.py`) and, if the overlay/alarm were active, that the alarm
   sound actually stops (doesn't keep looping after the process is
   killed).
10. **Resilience (optional, more involved):** briefly cover/block the
    camera or disconnect an external webcam mid-run, if applicable, and
    observe whether the script handles it gracefully or hangs/crashes —
    there is no explicit handling for a camera disappearing mid-session
    in the code as read (only the initial `cap.isOpened()` check is
    handled).

## What this checklist does NOT cover

- No load/performance testing (e.g. how it behaves on an older/slower
  Mac, or with a very high-resolution webcam) — not attempted.
- No test of the `error` event path beyond "camera fails to open at
  startup" — a camera that disconnects mid-run is a different, untested
  code path (see step 10 above).
- No cross-platform testing — this script's alarm mechanism is
  macOS-only by construction; testing on Linux/Windows would first
  require porting `play_alarm_loop()`.

## If a test framework is ever introduced

There is no established pattern to follow yet. The highest-value first
automated tests (if/when this is worth automating) would likely be:
unit tests around the trigger/clear timing logic in `detector_loop()`
(refactored to be testable independent of a real `cv2.VideoCapture`,
e.g. by injecting a frame source and a fake clock), since that's the
core behavioral logic most likely to regress silently.

# FEATURES.md — Feature Inventory

This project has exactly one feature. It's broken down here into its
constituent behaviors for clarity.

## Feature: Webcam phone-use watchdog

- **Purpose:** Nag the person sitting in front of the webcam to put
  their phone down, by detecting a phone in frame and throwing up an
  unmissable fullscreen alarm until it's gone.
- **Flow:**
  1. On start, open the default webcam and load the YOLOv8n model.
  2. Continuously sample frames (every 3rd captured frame) and run
     object detection.
  3. If a "cell phone" (COCO class 67) is detected above a 0.45
     confidence threshold, continuously, for 2 seconds
     (`TRIGGER_SECONDS`) → show a fullscreen red overlay + start a
     repeating alarm sound.
  4. If no phone is detected, continuously, for 3 seconds
     (`CLEAR_SECONDS`) while the overlay is showing → auto-hide the
     overlay + stop the alarm.
  5. ESC on the overlay hides it immediately (alarm stops), but does not
     stop detection — see the caveat below.
  6. Ctrl+C in the launching terminal stops the whole process.
- **Status classification: Mostly complete.** The implementation is
  internally coherent and reads as a finished first draft of the
  intended behavior — no stubs, no `TODO`s, no obviously-missing pieces
  for the stated scope. It is not "Verified complete" because:
  - It has never been runtime-verified in this environment (the local
    `venv/` is broken — see below — and this audit deliberately did not
    launch the live webcam/detection loop).
  - One behavioral edge case (ESC-dismiss re-triggering almost
    immediately if the phone is still in frame) may or may not match the
    intended UX and hasn't been confirmed either way.
- **Files:** `monitor.py` (the entire feature lives in this one file —
  see `FILE_MAP.md` for a line-by-line breakdown).
- **Known issues:**
  1. **Cannot currently run as documented** — `venv/` is broken
     (borrowed/broken symlink chain to two unrelated projects' venvs;
     neither `opencv-python` nor `ultralytics` is installed). See
     `CLAUDE.md` Known issues #1. This is the single blocking issue for
     using this feature at all right now.
  2. **ESC-dismiss re-triggers almost immediately** if the phone is
     still in frame, because the trigger state (`phone_since`) isn't
     cleared just because the overlay was manually hidden — the very
     next qualifying detection frame re-fires `phone_detected`. See
     `ARCHITECTURE.md` → "What happens on detection", step 2, and
     `CLAUDE.md` Known issues #3.
  3. **No visible confirmation the watchdog is actually running and
     watching** — beyond the one console `print()` on webcam-open
     failure, there is no startup confirmation, no periodic heartbeat,
     and no way to tell (short of testing with an actual phone) whether
     detection is silently dead (e.g. after an unhandled exception in
     the detector thread — see `ARCHITECTURE.md` → Major risks #1).
  4. **macOS-only alarm.** `afplay` + a macOS system sound path with no
     fallback — will not play sound (likely will raise an exception) on
     other platforms.
  5. **First run needs internet** to download `yolov8n.pt` if not
     already cached — undocumented anywhere in the repo.
  6. **No way to run it automatically** (no service/scheduler wiring) —
     see `DEPLOYMENT.md`.
- **Remaining work (recommended, not yet done):**
  1. Rebuild `venv/` and confirm the whole pipeline actually runs
     end-to-end against a real webcam and a real phone (see
     `TESTING.md`).
  2. Decide and, if needed, fix the ESC-dismiss re-trigger behavior.
  3. Consider adding at least minimal logging (a startup confirmation,
     a log line per detection event) so "is this actually working" isn't
     purely a black box.
  4. Consider pinning dependency versions in `requirements.txt`.
  5. If unattended/background operation is wanted, add a real deployment
     mechanism (see `DEPLOYMENT.md`'s recommendations) — none exists
     today.

## Features that do NOT exist (explicitly, to avoid ambiguity)

- No configuration UI or CLI flags — every tunable is a hardcoded
  constant in `monitor.py`, edited by hand.
- No logging/reporting to any file, database, or remote service.
- No integration with `phone-watchdog-web` or any other project (see
  `ARCHITECTURE.md` → "Relationship to phone-watchdog-web").
- No support for detecting anything other than a phone (single
  hardcoded COCO class).
- No multi-camera support, no camera selection.
- No snooze/pause control beyond the momentary ESC dismiss.
- No notification-center/OS-native notification — the "alert" is
  entirely a custom fullscreen Tkinter window + `afplay` sound, not a
  macOS `osascript`/`UNUserNotification`-style system notification.

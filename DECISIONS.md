# DECISIONS.md — Architectural Decisions

This repo has no `ADR`/decisions log, no PR descriptions, and a single
commit with a generic message ("Initial commit: phone watchdog monitor
script"). Everything below is reconstructed by reading the code and
labeled **Verified** (directly evidenced by the code/structure) or
**Inferred** (a reasonable reading of *why*, not confirmed anywhere in
writing).

## Use YOLOv8n (nano) specifically, not a larger YOLOv8 variant

- **Status:** Verified (from `YOLO("yolov8n.pt")` in `monitor.py:35`).
- **Likely reasoning (Inferred):** YOLOv8n is the smallest/fastest
  variant in the YOLOv8 family — a reasonable choice for a script meant
  to run continuously in the foreground on a personal laptop without
  dedicated GPU acceleration, trading some detection accuracy for speed.

## Skip frames rather than run inference on every frame

- **Status:** Verified (`DETECT_EVERY_N_FRAMES = 3`, `monitor.py:25`).
- **Likely reasoning (Inferred):** running YOLO inference on every
  captured frame would be unnecessarily expensive for a simple presence
  check; sampling every third frame trades a small amount of detection
  latency for meaningfully lower CPU/GPU load, still fast enough that a
  ~2-second trigger threshold is unaffected in practice.

## Require continuous presence (2s) before alarming, not instant trigger

- **Status:** Verified (`TRIGGER_SECONDS = 2.0`, the `phone_since`
  timing logic in `detector_loop()`).
- **Likely reasoning (Inferred):** avoids false-positive alarms from a
  single misdetected frame or a phone that's only briefly, incidentally
  in frame (e.g. picked up and set back down); requiring sustained
  presence is a simple, effective debounce.

## Require continuous absence (3s) before auto-clearing, not instant clear

- **Status:** Verified (`CLEAR_SECONDS = 3.0`).
- **Likely reasoning (Inferred):** symmetric debounce to the trigger
  side — avoids the overlay flickering on/off if detection briefly
  drops the phone for a single frame while it's still actually in frame
  (e.g. a hand momentarily occluding it). The clear threshold (3.0s) is
  slightly longer than the trigger threshold (2.0s) — Inferred reasoning:
  biases toward "stay alarmed a bit longer" rather than "clear
  eagerly," consistent with the tool's nagging purpose, but this
  asymmetry is not explained anywhere in the code or commit message.

## Tkinter for the overlay, not a web-based or native-notification UI

- **Status:** Verified (`import tkinter as tk`, the `Overlay` class).
- **Likely reasoning (Inferred):** Tkinter ships with the Python standard
  library — no extra dependency needed for a fullscreen native window,
  simplest possible choice for a single-user local script. A macOS
  system notification (`osascript`/`UNUserNotification`) would be
  dismissible/less intrusive; a custom fullscreen red overlay is a
  deliberately harder-to-ignore choice, consistent with a "nag until you
  comply" design goal.

## `afplay` + a bundled macOS system sound, not a bundled audio asset

- **Status:** Verified (`ALARM_SOUND =
  "/System/Library/Sounds/Sosumi.aiff"`, `subprocess.run(["afplay", ...])`).
- **Likely reasoning (Inferred):** avoids shipping/bundling an audio
  file and avoids adding an audio-playback Python dependency — reuses a
  sound already present on any stock macOS install. Trade-off: hardcodes
  macOS as the only supported platform (see `CLAUDE.md` Known issues).

## No persistence of any kind (no log file, no database, no stats)

- **Status:** Verified — no file I/O, no database import, no
  `open(...)` calls anywhere in `monitor.py` besides what `cv2`/
  `ultralytics` do internally to load model weights.
- **Likely reasoning (Inferred):** this is a real-time, momentary nag
  tool, not a tracking/analytics tool — nothing in the code suggests any
  intent to record history. Whether this is a deliberate scope decision
  or simply "not built yet" is genuinely unclear; not stated anywhere.

## No configuration file / environment variables — all tunables are
hardcoded module constants

- **Status:** Verified — no `os.environ`/`os.getenv`/config-file-parsing
  code anywhere.
- **Likely reasoning (Inferred):** appropriate simplicity for a
  single-user script the author edits directly when they want different
  behavior; not designed for distribution to other users with different
  preferences out of the box.

## No relationship to `phone-watchdog-web`

- **Status:** Verified negative — confirmed via a full read of
  `monitor.py`: no network-related imports, no URLs, no shared config.
  Whether this is a deliberate separation-of-concerns decision or simply
  "not built yet" is unknown — not stated anywhere in this repo. See
  `ARCHITECTURE.md`.

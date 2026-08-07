# FILE_MAP.md — Practical Repository Map

The entire repository is three tracked files plus a gitignored `venv/`.
There is no directory structure to speak of.

## `monitor.py` (165 lines — the entire application)

- **Purpose:** Everything — webcam capture, YOLOv8n phone detection,
  trigger/clear timing state machine, the Tkinter fullscreen overlay,
  and the alarm-sound loop. See `ARCHITECTURE.md` for the full flow.
- **Key pieces, in file order:**
  - `monitor.py:22-29` — module-level tunable constants (see
    `CLAUDE.md` → Environment setup table).
  - `monitor.py:31` — the shared `events = queue.Queue()` used to hand
    off state from the detector thread to the Tkinter thread.
  - `monitor.py:34-77` — `detector_loop()`: owns the webcam, runs
    inference, implements the trigger/clear timing logic, queues events.
  - `monitor.py:80-83` — `play_alarm_loop(stop_flag)`: the alarm-sound
    thread body.
  - `monitor.py:86-134` — `Overlay` class: the fullscreen Tkinter
    warning window, `show()`/`hide()`/`showing()`.
  - `monitor.py:137-165` — `main()`: wires up Tkinter, starts the
    detector thread, defines and schedules `poll()`, runs
    `root.mainloop()`.
- **Imports:** `queue`, `subprocess`, `threading`, `time`, `tkinter as tk`
  (standard library); `cv2` (`opencv-python`); `ultralytics.YOLO`.
- **Edit when:** changing detection sensitivity/timing, changing the
  overlay's appearance or dismiss behavior, changing the alarm sound or
  its repeat interval, adding logging, adding any new integration
  (e.g. a real link to `phone-watchdog-web`, if that's ever wanted).
- **Risk:** Medium-high for a project this size — it's the *only* file,
  so any change here is a change to 100% of the application's behavior.
  There are no automated tests to catch a regression (see `TESTING.md`),
  so manual review + a real webcam smoke test is the only safety net.

## `requirements.txt` (2 lines)

- **Purpose:** Lists the two third-party dependencies: `opencv-python`,
  `ultralytics`. No version pins.
- **Edit when:** adding/removing a dependency, or (recommended, not yet
  done) pinning versions for reproducibility.
- **Risk:** Low to edit, but the current unpinned state is itself a
  minor risk — see `CLAUDE.md` Known issues #2.

## `.gitignore` (4 lines)

- **Contents:** `venv/`, `__pycache__/`, `*.pyc`, `.DS_Store`.
- **Purpose:** Keeps the local virtualenv and Python bytecode cache out
  of version control.
- **Edit when:** adding a new kind of generated/local-only file (e.g. a
  future `.env` file, log output, or a downloaded `yolov8n.pt` model
  weights file if it ever ends up written into the repo directory —
  currently it is not present, but if `ultralytics` ever caches it into
  the working directory instead of its default cache location, it should
  be added here so it never gets accidentally committed).
- **Risk:** Low.

## `venv/` (gitignored, not part of tracked history)

- **Purpose:** Intended to be the project's local Python virtual
  environment.
- **Actual state (verified this audit): broken.** `venv/bin/python3` is
  a symlink chain into two unrelated sibling projects'
  virtualenvs (`hyperliquid-bot`, then `sports-betting-project`), and
  neither `opencv-python` nor `ultralytics` is installed in the
  resulting environment. See `CLAUDE.md` Known issues #1 for the fix.
- **Edit when:** never hand-edit; delete and regenerate with
  `python3 -m venv venv && ./venv/bin/pip install -r requirements.txt`.
- **Risk:** N/A (not tracked by git, not part of the deliverable code) —
  but functionally blocking until rebuilt.

## Where to make common changes

- **Change the detection sensitivity or timing** (how long a phone must
  be visible before the alarm fires, or absent before it clears): edit
  `TRIGGER_SECONDS`, `CLEAR_SECONDS`, and/or `CONFIDENCE_THRESHOLD` at
  the top of `monitor.py` (`monitor.py:22-24`). These are deliberate
  tuning values — see `CLAUDE.md` → "DO NOT CHANGE WITHOUT REVIEW" before
  changing them casually.
- **Change which webcam is used:** `cv2.VideoCapture(0)` in
  `detector_loop()` (`monitor.py:36`) is hardcoded to device index `0`
  (the default camera). To support a different camera, this would need
  to become a parameter/constant — no such option exists today.
- **Change detection performance (frame skip rate):** `DETECT_EVERY_N_FRAMES`
  (`monitor.py:25`).
- **Change what counts as "a phone":** `COCO_CELL_PHONE_CLASS_ID = 67`
  (`monitor.py:29`) — only correct for the standard COCO80 class
  ordering used by the stock `yolov8n.pt` checkpoint; see `CLAUDE.md`
  Critical rules before touching this.
- **Change the alarm sound or how often it repeats:** `ALARM_SOUND`
  (macOS-only path) and `ALARM_INTERVAL_SECONDS`
  (`monitor.py:26-27`), and/or `play_alarm_loop()` itself
  (`monitor.py:80-83`) if you need cross-platform audio.
- **Change the overlay's appearance or text:** `Overlay.show()`
  (`monitor.py:96-127`) — the two `tk.Label` widgets and the
  `bg="#8b0000"` color.
- **Change the overlay's dismiss behavior:** `Overlay.hide()`
  (`monitor.py:129-134`) and the ESC binding
  (`self.win.bind("<Escape>", ...)`, `monitor.py:121`) — see
  `CLAUDE.md` Known issues #3 for the current (possibly unintended)
  re-trigger behavior before changing this.
- **Add logging/observability:** currently there is exactly one
  `print()` call (`monitor.py:154`, only on webcam-open failure) — if
  adding more, consider Python's `logging` module rather than more raw
  `print()` calls, and note that stdout may not be visible at all if
  this is ever run as a background/launchd service (see
  `DEPLOYMENT.md`).
- **Add a real integration with `phone-watchdog-web` or any other
  service:** no scaffolding exists for this today (no HTTP client
  dependency, no config file) — this would be new architecture, not a
  small edit. Document the decision in `DECISIONS.md` if undertaken.

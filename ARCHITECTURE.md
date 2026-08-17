# ARCHITECTURE.md — Technical Architecture Reference

## System overview

Phone Watchdog is a single Python process (`monitor.py`) with three
threads of execution coordinated through one thread-safe queue:

1. **The detector thread** (`detector_loop`, a `daemon=True`
   `threading.Thread`) — owns the webcam, runs YOLOv8n inference, and
   decides when a phone has appeared/disappeared for long enough to
   matter.
2. **The Tkinter main thread** — runs `root.mainloop()`, polls the queue
   every 150ms, and is the only thread allowed to touch any Tkinter
   widget (required by Tkinter's threading model).
3. **A short-lived alarm thread** (`play_alarm_loop`, spun up fresh each
   time the overlay is shown) — repeatedly shells out to `afplay` to
   play a system alarm sound while the overlay is visible.

There is no client/server split, no network layer, no database, and no
external service integration. Everything happens in one local process,
in memory, for the lifetime of that process only.

## Architecture diagram

```mermaid
flowchart TB
    subgraph Detector["Detector thread (daemon)"]
        Cam["cv2.VideoCapture(0)<br/>webcam frames"]
        YOLO["YOLOv8n model<br/>(ultralytics.YOLO(\"yolov8n.pt\"))"]
        Logic["Trigger/clear timing logic<br/>TRIGGER_SECONDS / CLEAR_SECONDS"]
        Cam -->|"every 3rd frame<br/>(DETECT_EVERY_N_FRAMES)"| YOLO
        YOLO -->|"class 67 = cell phone,<br/>conf >= CONFIDENCE_THRESHOLD"| Logic
    end

    Q[("queue.Queue()<br/>events: phone_detected / phone_cleared / error")]
    Logic -->|"events.put(...)"| Q

    subgraph MainThread["Tkinter main thread"]
        Poll["poll()<br/>root.after(150, poll)"]
        Overlay["Overlay class<br/>fullscreen Tk.Toplevel"]
        Q -->|"events.get_nowait()"| Poll
        Poll -->|"phone_detected"| Overlay
        Poll -->|"phone_cleared"| Overlay
    end

    subgraph AlarmThread["Alarm thread (spawned on overlay.show())"]
        Alarm["play_alarm_loop()<br/>afplay Sosumi.aiff every 2.5s"]
    end

    Overlay -->|"show(): starts thread"| Alarm
    Overlay -->|"hide(): sets stop Event"| Alarm

    Overlay -.->|"fullscreen red window<br/>+ ESC binding"| User["User (in front of webcam)"]
    Cam -.->|"reads real webcam feed"| User
```

## What triggers a check

Every frame `cap.read()` successfully returns. Only every third frame
(`frame_count % DETECT_EVERY_N_FRAMES != 0` skips the other two) is
actually run through the YOLO model — a simple performance optimization,
not a correctness-relevant gate.

## What happens on detection

1. `model.predict(frame, ...)` returns bounding boxes; the loop checks
   whether any box's class ID equals `COCO_CELL_PHONE_CLASS_ID` (67) at
   or above `CONFIDENCE_THRESHOLD` (0.45).
2. If yes and this is the first frame seeing it, `phone_since` is set to
   the current monotonic time. On every subsequent frame that still sees
   a phone, once `now - phone_since >= TRIGGER_SECONDS` (2.0s), a
   `("phone_detected", None)` tuple is pushed onto the `events` queue —
   **every qualifying frame**, not just once (see `FEATURES.md` /
   `CLAUDE.md` Known issues for the behavioral implication).
3. The Tkinter thread's `poll()` drains the queue every 150ms and calls
   `overlay.show()` for each `phone_detected` event. `show()` is
   idempotent — if the window is already open, it does nothing.
4. `show()` creates a fullscreen, always-on-top `tk.Toplevel` with a red
   background reading "PUT YOUR PHONE DOWN", binds ESC to `hide()`, and
   starts the alarm thread (`play_alarm_loop`), which shells out to
   `afplay <Sosumi.aiff>` every `ALARM_INTERVAL_SECONDS` (2.5s) until
   told to stop.
5. If no phone is seen on a given inference frame, `phone_since` resets
   to `None` and a `clear_since` timer starts instead; once a phone has
   been continuously absent for `CLEAR_SECONDS` (3.0s), a
   `("phone_cleared", None)` event fires, and `poll()` calls
   `overlay.hide()` — which sets the alarm thread's stop `Event` and
   destroys the Tkinter window.
6. If `cap.isOpened()` is ever `False` (webcam unavailable/denied
   permission), a single `("error", "Could not open webcam.")` event is
   queued, `poll()` prints it to the console, and calls `root.quit()`,
   ending the whole program.

## Relationship to `phone-watchdog-web`

**No relationship found.** `monitor.py` was read in full; its only
imports are `queue`, `subprocess`, `threading`, `time`, `tkinter`, `cv2`,
and `ultralytics.YOLO`. There is no HTTP client, no socket, no URL
string, and no shared-config file referencing `phone-watchdog-web`
anywhere in this repository. `monitor.py` also imports no database
library (`sqlite3`, `psycopg`, etc.) — it performs no persistence of any
kind, unlike `phone-watchdog-web`'s Postgres `catches` table. If the two
projects are meant to talk to each other, that integration does not
exist on this side as of this audit (2026-08-06) — it would need to be
added deliberately.

**[Verified 2026-08-17, from both sides]:** independently re-confirmed
during a documentation sweep of `~/Projects/phone-watchdog-web` — that
repo's own application code contains no reference to this repo either,
no shared package, and no shared database. Neither repo has changed
since the original 2026-08-06 audit that first established "no
relationship." Confirmed from both sides, not just inferred from one.

## Error handling

- **Webcam unavailable:** the only handled error path. `cap.isOpened()
  == False` → one `error` event → printed to console → `root.quit()`.
  No retry logic, no user-facing dialog beyond the console print.
- **A dropped/failed individual frame read** (`ok == False` from
  `cap.read()`): handled by sleeping 0.1s and retrying the loop — not
  treated as fatal, no event is queued, no cap on consecutive failures
  (an indefinitely broken camera after a successful open would spin this
  loop forever without ever surfacing an error to the user).
- **No `try`/`except` blocks exist anywhere in `monitor.py`** (confirmed
  via full read and via `grep -n "except"` — zero matches). Any
  exception inside `model.predict()`, `cv2` frame processing, or the
  Tkinter/audio code paths would propagate as an unhandled exception and
  crash the relevant thread (in the detector thread, this would silently
  kill background detection since it's a daemon thread with no
  supervisor restarting it — the Tkinter main loop would keep running
  with a dead detector and no visible indication anything went wrong).
- **No bare `except:` blocks exist** (a common anti-pattern) — this is a
  positive finding, not a gap; there's simply no exception handling at
  all beyond the one `isOpened()` check.

## Major risks

1. **A silent detector-thread death would look like "nothing is being
   detected" with no error surfaced.** Because `detector_loop` has no
   exception handling and runs as an unsupervised daemon thread, any
   uncaught exception inside it (e.g. a transient `cv2`/`ultralytics`
   error) kills detection permanently for the rest of that process's
   life, with the Tkinter window staying open and looking normal. File
   path: `monitor.py:34-77`.
2. **Repeated `phone_detected` events while a phone stays in frame** (see
   "What happens on detection" step 2) mean the event queue is not
   simply "one event per state transition" — it can grow unbounded while
   a phone remains visible, though `poll()`'s `while True: ... except
   queue.Empty` drain pattern (`monitor.py:145-158`) keeps the queue from
   actually backing up in practice, since it's fully drained every
   150ms.
3. **No supervision/restart mechanism** — if the process crashes or is
   killed, detection simply stops; there is no watchdog-for-the-watchdog,
   no launchd/systemd integration (see `DEPLOYMENT.md`).
4. **Broken local `venv/`** (an environment risk, not a code risk) — see
   `PROJECT_STATE.md` / `CLAUDE.md` Known issues #1. This currently
   blocks the script from running at all as documented.
5. **No automated tests** to catch a regression in the trigger/clear
   timing logic or the COCO class-ID mapping if the YOLO model is ever
   swapped. See `TESTING.md`.

# Phone Watchdog

A small local Python script that watches your webcam for a phone. If it
sees one continuously for a couple of seconds, it throws up a fullscreen
red "PUT YOUR PHONE DOWN" warning and plays a repeating alarm sound until
you put the phone down. A personal focus/self-discipline tool — nobody
else can see or receive this; it only nags whoever is sitting in front
of the machine it's running on.

## What it monitors

- Reads frames from your **default webcam** (`cv2.VideoCapture(0)`).
- Runs every 3rd captured frame through a pretrained **YOLOv8n**
  object-detection model (via `ultralytics`) and checks whether it sees
  the COCO class "cell phone" (class ID 67) above a 0.45 confidence
  threshold.
- If a phone is visible continuously for ~2 seconds, it shows a
  fullscreen always-on-top overlay and starts a repeating alarm
  (`afplay` + a macOS system sound). The overlay auto-closes once the
  phone has been out of frame continuously for ~3 seconds, or can be
  dismissed early with ESC (dismissing does not pause detection — see
  `CLAUDE.md` Known issues #3 if the phone is still in view).
- It does **not** identify a specific phone/device — it detects the
  generic visual category "cell phone," the same way it would recognize
  any other cell phone-shaped object.

## What data is collected, and where it lives

**Nothing is stored or transmitted, ever, by this script.** This matters
enough for a webcam-based tool that it's worth being explicit:

- Each webcam frame is read, passed to the YOLO model for in-memory
  inference, and **discarded immediately** — there is no `cv2.imwrite`,
  no log file, no database, and no network call that sends frame data
  anywhere. Confirmed by a full read of `monitor.py`.
- No audio is recorded — the microphone is never touched; the only audio
  activity is *playing* the alarm sound.
- No other sensor or personal data (location, contacts, etc.) is
  accessed.
- All application state (timers, queue, GUI objects) lives only in
  process memory for the lifetime of the running script — nothing
  persists across restarts. There is no config file, no `.env`, and no
  credentials anywhere in this repo.
- The one outbound network call this project makes is a **one-time
  download of the YOLOv8n model weights** (`yolov8n.pt`, from
  Ultralytics' servers) on first run, if not already cached locally by
  the `ultralytics` library. That's model weights, not your data — no
  video/frame content is ever sent out.

See `SECURITY.md` and `DATABASE.md` in this repo for the full audited
detail behind these claims (what was checked, and how).

## Stack

- **Language:** Python 3
- **Webcam capture:** `opencv-python` (`cv2`)
- **Detection:** `ultralytics` (YOLOv8n, pretrained COCO weights)
- **GUI overlay:** Tkinter (Python's built-in Tk binding) — a native
  desktop window, not a web UI
- **Alarm sound:** macOS's `afplay` CLI, invoked via `subprocess`,
  playing a bundled macOS system sound — **macOS only**, no
  cross-platform fallback exists today

## How to run

```bash
cd ~/Projects/phone-watchdog

# Set up the environment (rebuild venv/ from scratch — see CLAUDE.md
# Known issues #1, the committed venv/ currently borrows another
# project's broken interpreter and does not have these installed):
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Run the watchdog:
./venv/bin/python monitor.py

# Stop it:
#   Ctrl+C in the terminal that launched it, or
#   press ESC on the overlay to dismiss it (does not pause detection —
#   see Known issues in CLAUDE.md)
```

First run needs internet access once, to download the YOLOv8n model
weights if they aren't already cached. Camera permission must be granted
to whatever terminal/Python binary launches the script.

There is no lint/test/build command — this is a single 165-line script
with no packaging. See `TESTING.md` for the manual smoke-test checklist
(requires a human physically present with a webcam and a phone).

## Companion project: `phone-watchdog-web`

`~/Projects/phone-watchdog-web` is a separate Next.js dashboard project
living alongside this one. **As of this writing, the two are not wired
together** — this script has no HTTP client, no shared config, and no
network call to that project anywhere in its code (verified by a full
read of `monitor.py`; see `ARCHITECTURE.md` → "Relationship to
phone-watchdog-web" for the full audit note). If you're looking for a
web dashboard, that's the sibling repo; if you're looking for the actual
webcam-watching/alarm behavior, you're in the right place. Any future
integration between the two would be new work, not something already
scaffolded here.

## Full documentation

This repo carries a full handoff documentation set for anyone (human or
AI agent) picking it up cold — see `CLAUDE.md` for the entry point, or
`HANDOFF.md` for the fastest "what do I need to know right now" summary.

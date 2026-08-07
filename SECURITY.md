# SECURITY.md — Defensive Security Review

This is a defensive review of what exists in the repository as of this
audit (2026-08-06). No penetration testing or exploitation was performed
— this is static code review only.

## What data does `monitor.py` collect/observe?

- **Live webcam video**, read frame-by-frame via
  `cv2.VideoCapture(0).read()`. Each frame is:
  1. Passed to the YOLOv8n model for inference (in-memory, local).
  2. **Discarded immediately after inference** — no frame is ever
     written to disk, logged, uploaded, or otherwise retained. Confirmed
     via a full read of `monitor.py`: there is no `cv2.imwrite`, no file
     write, no network send anywhere in the file.
- **No audio is captured** — the microphone is never accessed; audio is
  only ever *played* (the alarm sound), never recorded.
- **No other sensor/personal data** (location, contacts, etc.) is
  accessed — the only OS-level resource this script touches is the
  default webcam and, indirectly, the audio output device (via the
  `afplay` subprocess).

## Where is data stored or sent?

**Nowhere, persistently.** See `DATABASE.md` — there is no file
persistence and no network transmission of any kind in this codebase.
Everything is processed in memory and discarded. This is a materially
strong privacy property *as the code is currently written* — but see
"Caveats" below.

## Credential handling

**No credentials exist in this codebase.** No API keys, no passwords, no
tokens, no `.env` file, no config file of any kind. Confirmed via a
repo-wide search for common secret patterns
(`password|token|api_key|secret|credential`) — zero matches in
`monitor.py`. There is nothing to leak.

## Hardcoded values review (per this audit's explicit checklist)

- **No hardcoded IP addresses** — confirmed via `grep` for
  IPv4-shaped strings; zero matches.
- **No hardcoded credentials** — confirmed above.
- **No hardcoded phone identifiers** (e.g. a specific device ID, IMEI,
  phone number) — this script detects the visual *category* "cell
  phone" via a generic pretrained COCO object-detection model; it does
  not identify or fingerprint any specific device.
- **One hardcoded filesystem path exists:** `ALARM_SOUND =
  "/System/Library/Sounds/Sosumi.aiff"` — a macOS system asset path, not
  sensitive, but worth noting as a portability constraint (see
  `CLAUDE.md`).

## Caveats to the "nothing is stored or sent" property

1. **This property is a reading of the current code, not a guarantee
   enforced by any test.** There is no automated test asserting "no
   frame is ever written to disk" — it's true today because no such code
   path exists, but a future change could add one without any existing
   safeguard catching it. If frame-saving/logging is ever added, it
   should be called out explicitly (in this file and to the user) given
   this is webcam footage of a real person.
2. **The YOLO model weights (`yolov8n.pt`) are downloaded from
   Ultralytics' servers on first run** if not already cached — this is a
   one-time network request for model weights, not a transmission of any
   captured video/frame data, but it is an outbound network call this
   repo doesn't document anywhere (see `API_REFERENCE.md`).
3. **No encryption/access-control is relevant** since nothing is stored
   — this is a non-issue given the current architecture, not an
   oversight.

## Dependency concerns

- `requirements.txt` pins no versions for `opencv-python` or
  `ultralytics` — no `pip-audit`/`safety`/`npm audit`-equivalent scan was
  run as part of this audit (would require actually installing the
  dependencies in a working venv, which this audit avoided doing beyond
  the read-only checks already described in `PROJECT_STATE.md`).
  **Recommend running a dependency vulnerability scan** (e.g. `pip-audit`)
  once `venv/` is rebuilt (see `TASKS.md` TASK-001), before treating
  dependencies as vetted.
- Both dependencies (`opencv-python`, `ultralytics`) are widely-used,
  actively-maintained open-source packages — no specific known-CVE
  concern was identified by inspection, but this was not independently
  verified against a CVE database this audit.

## Physical/environmental security note (specific to this project's
nature, not a typical "app security" concern)

This script actively watches a real webcam and reacts to what it sees.
Anyone who can run it has effectively turned on always-analyzing webcam
monitoring on that machine (though, per the above, nothing is retained
or transmitted). This is a meaningful behavioral fact to flag to any
user of this tool, even though it isn't a traditional "vulnerability" —
it's the entire point of the tool, but worth being explicit about,
especially since there's no visible indicator (no "recording" light
beyond the OS's own camera-in-use indicator, no on-screen "watchdog
active" banner) confirming to a bystander that analysis is happening.

## Production security gaps (headline list)

1. **No frame/audio persistence exists — this is good, but unenforced by
   any test.** Severity: informational, not currently a gap.
2. **No dependency vulnerability scan performed.** Severity:
   unknown/unverified — recommend running one (see above).
3. **No supervision if the detector thread dies silently** (see
   `ARCHITECTURE.md` → Major risks) — not a data-security issue, but a
   reliability/trust issue: a user could believe they're being monitored
   when detection has actually silently stopped.
4. **`venv/` currently borrows another project's Python interpreter**
   (see `CLAUDE.md` Known issues #1) — not a security vulnerability in
   the traditional sense, but worth noting as a sign this environment
   was not carefully isolated from sibling projects on this machine.

## Recommended fixes (priority order)

1. Rebuild `venv/` cleanly and isolated from other projects (see
   `TASKS.md` TASK-001).
2. Run a dependency vulnerability scan (`pip-audit` or similar) once the
   venv is fixed.
3. If this tool is ever extended to persist or transmit any data
   (frames, detection logs, a `phone-watchdog-web` integration), treat
   that as a significant new privacy-relevant decision requiring
   explicit documentation and, ideally, explicit user awareness/consent
   at that time — not something to add quietly.
4. None of the above are currently blocking — this is a local,
   single-user, no-persistence tool with a small, well-understood attack
   surface.

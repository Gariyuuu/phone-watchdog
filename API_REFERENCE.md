# API_REFERENCE.md

## N/A — no API, no outbound calls, no webhooks.

Verified by a full read of `monitor.py`: the only imports are `queue`,
`subprocess`, `threading`, `time`, `tkinter`, `cv2`, and
`ultralytics.YOLO`. There is no `requests`, `urllib`, `http.client`,
`socket`, `websockets`, or any other networking library imported or used
anywhere in this file, and no URL string appears anywhere in the code.

## Specifically checked and ruled out

- **No outbound HTTP/API calls of any kind** — confirmed by the import
  list above and a full manual read of every function.
- **No calls to `phone-watchdog-web`** (the sibling repo at
  `~/Projects/phone-watchdog-web`) or any other service — no shared
  config, no hardcoded URL, no environment variable that could point at
  one. See `ARCHITECTURE.md` → "Relationship to phone-watchdog-web" for
  the full note.
- **No webhooks, incoming or outgoing** — there is no server/listener of
  any kind in this codebase; the process only ever reads from the local
  webcam and writes to the local screen/speaker.
- **No third-party SaaS/notification integration** (no Slack/email/push
  notification API) — the only "alert" mechanisms are the local Tkinter
  overlay and the local `afplay` subprocess call.
- **The only "external" thing this code touches:** `ultralytics`'s own,
  internal, first-run download of the `yolov8n.pt` model weights file —
  this is third-party library behavior, not an API this project's own
  code defines or calls directly, and it is not documented anywhere in
  this repo (see `DATABASE.md` / `CLAUDE.md` Known issues).

## If a real integration is ever added

There is no existing API client pattern, auth pattern, or config
mechanism to extend in this codebase — building one would be new
architecture. Document the decision in `DECISIONS.md` and add any new
config values as environment-variable placeholders (see `CLAUDE.md` →
Environment setup) rather than hardcoding endpoints or credentials.

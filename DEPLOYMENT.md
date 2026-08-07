# DEPLOYMENT.md

## How this script is currently intended to run

**Manual, foreground-only execution.** Per `monitor.py`'s own docstring
(`monitor.py:1-10`):

```
Run:  ./venv/bin/python monitor.py
Stop: Ctrl+C in the terminal, or press ESC on the overlay to dismiss it.
```

There is no evidence anywhere in this repository of any automated/
background run mechanism:

- **No `launchd` `.plist` file** anywhere in the repo (checked via a
  repo-wide search for `*.plist` — none found).
- **No cron reference** — no `crontab` file, no comment mentioning cron,
  no `cron` string anywhere in the codebase.
- **No `systemd` unit file** (not relevant on macOS anyway, but checked
  for completeness — none found).
- **No shell wrapper script** (e.g. `run.sh`, `start.sh`) — none exists;
  the docstring's command is the only documented invocation.
- **No Docker/container configuration** — no `Dockerfile`, no
  `docker-compose.yml`.
- **No packaging** (`setup.py`, `pyproject.toml`, `Pipfile`) that would
  let it be installed as a CLI tool.

**Conclusion:** as of this audit, the only way to run this is to
manually open a terminal, `cd` into the repo, and run
`./venv/bin/python monitor.py` yourself, keeping that terminal window
(and the process) alive for as long as you want the watchdog active.

## What "deployment" would mean for this project (there is no hosting
target — it is not a web app)

There is no server/cloud deployment target for this project — it is a
local desktop script that needs direct access to the machine's webcam
and audio output. "Deployment" here means: getting it to start reliably
without a human manually running the command each time, if that's ever
wanted.

## Recommended options (not implemented — Inferred/Recommended only)

If unattended/automatic startup is ever desired, plausible options
(standard macOS mechanisms, none currently present in this repo):

1. **`launchd` LaunchAgent** — a `.plist` file in
   `~/Library/LaunchAgents/` pointing at `./venv/bin/python monitor.py`
   with the working directory set to this repo, configured to run at
   login. This is the standard macOS mechanism for a per-user background
   process. Would need `StandardOutPath`/`StandardErrorPath` configured
   given the script's near-total lack of logging (see `UI_SYSTEM.md`),
   or debugging a launchd-run instance would be very difficult.
2. **A manual shell alias/script** the user runs themselves at the start
   of a work session — lower effort, no login-time surprise (a
   fullscreen webcam-watching overlay tool silently starting at every
   login could itself be an unwelcome surprise if not clearly
   remembered/wanted).

Neither of these has been implemented, requested, or hinted at anywhere
in the repo — flagged here only as the standard next step *if* automatic
background operation is ever wanted. Do not implement either without
explicit confirmation from the project owner (per this audit's
instructions not to add new features).

## Pre-flight checklist before running (manual, today)

1. `venv/` must be rebuilt first — see `TASKS.md` TASK-001 (the
   currently-committed `venv/` is broken and does not have the required
   dependencies installed).
2. Camera permission must be granted to whatever terminal/Python binary
   launches the script (macOS will prompt on first `cv2.VideoCapture`
   access if not already granted; if previously denied, `cap.isOpened()`
   will return `False` and the script will print an error and exit
   immediately).
3. Internet access is needed on first run only, to download
   `yolov8n.pt` if not already cached.
4. No environment variables need to be set — none are read (see
   `CLAUDE.md` → Environment setup).

## Rollback

Not applicable — there is no deployed environment to roll back. "Undo"
is simply: stop the process (Ctrl+C).

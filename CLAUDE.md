# CLAUDE.md — Operating Manual for Phone Watchdog

This file is the primary entry point for any AI coding agent (or human)
picking up this repository. Read this first, then `PROJECT_STATE.md`, then
`TASKS.md`, before touching code.

This entire memory system (`CLAUDE.md`, `PROJECT_STATE.md`, `ARCHITECTURE.md`,
`FILE_MAP.md`, `FEATURES.md`, `TASKS.md`, `ROADMAP.md`, `DECISIONS.md`,
`DATABASE.md`, `API_REFERENCE.md`, `UI_SYSTEM.md`, `SECURITY.md`,
`TESTING.md`, `DEPLOYMENT.md`, `CHANGELOG.md`, `SESSION_LOG.md`,
`HANDOFF.md`) was generated on **2026-08-06** by auditing the actual
repository (source, config, git history) — not by recalling prior chat
history. Where something couldn't be verified from the repo, it is
labeled **Unverified**, **Inferred**, or **Unable to verify** rather than
stated as fact.

## Project identity

- **Name:** Phone Watchdog (repo name: `phone-watchdog`)
- **One-sentence description:** A local, single-file Python script that
  watches a webcam feed for a phone in frame using YOLOv8n object
  detection, and if a phone is visible continuously for a couple of
  seconds, throws up a fullscreen red warning overlay and plays a
  repeating alarm sound until the phone is put down.
- **Detailed summary:** `monitor.py` opens the default webcam (`cv2.VideoCapture(0)`),
  runs every third captured frame through an Ultralytics YOLOv8n object
  detection model, and checks whether any detected box is COCO class 67
  ("cell phone") above a confidence threshold. If a phone is seen
  continuously for `TRIGGER_SECONDS` (2.0s), the script fires a
  `phone_detected` event that a Tkinter-based UI thread turns into: (a) a
  fullscreen, always-on-top red overlay window reading "PUT YOUR PHONE
  DOWN", and (b) a background thread that plays a macOS system alarm
  sound (`afplay /System/Library/Sounds/Sosumi.aiff`) on a repeating
  interval. The overlay auto-closes once the phone has been absent from
  frame for `CLEAR_SECONDS` (3.0s), or can be dismissed early with ESC
  (see "Known issues" — dismissing with ESC does not stop detection, so
  the overlay can immediately reappear if the phone is still in frame).
- **Purpose (inferred from code, not stated anywhere in the repo):** a
  personal focus/self-discipline tool — nag yourself (or whoever is in
  front of the webcam) into putting a phone down during work/study by
  webcam. There is no multi-user concept, no accounts, no remote
  reporting; it is purely local and self-contained.
- **Target audience:** A single local user running this on their own
  Mac while working, as a self-imposed anti-phone-distraction nag. Not
  built for distribution, install, or use by anyone other than the
  person running it in front of their own webcam.
- **Current development stage:** Very early / minimal. One application
  file (`monitor.py`), two commits total (the app itself, plus a later
  documentation batch), no tests, no packaging, no automation to run it
  as a service.
  Functionally it reads as a complete first draft of the described
  behavior (see "Completeness classification" below), but it has never
  been runtime-verified in this environment because the project's own
  `venv/` is broken (see "Known issues" — this is the single most
  important fact for anyone picking this up).
- **Production status:** **Not deployed anywhere.** This is a local
  script, not a hosted service. No evidence of it being packaged,
  scheduled, or run as a background service (no launchd `.plist`, no
  cron reference, no `systemd` unit — confirmed by a repo-wide search).
- **Repository type:** Single-file Python script + `requirements.txt` +
  a local `venv/` (gitignored). Not a monorepo, not a package, no `src/`
  layout, no `setup.py`/`pyproject.toml`.
- **Relationship to `phone-watchdog-web`:** **None found.** `monitor.py`
  was read in full: it imports only `queue`, `subprocess`, `threading`,
  `time`, `tkinter`, `cv2`, and `ultralytics.YOLO`. There is no
  `requests`/`urllib`/`http`/`socket` import, no URL string, no shared
  config file, and no reference to `phone-watchdog-web` anywhere in this
  repo. The sibling repo at `~/Projects/phone-watchdog-web` is a
  **separate, unrelated codebase** as far as this repo's contents show —
  if a relationship exists, it is not implemented on this side and would
  need to be confirmed independently from that repo.
- **Important scope note:** `~/Projects` (the parent of this repo) is
  **not** a monorepo — it's roughly 20 unrelated, independently-pushed
  git repos belonging to the same developer. Nothing in this memory
  system applies outside `~/Projects/phone-watchdog`.

## Current status

See `PROJECT_STATE.md` for the exact, timestamped snapshot. Summary:

- **Latest milestone:** Initial commit (`d2c04e6`, 2026-08-03) —
  `monitor.py`, `requirements.txt`, `.gitignore` — followed by a
  documentation-only commit (`6631562`, 2026-08-06) adding the 17-file
  handoff memory system, and `README.md` added 2026-08-07 (untracked as
  of writing this line; see `PROJECT_STATE.md` for exact current git
  state). No application-code commits beyond the initial one.
- **Current blockers:** The project's own `venv/` is broken — see
  "Known issues" below. As shipped, running the script via the exact
  command its own docstring recommends (`./venv/bin/python monitor.py`)
  will fail immediately with `ModuleNotFoundError: No module named
  'cv2'`. This was discovered and verified during this audit, not
  previously documented anywhere.
- **Highest-priority next task:** Rebuild `venv/` from scratch
  (`python3 -m venv venv && ./venv/bin/pip install -r requirements.txt`)
  and do a real, human-supervised smoke test in front of the actual
  webcam before trusting the detection logic. See `TASKS.md`.

## Completeness classification

**Mostly complete**, with one critical environment-level caveat:

- The detection → alarm → overlay → auto-clear logic reads as a coherent,
  finished implementation of the stated behavior when read line-by-line —
  no `TODO`/`FIXME`/placeholder code, no stubbed-out functions, no dead
  branches.
- However, it has **never been confirmed to actually run** in this
  environment: the local `venv/` does not have the required dependencies
  installed (see below), and this audit deliberately did not launch the
  webcam/detector loop (per the task's own safety instructions, to avoid
  acting on a real camera/personal data without first fully understanding
  the code — which has now been done by full manual read-through). Until
  someone runs it against a real webcam with a real phone, "the detection
  actually works as intended" is **Unable to verify**, not confirmed.
- First run will also require internet access, undocumented anywhere in
  the repo: `ultralytics` auto-downloads the `yolov8n.pt` model weights
  file on first `YOLO("yolov8n.pt")` call if it isn't already cached
  locally — no `.pt` file is committed to this repo (confirmed via
  `find . -iname "*.pt"`).

## Technology stack

Determined by reading `requirements.txt` and `monitor.py` directly — not
guessed.

- **Language:** Python. **Exact version this project was written/tested
  against is Unable to verify** — no `.python-version`, no version pin
  in `requirements.txt`, and the committed `venv/pyvenv.cfg` reports
  `version = 3.9.6`, but (see "Known issues") that `venv/` is not
  actually this project's own environment — it's a broken symlink chain
  borrowing another project's interpreter, so 3.9.6 should not be
  trusted as "the" version this code targets, only as "a" version that
  happens to be reachable through the current broken venv.
- **Core dependencies (`requirements.txt`, unpinned):**
  - `opencv-python` — webcam capture (`cv2.VideoCapture`) and frame
    handling.
  - `ultralytics` — YOLOv8 object detection (`from ultralytics import
    YOLO`), using the pretrained `yolov8n.pt` (YOLOv8-nano) checkpoint
    and the standard 80-class COCO label set (class ID 67 = "cell
    phone").
- **Standard library used:** `queue` (thread-safe event handoff between
  the detector thread and the Tkinter main loop), `subprocess` (shelling
  out to macOS's `afplay` for the alarm sound), `threading`, `time`,
  `tkinter` (the overlay GUI).
- **GUI toolkit:** Tkinter (Python's bundled Tk binding) — a native
  desktop overlay window, not a web UI.
- **Audio:** macOS's built-in `afplay` CLI, invoked via `subprocess.run`,
  playing a bundled macOS system sound
  (`/System/Library/Sounds/Sosumi.aiff`). **This hardcodes a macOS-only
  path and a macOS-only command** — the script as written will not work
  unmodified on Linux/Windows (no cross-platform audio fallback exists).
- **No web framework, no database, no external API client, no test
  framework, no linter/formatter config** exist anywhere in this repo.
- **Package manager:** `pip` via a plain `requirements.txt` (no
  `pip-tools`/`poetry`/`uv` lockfile).

## Essential commands

All commands below are **as documented in `monitor.py`'s own docstring**
and inferred from the repo layout — there is no separate run script,
Makefile, or `README.md` in this repo.

```bash
cd ~/Projects/phone-watchdog

# Set up the environment (the existing venv/ is broken — see Known issues;
# rebuild it before attempting to run anything):
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Run the watchdog (per monitor.py's own docstring):
./venv/bin/python monitor.py

# Stop it:
#   Ctrl+C in the terminal that launched it, or
#   press ESC on the overlay to dismiss it (does NOT stop detection —
#   see Known issues)

# Syntax-only check (safe, does not open the webcam or any GUI):
./venv/bin/python -m py_compile monitor.py
```

There is no lint command, no test command, no build step, and no
dedicated run script (e.g. no `run.sh`) anywhere in the repo — confirmed
via a repo-wide file search during this audit.

## Repository structure

```
phone-watchdog/
├── monitor.py           # The entire application. ~165 lines. See ARCHITECTURE.md / FILE_MAP.md.
├── requirements.txt      # 2 unpinned dependencies: opencv-python, ultralytics
├── .gitignore            # venv/, __pycache__/, *.pyc, .DS_Store
└── venv/                 # Local virtualenv — gitignored, NOT part of the repo's
                           # tracked history. Currently BROKEN (see Known issues) —
                           # do not assume it works; rebuild it before relying on it.
```

That's the entire repository. There is no `src/` layout, no `tests/`
directory, no `docs/` directory, no CI config (no `.github/workflows/`),
no README, and no packaging metadata (`setup.py`/`pyproject.toml`)
anywhere.

## Architecture summary

See `ARCHITECTURE.md` for the full write-up with a Mermaid diagram. Short
version:

- **One process, two threads, plus the Tkinter main loop.** A background
  `detector_loop()` thread continuously reads webcam frames, runs YOLOv8n
  inference on every 3rd frame, and pushes `("phone_detected", None)` /
  `("phone_cleared", None)` / `("error", message)` tuples onto a
  thread-safe `queue.Queue`.
- **Tkinter's main loop polls that queue** every 150ms (`root.after(150,
  poll)`) on the main thread (required — Tkinter is not thread-safe) and
  reacts by showing/hiding a fullscreen `Overlay` window.
- **A third, short-lived thread** plays the alarm sound in a loop
  (`play_alarm_loop`) while the overlay is showing, stopped via a
  `threading.Event` when the overlay is hidden.
- **No persistence, no network calls, no external service integration**
  anywhere in the runtime path — everything is in-memory, local, and
  ephemeral. State resets completely every time the process restarts.

## Environment setup

**No environment variables are read anywhere in `monitor.py`** — confirmed
via a full read of the file; there is no `os.environ`/`os.getenv` call at
all. Every tunable is a hardcoded module-level constant at the top of
`monitor.py`:

| Constant | Current value | What it controls |
|---|---|---|
| `TRIGGER_SECONDS` | `2.0` | How long a phone must be continuously visible before the alarm fires |
| `CLEAR_SECONDS` | `3.0` | How long the phone must be continuously absent before the overlay auto-closes |
| `CONFIDENCE_THRESHOLD` | `0.45` | Minimum YOLO detection confidence to count as "a phone" |
| `DETECT_EVERY_N_FRAMES` | `3` | Run inference on every Nth captured frame (perf tuning) |
| `ALARM_SOUND` | `/System/Library/Sounds/Sosumi.aiff` | **Hardcoded macOS system sound path** |
| `ALARM_INTERVAL_SECONDS` | `2.5` | Delay between repeated alarm plays while the overlay is up |
| `COCO_CELL_PHONE_CLASS_ID` | `67` | The COCO class index YOLO uses for "cell phone" (standard COCO ordering — not project-specific) |

None of these are secrets — they're all plain tunables safe to see in
plaintext. **If this project ever grows configuration that genuinely
should be an environment variable** (e.g. a webcam device index other
than `0`, a different alarm sound path for cross-platform support, or —
if a real integration with `phone-watchdog-web` is ever added — an API
URL/token), add it with a placeholder in a new `.env.example` file and
document it here. As of this audit, **no `.env`, `.env.example`, or any
config file exists in this repo**, and none is currently needed for the
script to run (only for the venv to be correctly set up — see Known
issues).

## Critical rules — DO NOT CHANGE WITHOUT REVIEW

- **`COCO_CELL_PHONE_CLASS_ID = 67`** — this must stay in sync with
  whatever COCO class ordering the loaded YOLO checkpoint actually uses.
  It is currently correct for the standard Ultralytics COCO80 class list
  (index 67 = "cell phone"), but if the model checkpoint (`yolov8n.pt`)
  is ever swapped for a differently-trained/ordered model, this constant
  must be re-verified, not assumed.
- **The trigger/clear timing constants (`TRIGGER_SECONDS`,
  `CLEAR_SECONDS`, `CONFIDENCE_THRESHOLD`)** — these were presumably
  tuned by the author for their own webcam/environment (not documented
  anywhere why these exact values were chosen — see `DECISIONS.md`,
  marked Inferred). Changing them changes real-world nag sensitivity;
  treat as a deliberate behavior change, not incidental cleanup.
- **`ALARM_SOUND`'s hardcoded macOS path** — do not change this casually
  to "improve portability" without actually testing on the target
  platform; there is no fallback/cross-platform audio path implemented,
  so a naive change could silently break the alarm entirely.
- **Do not commit `venv/`** — it's gitignored for a reason (large,
  machine-specific). The currently-committed... wait, it is NOT
  committed (confirmed via `git ls-files` / `.gitignore`) — keep it that
  way.
- **Do not run `monitor.py` unattended against a live webcam** without
  understanding that it will actively capture and analyze real video of
  whoever is in front of the camera (locally, in-memory only — no
  evidence of any frame being saved or transmitted anywhere, but this
  has not been exhaustively fuzz-tested, only read).

## Known issues

1. **CRITICAL — the committed `venv/` is broken and does not contain the
   project's dependencies.** Verified this audit:
   `venv/bin/python3` is a symlink to
   `/Users/gariyuu/Projects/hyperliquid-bot/.venv/bin/python3`, which is
   itself a symlink to
   `/Users/gariyuu/Projects/sports-betting-project/.venv/bin/python3` —
   i.e. this venv's interpreter is not phone-watchdog's own Python at
   all, it's borrowed (likely accidentally, e.g. `python3 -m venv venv`
   run with an already-broken `python3` on `PATH` at creation time) from
   two unrelated sibling projects. Running `venv/bin/python3 -m pip list`
   shows only `pip` and `setuptools` — **neither `opencv-python` nor
   `ultralytics` is installed** anywhere in the resolved environment.
   Running `./venv/bin/python monitor.py` exactly as the script's own
   docstring instructs will fail immediately with `ModuleNotFoundError:
   No module named 'cv2'`. **Fix: delete and rebuild `venv/` from
   scratch** (`rm -rf venv && python3 -m venv venv && ./venv/bin/pip
   install -r requirements.txt`) before attempting to run this script.
   Not fixed during this audit (documentation-only pass, per
   instructions — flagging rather than acting).
2. **No pinned dependency versions.** `requirements.txt` lists
   `opencv-python` and `ultralytics` with no version constraints — a
   fresh `pip install` at any future date could pull a materially
   different `ultralytics`/`opencv-python` release than whatever the
   author originally tested against (unknown, since no lockfile exists).
3. **ESC does not stop detection, only hides the overlay.** In
   `detector_loop()`, once `phone_since` has been set and
   `TRIGGER_SECONDS` has elapsed, **every subsequent detection frame
   that still sees a phone re-queues a `phone_detected` event** (there is
   no "already firing" guard — `phone_since` is only cleared when the
   phone stops being seen). `Overlay.show()` is idempotent while the
   window is open, but if the user presses ESC (which calls
   `Overlay.hide()`, destroying the window and stopping the alarm), and
   the phone is still in frame at the next detection frame (as fast as
   ~3 captured frames later, given `DETECT_EVERY_N_FRAMES = 3`), the
   overlay will immediately reappear. This means ESC functions more like
   a very brief flicker-dismiss than a real "I acknowledge, leave me
   alone" dismissal, which may not match a user's intuitive expectation
   from the docstring's wording ("press ESC to dismiss it"). Not
   necessarily a bug — may be intentional ("keep nagging until the phone
   is actually gone") — but worth confirming intent with the project
   owner rather than assuming either reading.
4. **First run requires internet access, undocumented.** `YOLO("yolov8n.pt")`
   will download the model weights from Ultralytics' servers on first use
   if not already cached locally (no `.pt` file is committed to this
   repo). Nothing in the repo documents this network dependency or where
   the model gets cached.
5. **macOS-only.** `ALARM_SOUND` and the `afplay` subprocess call are
   both macOS-specific with no fallback — this script will not play any
   alarm sound (and will likely raise `FileNotFoundError` from
   `subprocess.run(["afplay", ...])`) on Linux or Windows.
6. **No automated tests, no CI, no lint config.** See `TESTING.md`.
7. **No mechanism to run this automatically** (no launchd `.plist`, no
   cron entry, no systemd unit found anywhere in the repo) — it is a
   manual, foreground-only script as currently packaged. See
   `DEPLOYMENT.md`.
8. **One `print()` statement is the only console output**
   (`print(f"Error: {payload}")` in `main()`'s `poll()`, fired only if
   the webcam fails to open) — not a debug leftover, it's the script's
   one and only user-facing error surface, but it's easy to miss since
   nothing else is logged (no confirmation the detector loop started
   successfully, no periodic heartbeat, no confirmation a phone was
   detected beyond the overlay itself appearing).

## AI working instructions

Future Claude Code sessions (or any AI agent) working in this repo must:

1. Read `CLAUDE.md` (this file).
2. Read `PROJECT_STATE.md`.
3. Read `TASKS.md`.
4. Read whichever of `ARCHITECTURE.md` / `FEATURES.md` / `API_REFERENCE.md`
   / `DATABASE.md` / `UI_SYSTEM.md` / `SECURITY.md` / `DEPLOYMENT.md` is
   relevant to the task at hand.
5. Inspect `monitor.py` directly before changing it — do not trust a
   memory file's description of its exact behavior over reading the
   function itself; memory files can go stale.
6. Check `git status` before modifying files.
7. Avoid overwriting unrelated work.
8. Make small, reviewable changes — this is a 165-line single-file
   script; there is rarely a reason for a sprawling diff.
9. Run `./venv/bin/python -m py_compile monitor.py` after any change (a
   syntax-only, safe check). **Do not launch `monitor.py`'s full
   webcam/detection/GUI loop** without explicit user permission and
   presence — it opens a real camera and drives a real fullscreen
   overlay + audible alarm.
10. Update documentation after meaningful changes (see the permanent
    rules below).
11. Never claim something works without verification — "it compiles" is
    not the same claim as "it correctly detects a phone in the webcam
    feed." Say which one you mean.
12. Never expose secrets in output, commits, or documentation. (As of
    this audit there are none in this repo — keep it that way if any are
    ever introduced, e.g. an API key for a future `phone-watchdog-web`
    integration.)
13. Never silently add a network call, external API integration, or
    persistence layer that doesn't exist today without it being the
    explicit point of the task — this script is currently fully local
    and offline-after-first-run by design (as far as this audit can
    tell); don't quietly change that.
14. Never assume `venv/` works — it is currently broken (see Known
    issues #1). Verify or rebuild it before relying on it.
15. Never remove a dependency without checking all usages first.
16. Never change `COCO_CELL_PHONE_CLASS_ID`, the alarm sound path, or the
    trigger/clear timing constants without it being the explicit point
    of the task (see "DO NOT CHANGE WITHOUT REVIEW" above).
17. Record unresolved uncertainty in the relevant memory file rather than
    guessing and presenting a guess as fact.
18. Never commit, push, deploy, reset, or discard changes unless the user
    explicitly asks for that specific action.

## Permanent rules for future development

**After every meaningful coding task:**

1. Update `PROJECT_STATE.md` with the new exact stopping point.
2. Update `TASKS.md` (move/close tasks, add new ones discovered).
3. Append an entry to `SESSION_LOG.md` (do not overwrite prior entries).
4. Update whichever of `FEATURES.md` / `ARCHITECTURE.md` /
   `API_REFERENCE.md` / `DATABASE.md` / `TESTING.md` / `DEPLOYMENT.md` /
   `SECURITY.md` is affected by the change.
5. Remove or correct stale information you notice, even if unrelated to
   your task — but note what you changed and why in `SESSION_LOG.md`.
6. Record meaningful architectural decisions in `DECISIONS.md`.
7. Run the verification available (`py_compile` at minimum; a real
   webcam smoke test only with explicit user presence/permission — see
   `TESTING.md`).
8. Clearly record anything not verified (e.g. "compiles but not
   runtime-tested against a real webcam") rather than implying full
   verification.
9. Treat this repository's memory files as the permanent source of
   project memory — do not rely on chat history surviving to the next
   session.

**Before every meaningful coding task:**

1. Read `CLAUDE.md`.
2. Read `PROJECT_STATE.md`.
3. Read `TASKS.md`.
4. Read the relevant technical documentation file(s).
5. Run `git status` and `git diff --stat`.
6. Inspect `monitor.py` directly.
7. Confirm the requested work isn't already done.
8. Preserve unrelated work — don't `git checkout`/`reset`/`clean` without
   first stashing or confirming with the user.
9. Identify risks before modifying anything listed under "DO NOT CHANGE
   WITHOUT REVIEW" above.

# HANDOFF.md — Start Here

You are picking up **Phone Watchdog** with no memory of any prior
conversation. This file is your fastest path to being useful. Everything
here is backed by the other memory files in this repo root, all written
2026-08-06 from a direct audit of the actual code — not from chat
history.

## What is this project?

A single Python script (`monitor.py`) that watches your webcam for a
phone, and if it sees one continuously for ~2 seconds, throws up a
fullscreen red "PUT YOUR PHONE DOWN" overlay with a repeating alarm sound
until the phone is put away. Uses OpenCV for webcam capture and a
YOLOv8n object-detection model (via `ultralytics`) to detect the phone.
Entirely local — no network calls at runtime beyond a one-time model
weights download, no persistence, no accounts, no relationship to the
sibling `phone-watchdog-web` repo (confirmed by code, not just assumed).

Full detail: `CLAUDE.md` (read this in full before doing anything else).

## What should I read first?

In order:
1. `CLAUDE.md` — identity, stack, known issues, critical rules.
2. `PROJECT_STATE.md` — the exact stopping point, right now.
3. `TASKS.md` — what's queued, starting with TASK-001.
4. Whichever of `ARCHITECTURE.md` / `FEATURES.md` / `SECURITY.md` /
   `TESTING.md` / `DEPLOYMENT.md` is relevant to what you're about to do.

## What is the current task?

**No application-code task is in progress.** This session's work was a
documentation-only audit (building this 17-file memory system from
scratch — the repo had none before). That work is complete: all 17 files
exist, are internally consistent, and contain no invented facts or
secrets. The recommended next task, if the user wants to continue, is
`TASKS.md` → **TASK-001: rebuild the broken `venv/`** — but confirm with
the user before starting it; don't assume it's wanted without asking.

## What works right now?

- `monitor.py` is syntactically valid Python (`py_compile` passes).
- The code, read line-by-line, is internally coherent and appears to be
  a complete first draft of its stated behavior — no stubs or TODOs.
- Git itself is healthy: clean tree, one commit, one branch, tracking a
  real GitHub remote.

## What is broken?

**The local `venv/` does not work.** `venv/bin/python3` is a symlink
chain into two *other, unrelated* projects'
virtualenvs (`~/Projects/hyperliquid-bot/.venv` →
`~/Projects/sports-betting-project/.venv`), and neither
`opencv-python` nor `ultralytics` — the two things `monitor.py` actually
needs — is installed anywhere in that chain. Running the script exactly
as its own docstring instructs (`./venv/bin/python monitor.py`) fails
immediately with `ModuleNotFoundError: No module named 'cv2'`. This was
discovered during this audit and had never been documented before.

Beyond that: whether the actual detection/alarm/overlay behavior works
correctly against a real webcam is **Unable to verify** — it has never
been run in this environment (deliberately not attempted this session,
per the task's own safety instructions about not acting on real
camera/personal data before fully understanding the code — which has
now been done via full manual read).

## What should I do next?

If the user wants this script actually usable: `TASKS.md` TASK-001
(rebuild `venv/`) then TASK-002 (a real, human-supervised smoke test —
see `TESTING.md`'s full checklist). If the user has something else in
mind, don't assume — ask.

## Which files are most important?

- `monitor.py` — the entire application (165 lines, one file). See
  `FILE_MAP.md` for a line-by-line breakdown.
- `requirements.txt` — the 2 dependencies (unpinned).

There genuinely are no other source files — this is a minimal repo.

## Which areas are dangerous to modify?

See `CLAUDE.md` → "DO NOT CHANGE WITHOUT REVIEW". Headline items:
`COCO_CELL_PHONE_CLASS_ID` (must match the loaded model's class
ordering), the trigger/clear timing constants (deliberately tuned,
reason not documented — don't change casually), and the hardcoded
macOS-only alarm path (no fallback exists if changed carelessly). Also:
**never launch the full webcam/detection/GUI loop unattended** — it opens
a real camera.

## Which commands should I run first?

```bash
cd ~/Projects/phone-watchdog
git status                              # confirm this matches PROJECT_STATE.md — don't assume, check
./venv/bin/python -m py_compile monitor.py   # safe syntax check only
```

Do **not** run `./venv/bin/python monitor.py` yet — it will fail
(`ModuleNotFoundError: No module named 'cv2'`) until `venv/` is rebuilt
(see TASK-001), and even after rebuilding, only run the full script when
a human is physically present (it opens a real webcam).

## How do I verify the app still works?

There is no automated test suite (see `TESTING.md`) — the only
verification path is: (1) `py_compile` for a syntax check, and (2) a
real, human-supervised manual smoke test per `TESTING.md`'s checklist,
which requires a rebuilt `venv/` and a person physically present with a
webcam and a phone.

---

## Prompt for the next Claude Code account

Copy-paste this to start a new session cleanly:

```
Read CLAUDE.md, PROJECT_STATE.md, and TASKS.md in full before doing
anything else. Then:

1. Run `git status` and `git log --oneline -5` and confirm the repo
   state matches what PROJECT_STATE.md describes. If it doesn't
   (someone else has committed/changed things since), stop and tell me
   what's different before proceeding.
2. Run `./venv/bin/python -m py_compile monitor.py` and confirm it still
   passes (safe, syntax-only — does not open the webcam).
3. In 3-5 sentences, summarize your understanding of: what this project
   is, what it actually monitors and how, and what the single biggest
   blocker is right now (the broken venv/). I want to confirm you've
   actually absorbed the memory files, not just skimmed them.
4. Flag anything in CLAUDE.md/PROJECT_STATE.md/TASKS.md/FEATURES.md that
   looks stale or contradicts what you find in the actual code — don't
   silently work around a contradiction, surface it.
5. Do NOT run the full monitor.py webcam/detection/GUI loop unless I am
   explicitly present and have asked you to — it opens a real camera and
   drives a real fullscreen overlay + audible alarm.
6. If I ask you to fix the broken venv/ (TASK-001), rebuild it cleanly
   (`rm -rf venv && python3 -m venv venv && ./venv/bin/pip install -r
   requirements.txt`) and confirm `cv2`/`ultralytics` import
   successfully — don't just assume it worked.
7. After completing any meaningful work, update PROJECT_STATE.md,
   TASKS.md, and append to SESSION_LOG.md before ending your session —
   don't let the next handoff start from a stale snapshot.
```

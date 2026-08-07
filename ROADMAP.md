# ROADMAP.md

There is no written roadmap anywhere in this repository (no issues, no
project board reference, no comments describing future plans). Everything
below is **Inferred** from the current state of the code and repo, not
sourced from any explicit statement by the project owner. Confirm with
the user before treating any of this as committed direction.

## Current milestone

**Get the existing feature actually running and verified.** The code
appears functionally complete for its stated scope (see `FEATURES.md`),
but has never been confirmed to run in this environment, and the local
`venv/` is currently broken. The realistic "current milestone" is:
rebuild `venv/`, do a real smoke test, fix anything the smoke test turns
up (see `TASKS.md` TASK-001/TASK-002).

## Next milestone (inferred, unconfirmed)

If the current implementation is confirmed working, plausible next steps
based purely on gaps visible in the code (not on any stated intent):

- Add at least minimal logging/observability so "is this actually
  working" doesn't require a live phone test every time.
- Resolve the ESC-dismiss re-trigger ambiguity (see `TASKS.md` → Bugs).
- Pin dependency versions in `requirements.txt`.
- Decide on a real deployment mechanism if this is meant to run
  automatically/in the background rather than as a manually-launched
  foreground script (see `DEPLOYMENT.md`).

## Long-term ideas (speculative — not found anywhere in the repo, listed
only as plausible directions given the current single-feature scope)

- Cross-platform alarm support (currently macOS-only via `afplay`).
- Configurable webcam device index / multiple camera support.
- A snooze control (distinct from the current momentary ESC dismiss).
- Some form of usage summary/stats (e.g. "how many times today") — this
  would be new, currently there is zero persistence of any kind.
- If a real relationship with `phone-watchdog-web` is ever wanted (none
  exists today — see `ARCHITECTURE.md`), that would be a genuinely new
  integration, not an extension of anything already scaffolded.

## Out of scope (inferred from what's deliberately absent)

- No accounts/multi-user support — this is a single-user, single-machine
  local tool by construction (no auth code, no user model of any kind).
- No cloud sync / remote reporting — no network code exists at all
  beyond the model's own first-run download.
- No mobile app / companion app — nothing in the repo suggests this was
  ever planned; "the phone" is purely something the webcam looks *at*,
  not a client device the software talks to.

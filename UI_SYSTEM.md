# UI_SYSTEM.md

## This is a headless CLI script that produces one native GUI window — not a web app, and has no design system.

There is no HTML, no CSS, no browser-based UI, no component library, no
design tokens, and no theming system anywhere in this repo. What exists
instead:

## Console output

Exactly one line of console output exists in the entire codebase:

```python
print(f"Error: {payload}")   # monitor.py:154
```

This fires only when the webcam fails to open (`cap.isOpened() ==
False`). There is no startup banner, no "watchdog started" confirmation,
no per-detection log line, and no shutdown message. Running the script
successfully produces **zero terminal output** unless/until that one
error path is hit.

## The overlay window (the only real "UI")

`monitor.py`'s `Overlay` class (`monitor.py:86-134`) creates a single
native Tkinter window, shown only while a phone is considered "in view":

- **Type:** `tk.Toplevel`, `-fullscreen True`, `-topmost True` (always on
  top of every other window).
- **Background:** solid dark red, `bg="#8b0000"`.
- **Content:** two centered `tk.Label` widgets —
  1. Headline: `"PUT YOUR PHONE DOWN"`, Helvetica 64pt bold, white text.
  2. Subtext: `"Overlay closes automatically once the phone is out of
     frame.\nPress ESC to dismiss now."`, Helvetica 18pt, white text.
- **Interaction:** the only input handling is one key binding —
  `<Escape>` → `hide()`. There are no buttons, no mouse interaction, no
  other keyboard shortcuts.
- **Lifecycle:** created fresh each time `show()` is called (only if not
  already showing — idempotent), destroyed (`self.win.destroy()`) each
  time `hide()` is called. Not reused/hidden-and-reshown — a genuinely
  new `Toplevel` each time.
- **No accessibility features** were found (no explicit focus
  management beyond `focus_force()`, no screen-reader considerations, no
  colorblind-safe palette check) — appropriate for the project's current
  single-user, single-developer scope, but worth noting if this is ever
  shared with anyone else.
- **No responsive/layout system** — it's two `pack(expand=True)`'d
  labels on a fullscreen window; behavior at different screen
  resolutions was not tested this audit (would require actually
  launching the GUI).

## No other UI surface exists

No system tray icon, no menu bar item, no settings window, no web
dashboard, no CLI flags/arguments (`monitor.py` takes no command-line
arguments — `sys.argv` is never referenced). The entire user-facing
surface is: (a) the console (near-silent), and (b) the fullscreen overlay
described above.

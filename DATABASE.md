# DATABASE.md

## There is no database.

Verified by a full read of `monitor.py` and a repo-wide search: no
database driver is imported (`requirements.txt` lists only
`opencv-python` and `ultralytics`), no `sqlite3` import, no ORM, no
connection string, no `.db`/`.sqlite` file anywhere in the repository.

## Is there any local state file?

**No.** There is no file I/O anywhere in `monitor.py` for reading or
writing application state — no log file, no JSON/YAML state file, no
config file read at startup. All state is held purely in memory for the
lifetime of the process:

- `phone_since`, `clear_since`, `frame_count` — local variables inside
  `detector_loop()`, reset to their initial values every time the
  process (re)starts.
- `events` (`queue.Queue()`) — an in-memory, in-process queue; not
  persisted, not shared across processes.
- The `Overlay` instance's `win`/`alarm_stop`/`alarm_thread` — in-memory
  Tkinter/threading objects, again scoped to the single running process.

## Model weights caching (the one thing that touches disk)

`ultralytics.YOLO("yolov8n.pt")` will, on first use, download the
YOLOv8n model weights file if it isn't already present in Ultralytics'
own cache location. This is **not** application-level "database" state —
it's a third-party library's own model-weights cache, not something this
project's code reads, writes, or manages directly. No `.pt` file is
committed to this repository (confirmed via `find . -iname "*.pt"`), and
where exactly it gets cached on this machine was not inspected during
this audit (out of scope — it's `ultralytics`' own concern, not this
project's).

## If persistence is ever added

There is currently no schema, no migration tooling, and no established
pattern to follow. Any future persistence (e.g. a log of detection
events, or usage stats) would be new architecture — document the
decision in `DECISIONS.md` when/if it's introduced, rather than adding
it silently.

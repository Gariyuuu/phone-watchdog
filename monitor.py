#!/usr/bin/env python3
"""Webcam phone-use watchdog.

Watches the webcam for a phone in frame using YOLOv8n object detection.
If a phone is seen continuously for a few seconds, it plays an alarm and
throws up a fullscreen warning overlay until the phone is put down.

Run:  ./venv/bin/python monitor.py
Stop: Ctrl+C in the terminal, or press ESC on the overlay to dismiss it.
"""

import queue
import subprocess
import threading
import time
import tkinter as tk

import cv2
from ultralytics import YOLO

# --- Tunables ---
TRIGGER_SECONDS = 2.0       # phone must be visible this long before alarm fires
CLEAR_SECONDS = 3.0         # phone must be absent this long before overlay auto-closes
CONFIDENCE_THRESHOLD = 0.45
DETECT_EVERY_N_FRAMES = 3   # skip frames for performance
ALARM_SOUND = "/System/Library/Sounds/Sosumi.aiff"
ALARM_INTERVAL_SECONDS = 2.5

COCO_CELL_PHONE_CLASS_ID = 67

events = queue.Queue()


def detector_loop():
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        events.put(("error", "Could not open webcam."))
        return

    phone_since = None
    clear_since = None
    frame_count = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                time.sleep(0.1)
                continue

            frame_count += 1
            if frame_count % DETECT_EVERY_N_FRAMES != 0:
                continue

            results = model.predict(frame, verbose=False, conf=CONFIDENCE_THRESHOLD)
            phone_seen = any(
                int(box.cls[0]) == COCO_CELL_PHONE_CLASS_ID
                for box in results[0].boxes
            )

            now = time.monotonic()

            if phone_seen:
                clear_since = None
                if phone_since is None:
                    phone_since = now
                elif now - phone_since >= TRIGGER_SECONDS:
                    events.put(("phone_detected", None))
            else:
                phone_since = None
                if clear_since is None:
                    clear_since = now
                elif now - clear_since >= CLEAR_SECONDS:
                    events.put(("phone_cleared", None))
    finally:
        cap.release()


def play_alarm_loop(stop_flag):
    while not stop_flag.is_set():
        subprocess.run(["afplay", ALARM_SOUND])
        stop_flag.wait(ALARM_INTERVAL_SECONDS)


class Overlay:
    def __init__(self, root):
        self.root = root
        self.win = None
        self.alarm_stop = None
        self.alarm_thread = None

    def showing(self):
        return self.win is not None

    def show(self):
        if self.win is not None:
            return
        self.win = tk.Toplevel(self.root)
        self.win.attributes("-fullscreen", True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg="#8b0000")
        self.win.focus_force()

        tk.Label(
            self.win,
            text="PUT YOUR PHONE DOWN",
            font=("Helvetica", 64, "bold"),
            fg="white",
            bg="#8b0000",
        ).pack(expand=True)

        tk.Label(
            self.win,
            text="Overlay closes automatically once the phone is out of frame.\nPress ESC to dismiss now.",
            font=("Helvetica", 18),
            fg="white",
            bg="#8b0000",
        ).pack(pady=20)

        self.win.bind("<Escape>", lambda e: self.hide())

        self.alarm_stop = threading.Event()
        self.alarm_thread = threading.Thread(
            target=play_alarm_loop, args=(self.alarm_stop,), daemon=True
        )
        self.alarm_thread.start()

    def hide(self):
        if self.alarm_stop:
            self.alarm_stop.set()
        if self.win is not None:
            self.win.destroy()
            self.win = None


def main():
    root = tk.Tk()
    root.withdraw()

    overlay = Overlay(root)

    threading.Thread(target=detector_loop, daemon=True).start()

    def poll():
        try:
            while True:
                kind, payload = events.get_nowait()
                if kind == "phone_detected":
                    overlay.show()
                elif kind == "phone_cleared":
                    overlay.hide()
                elif kind == "error":
                    print(f"Error: {payload}")
                    root.quit()
        except queue.Empty:
            pass
        root.after(150, poll)

    root.after(150, poll)
    root.mainloop()


if __name__ == "__main__":
    main()

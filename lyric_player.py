import pygame
import time
import os
import tkinter as tk
from threading import Thread

FONT_SIZE = 32
ACTIVE_COLOR = "#00FFFF"
DIM_COLOR = "#555555"
DONE_COLOR = "#00FF00"
BG_COLOR = "#0d0d0d"
LOOKAHEAD = 5

def load_segments(lyric_file):
    segments = []
    with open(lyric_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("["):
                parts = line.split("] ", 1)
                times = parts[0].strip("[").split(" - ")
                text = parts[1].strip() if len(parts) > 1 else ""
                if text:
                    segments.append({
                        'start': float(times[0]),
                        'end': float(times[1]),
                        'text': text
                    })
    return segments

class LyricsWindow:
    def __init__(self, root, segments):
        self.root = root
        self.segments = segments
        self.current_index = 0

        root.title("♫ Lyrics Player")
        root.configure(bg=BG_COLOR)
        root.geometry("900x600")
        root.resizable(True, True)

        # Title bar
        title = tk.Label(root, text="♫ Now Playing", fg="#FFAA00",
                         bg=BG_COLOR, font=("Nirmala UI", 14, "bold"))
        title.pack(pady=(15, 5))

        tk.Label(root, text="─" * 60, fg="#333333", bg=BG_COLOR,
                 font=("Consolas", 10)).pack()

        # Scrollable lyrics frame
        self.canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        self.frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Create a label for every lyric line
        self.labels = []
        for seg in segments:
            lbl = tk.Label(
                self.frame,
                text=seg['text'],
                fg=DIM_COLOR,
                bg=BG_COLOR,
                font=("Nirmala UI", FONT_SIZE),  # Nirmala UI renders Sinhala perfectly
                anchor="w",
                justify="left",
                wraplength=860,
                pady=6
            )
            lbl.pack(fill="x", padx=10)
            self.labels.append(lbl)

        self.status_label = tk.Label(root, text="Starting...", fg="#FFAA00",
                                     bg=BG_COLOR, font=("Consolas", 11))
        self.status_label.pack(pady=8)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def highlight(self, index):
        """Make line at index bright, dim all others."""
        for i, lbl in enumerate(self.labels):
            if i == index:
                lbl.config(fg=ACTIVE_COLOR, font=("Nirmala UI", FONT_SIZE, "bold"))
            elif i < index:
                lbl.config(fg="#2a2a2a", font=("Nirmala UI", FONT_SIZE))  # Already sung
            else:
                lbl.config(fg=DIM_COLOR, font=("Nirmala UI", FONT_SIZE))  # Upcoming

        # Auto-scroll to keep active line centered
        self.root.update_idletasks()
        lbl_y = self.labels[index].winfo_y()
        canvas_h = self.canvas.winfo_height()
        self.canvas.yview_moveto(max(0, (lbl_y - canvas_h // 2)) /
                                  self.frame.winfo_height())

    def set_status(self, text, color="#FFAA00"):
        self.status_label.config(text=text, fg=color)

    def done(self):
        self.set_status("✓ Done!", DONE_COLOR)


def playback_thread(window, segments, audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    start_time = time.time()
    current_segment = 0

    try:
        while pygame.mixer.music.get_busy() and current_segment < len(segments):
            elapsed = time.time() - start_time
            seg = segments[current_segment]

            if elapsed >= seg['start']:
                window.root.after(0, window.highlight, current_segment)
                wait_until = start_time + seg['end']
                while time.time() < wait_until:
                    if not pygame.mixer.music.get_busy():
                        break
                    time.sleep(0.05)
                current_segment += 1

            time.sleep(0.02)

    except Exception as e:
        print(f"Playback error: {e}")

    window.root.after(0, window.done)


def play_lyrics(audio_path, lyric_file="lyrics.txt"):
    if not os.path.exists(lyric_file):
        print(f"Error: Could not find '{lyric_file}'.")
        return
    if not os.path.exists(audio_path):
        print(f"Error: Could not find '{audio_path}'.")
        return

    segments = load_segments(lyric_file)

    root = tk.Tk()
    window = LyricsWindow(root, segments)

    # Start playback in background thread
    t = Thread(target=playback_thread, args=(window, segments, audio_path), daemon=True)
    t.start()

    root.mainloop()


if __name__ == "__main__":
    audio_file = "nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3"
    play_lyrics(audio_file)
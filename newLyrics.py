import pygame
import time
import os
import sys
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich.progress import ProgressBar

console = Console()

def play_pro_lyrics(audio_path, lyric_file):
    # --- 1. File Check (Debug messages ekka) ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(script_dir, audio_path)
    lyric_file = os.path.join(script_dir, lyric_file)

    if not os.path.exists(audio_path) or not os.path.exists(lyric_file):
        console.print(f"[bold red]Error:[/bold red] Files hoyaganna ba! Folder eka check karanna.")
        return

    segments = []
    with open(lyric_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("["):
                try:
                    parts = line.split("] ", 1)
                    times = parts[0].strip("[").split(" - ")
                    text = parts[1].strip() if len(parts) > 1 else ""
                    if text:
                        segments.append({'start': float(times[0]), 'end': float(times[1]), 'text': text})
                except: continue

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    start_time = time.time()
    current_segment = 0

    # UI Refresh Function
    def make_ui(lyric_text, progress_pct=0, total_progress=0):
        # Karaoke highlight effect
        num_chars = int(len(lyric_text) * progress_pct)
        display_text = Text()
        display_text.append(lyric_text[:num_chars], style="bold cyan")
        display_text.append(lyric_text[num_chars:], style="bright_black")

        # Progress bar setup
        p_bar = ProgressBar(total=100, completed=total_progress * 100, width=40)

        # Main Layout
        layout = Layout()
        layout.split_column(
            Layout(name="upper", size=3),
            Layout(name="middle", size=7),
            Layout(name="lower", size=3)
        )

        layout["upper"].update(Align.center("[bold yellow]🎵 Suneera Sumanga - Nela Ganumata Nohaki Wuwada[/bold yellow]"))
        layout["middle"].update(Panel(Align.center(display_text, vertical="middle"), border_style="blue", padding=(1, 2)))
        layout["lower"].update(Align.center(p_bar))

        return layout

    # Live Display
    with Live(make_ui("--- Starting ---"), console=console, screen=True, refresh_per_second=20) as live:
        try:
            while pygame.mixer.music.get_busy() or current_segment < len(segments):
                elapsed = time.time() - start_time
                total_duration = pygame.mixer.Sound(audio_path).get_length()
                song_progress = min(elapsed / total_duration, 1.0)

                if current_segment < len(segments):
                    segment = segments[current_segment]
                    if elapsed >= segment['start']:
                        duration = segment['end'] - segment['start']
                        line_elapsed = elapsed - segment['start']
                        line_pct = min(line_elapsed / (duration * 0.95), 1.0)

                        live.update(make_ui(segment['text'], line_pct, song_progress))

                        if elapsed > segment['end']:
                            current_segment += 1
                    else:
                        live.update(make_ui("... 🎸 Instrumental 🎸 ...", 0, song_progress))

                time.sleep(0.02)
        except KeyboardInterrupt:
            pygame.mixer.music.stop()

if __name__ == "__main__":
    audio = "nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3"
    lyrics = "lyrics.txt"
    play_pro_lyrics(audio, lyrics)
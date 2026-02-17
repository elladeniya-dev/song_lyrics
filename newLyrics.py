import pygame
import time
import os
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

def play_lyrics(audio_path, lyric_file):
    # --- 1. File check kireema ---
    if not os.path.exists(audio_path):
        console.print(f"[bold red]Error:[/bold red] Audio file eka ne: {audio_path}")
        return
    if not os.path.exists(lyric_file):
        console.print(f"[bold red]Error:[/bold red] Lyrics file eka ne: {lyric_file}")
        return

    segments = []
    # --- 2. Lyrics load kireema ---
    with open(lyric_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("["):
                parts = line.split("] ", 1)
                times = parts[0].strip("[").split(" - ")
                text = parts[1].strip() if len(parts) > 1 else ""
                if text:
                    segments.append({'start': float(times[0]), 'end': float(times[1]), 'text': text})

    console.print(f"[green]Found {len(segments)} lyric segments![/green]")

    # --- 3. Playback patan ganna welawa ---
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    start_time = time.time()
    current_segment = 0

    console.print("[yellow]Starting playback... (Press Ctrl+C to stop)[/yellow]\n")

    try:
        while pygame.mixer.music.get_busy() and current_segment < len(segments):
            elapsed = time.time() - start_time
            segment = segments[current_segment]

            if elapsed >= segment['start']:
                # IntelliJ terminal eke lassanata panel ekaka lyrics pennanawa
                console.print(Panel(f"[bold cyan]{segment['text']}[/bold cyan]", border_style="blue"))
                current_segment += 1

            time.sleep(0.05)
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        console.print("\n[bold red]Stopped by user.[/bold red]")

if __name__ == "__main__":
    # Me file names ube folder eke thiyena ewa ekka check karanna
    audio = "nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3"
    lyrics = "lyrics.txt"

    play_lyrics(audio, lyrics)
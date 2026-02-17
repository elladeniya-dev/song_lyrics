import pygame
import time
import os
import sys
from rich.console import Console
from rich.live import Live
from rich.text import Text

# IntelliJ එකේ colors බලෙන්ම පෙන්වන්න
console = Console(force_terminal=True, color_system="truecolor")

def play_pro_lyrics(audio_file, lyric_file):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(base_dir, audio_file)
    lyric_path = os.path.join(base_dir, lyric_file)

    if not os.path.exists(audio_path) or not os.path.exists(lyric_path):
        console.print("[bold red]Files missing! Check paths.[/bold red]")
        return

    segments = []
    with open(lyric_path, "r", encoding="utf-8") as f:
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

    console.print(f"\n[bold yellow]🎵 Playing: {audio_file}[/bold yellow]\n")

    try:
        # 'Live' loop එක පාවිච්චි කරනවා smooth animation එකට
        with Live(Text("..."), console=console, refresh_per_second=30) as live:
            while pygame.mixer.music.get_busy() or current_segment < len(segments):
                # සින්දුව ප්ලේ වුණ වෙලාව (Current song time)
                elapsed = time.time() - start_time

                if current_segment < len(segments):
                    seg = segments[current_segment]

                    if elapsed >= seg['start']:
                        # --- Smooth Typing Logic ---
                        duration = seg['end'] - seg['start']
                        line_elapsed = elapsed - seg['start']

                        # සින්දුවේ වෙලාවට අනුව ප්‍රගතිය (0.0 to 1.0)
                        progress = min(line_elapsed / (duration * 0.95), 1.0)

                        # පෙන්විය යුතු අකුරු ගණන
                        num_chars = int(len(seg['text']) * progress)

                        # Styled text එක හදනවා (කියන ටික cyan, ඉතුරු ටික gray)
                        display_text = Text()
                        display_text.append(seg['text'][:num_chars], style="bold cyan")
                        display_text.append(seg['text'][num_chars:], style="bright_black")

                        live.update(display_text)

                        # පේළිය ඉවර නම් ඊළඟ එකට යනවා
                        if elapsed >= seg['end']:
                            current_segment += 1
                    else:
                        live.update(Text("... Instrumental ...", style="dim"))

                time.sleep(0.01) # CPU එකට පොඩි විවේකයක්

    except KeyboardInterrupt:
        pygame.mixer.music.stop()

if __name__ == "__main__":
    play_pro_lyrics("nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3", "lyrics.txt")
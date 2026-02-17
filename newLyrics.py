import pygame
import time
import os
import sys
from rich.console import Console
from rich.text import Text

# IntelliJ terminal එකේ colors force කරන්න force_terminal=True දානවා
console = Console(force_terminal=True, color_system="truecolor")

def play_pro_lyrics(audio_file, lyric_file):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(base_dir, audio_file)
    lyric_path = os.path.join(base_dir, lyric_file)

    if not os.path.exists(audio_path) or not os.path.exists(lyric_path):
        console.print("[bold red]Files missing![/bold red]")
        return

    segments = []
    with open(lyric_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("["):
                parts = line.split("] ", 1)
                times = parts[0].strip("[").split(" - ")
                text = parts[1].strip() if len(parts) > 1 else ""
                if text:
                    segments.append({'start': float(times[0]), 'end': float(times[1]), 'text': text})

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    start_time = time.time()
    current_segment = 0

    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(f"[bold yellow]🎵 Playing: {audio_file}[/bold yellow]\n" + "-"*40)

    try:
        while pygame.mixer.music.get_busy() and current_segment < len(segments):
            elapsed = time.time() - start_time
            segment = segments[current_segment]

            if elapsed >= segment['start']:
                text_val = segment['text']
                duration = segment['end'] - segment['start']
                line_start_time = time.time()

                last_num_chars = -1 # පේළියම එකපාර වැටෙන එක නවත්තන්න

                while True:
                    line_elapsed = time.time() - line_start_time
                    if line_elapsed >= duration:
                        # පේළිය ඉවර වුණාම සම්පූර්ණ පේළිය lock කරනවා
                        sys.stdout.write('\r' + " " * 120 + '\r')
                        console.print(f"[bold cyan]{text_val}[/bold cyan]")
                        break

                    # Typing progress එක calculate කරනවා
                    progress = min(line_elapsed / (duration * 0.9), 1.0)
                    num_chars = int(len(text_val) * progress)

                    # අකුරු ප්‍රමාණය වෙනස් වුණොත් විතරක් රෙන්ඩර් කරනවා (CPU load එක අඩු කරන්න)
                    if num_chars != last_num_chars:
                        # Styled text එකක් හදනවා color පේන්න
                        display_text = Text()
                        display_text.append(text_val[:num_chars], style="bold cyan")
                        display_text.append(text_val[num_chars:], style="bright_black") # ඉතුරු ටික gray

                        # \r පාවිච්චි කරලා පේළිය උඩම ලියනවා
                        sys.stdout.write('\r')
                        console.print(display_text, end="")
                        sys.stdout.flush()
                        last_num_chars = num_chars

                    time.sleep(0.02) # Animation එක smooth වෙන්න පොඩි delay එකක්

                current_segment += 1
            time.sleep(0.01)

    except KeyboardInterrupt:
        pygame.mixer.music.stop()

if __name__ == "__main__":
    play_pro_lyrics("nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3", "lyrics.txt")
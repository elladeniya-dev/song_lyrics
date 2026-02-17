import pygame
import time
import os
import sys
from colorama import init, Fore, Style
import shutil

init()

def clear_line():
    """Cross-platform line clear using terminal width"""
    width = shutil.get_terminal_size().columns
    sys.stdout.write('\r' + ' ' * (width - 1) + '\r')
    sys.stdout.flush()

def play_lyrics(audio_path, lyric_file="lyrics.txt"):
    segments = []

    if not os.path.exists(lyric_file):
        print(Fore.RED + f"Error: Could not find '{lyric_file}'." + Style.RESET_ALL)
        return

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

    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + "\nStarting playback...\n" + "="*40 + "\n" + Style.RESET_ALL)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    start_time = time.time()
    current_segment = 0
    last_printed_chars = 0  # Track how many chars were printed last frame

    try:
        while pygame.mixer.music.get_busy() and current_segment < len(segments):
            elapsed_time = time.time() - start_time
            segment = segments[current_segment]

            if elapsed_time >= segment['start']:
                text = segment['text']
                duration = segment['end'] - segment['start']
                line_start = time.time()
                last_printed_chars = 0

                while True:
                    current_elapsed = time.time() - line_start

                    if current_elapsed >= (duration * 0.85):
                        # ✅ Clear the whole line first, then print full text
                        clear_line()
                        sys.stdout.write(Fore.CYAN + text + Style.RESET_ALL)
                        sys.stdout.flush()
                        print()  # Move to next line
                        last_printed_chars = 0
                        break

                    progress = current_elapsed / (duration * 0.85)
                    chars_to_show = int(len(text) * progress)

                    # Only redraw if char count changed (avoids flicker)
                    if chars_to_show != last_printed_chars:
                        # ✅ Clear entire line before rewriting (fixes Sinhala overlap)
                        clear_line()
                        sys.stdout.write(Fore.CYAN + text[:chars_to_show] + Style.RESET_ALL)
                        sys.stdout.flush()
                        last_printed_chars = chars_to_show

                    time.sleep(0.01)

                current_segment += 1

            time.sleep(0.01)

    except KeyboardInterrupt:
        print(Fore.RED + "\nPlayback stopped by user." + Style.RESET_ALL)
        pygame.mixer.music.stop()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

    print(Fore.GREEN + "\n" + "="*40 + "\nDone!" + Style.RESET_ALL)

if __name__ == "__main__":
    audio_file = "nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3"

    if os.path.exists(audio_file):
        play_lyrics(audio_file)
    else:
        print(Fore.RED + f"Error: Could not find '{audio_file}'." + Style.RESET_ALL)
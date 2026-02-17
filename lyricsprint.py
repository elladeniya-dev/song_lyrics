import pygame
import time
import os
import sys

# cspell:ignore ganumata nohaki wuwada suneera sumanga

def play_pro_lyrics(audio_file, lyric_file):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(base_dir, audio_file)
    lyric_path = os.path.join(base_dir, lyric_file)

    if not os.path.exists(audio_path) or not os.path.exists(lyric_path):
        print(f"Files missing! Make sure '{audio_file}' and '{lyric_file}' are in the same folder.")
        return

    segments = []
    with open(lyric_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("["):
                try:
                    # Parses format: [113.50 - 120.50] Lyric text 🌸
                    parts = line.split("]", 1)
                    times = parts[0].strip("[").split(" - ")

                    start_time = float(times[0])
                    end_time = float(times[1])
                    text = parts[1].strip() if len(parts) > 1 else ""

                    segments.append({
                        'start': start_time,
                        'end': end_time,
                        'text': text
                    })
                except (ValueError, IndexError):
                    continue

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    current_segment = 0
    print(f"\n🎵 Playing: {audio_file}\n")

    try:
        last_rendered = ""
        # Keep running while music is playing and segments are left
        while pygame.mixer.music.get_busy() and current_segment < len(segments):

            # get_pos() returns milliseconds, divide by 1000 for exact seconds
            elapsed = pygame.mixer.music.get_pos() / 1000.0

            seg = segments[current_segment]

            if elapsed >= seg['start'] and elapsed <= seg['end']:
                # --- Smooth Typing Logic ---
                duration = seg['end'] - seg['start']
                line_elapsed = elapsed - seg['start']

                # Progress percentage (0.0 to 1.0)
                progress = min(line_elapsed / duration, 1.0)

                # Number of characters to display based on progress
                num_chars = int(len(seg['text']) * progress)
                display_text = seg['text'][:num_chars]

                # Only redraw if the text has changed
                if display_text != last_rendered:
                    # Pad with spaces (ljust) to clear leftover characters
                    sys.stdout.write("\r" + display_text.ljust(60))
                    sys.stdout.flush()
                    last_rendered = display_text

            elif elapsed > seg['end']:
                # Segment ended: print the final full line and move to the next
                sys.stdout.write("\r" + seg['text'].ljust(60) + "\n")
                sys.stdout.flush()
                current_segment += 1
                last_rendered = ""

            elif elapsed < seg['start']:
                # Waiting for the next segment (Instrumental/Pause)
                waiting_text = "🎶 ..."
                if last_rendered != waiting_text:
                    sys.stdout.write("\r" + waiting_text.ljust(60))
                    sys.stdout.flush()
                    last_rendered = waiting_text

            time.sleep(0.05) # Keeps the loop from eating up CPU

    except KeyboardInterrupt:
        print("\n\n⏹️ Playback stopped by user.")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        print("\nDone!")

if __name__ == "__main__":
    play_pro_lyrics("nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3", "lyrics.txt")
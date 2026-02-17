import pygame
import time
import os
import sys

def play_pro_lyrics(audio_file, lyric_file, time_offset=0.0):
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

    # Pygame get_pos() wenuwata OS time eka use karanawa hariyatama accurate wenna
    start_time_real = time.time()
    current_segment = 0

    print(f"\n🎵 Playing: {audio_file}\n")

    try:
        last_rendered = ""
        while pygame.mixer.music.get_busy() and current_segment < len(segments):

            # Hari second eka calculate karanawa (offset ekath ekka)
            elapsed = (time.time() - start_time_real) + time_offset

            seg = segments[current_segment]

            # 1. Thama lyric eka patan ganna welawa awe naththam (Instrumental/Waiting)
            if elapsed < seg['start']:
                waiting_text = "🎶 ..."
                if last_rendered != waiting_text:
                    sys.stdout.write("\r" + waiting_text.ljust(80))
                    sys.stdout.flush()
                    last_rendered = waiting_text

            # 2. Lyric eka play wena welawa (Typing effect)
            elif seg['start'] <= elapsed <= seg['end']:
                duration = seg['end'] - seg['start']
                line_elapsed = elapsed - seg['start']

                if "Instrumental" in seg['text'] or "Intro" in seg['text']:
                    display_text = seg['text']
                else:
                    # Typing speed eka adjust kara hariyatama song eka ekka yanna
                    progress = min(line_elapsed / (duration * 0.8), 1.0)
                    num_chars = int(len(seg['text']) * progress)
                    display_text = seg['text'][:num_chars]

                if display_text != last_rendered:
                    sys.stdout.write("\r" + display_text.ljust(80))
                    sys.stdout.flush()
                    last_rendered = display_text

            # 3. Lyric eka iwara unama next line ekata yana eka
            elif elapsed > seg['end']:
                sys.stdout.write("\r" + seg['text'].ljust(80) + "\n")
                sys.stdout.flush()
                current_segment += 1
                last_rendered = ""

            time.sleep(0.02) # Very small sleep to make it super smooth without lagging

    except KeyboardInterrupt:
        print("\n\n⏹️ Playback stopped by user.")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        print("\nDone!")

if __name__ == "__main__":
    # Lyrics issarahin yanawanam: time_offset eka adu karanna (e.g., -1.5)
    # Lyrics passen yanawanam: time_offset eka wadi karanna (e.g., 2.0)
    play_pro_lyrics("nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3", "lyrics.txt", time_offset=0.0)
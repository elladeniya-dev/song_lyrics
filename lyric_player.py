import whisper
import pygame
import time
import os

def generate_and_play_lyrics(audio_path, output_lyric_file="lyrics.txt"):
    print("Loading Whisper AI model... (This might take a moment)")
    # 'base' is fast and decent. Use 'small' or 'medium' for better accuracy if you have a good GPU.
    # Upgraded to 'medium' for better Sinhala accuracy
    model = whisper.load_model("medium")

    print(f"Transcribing '{audio_path}'... Sit tight!")
    # Transcribe the audio. This generates the text and the timestamps.
    result = model.transcribe(audio_path, language="si")
    segments = result['segments']

    # Step 1: Save the lyrics to a file
    print(f"Saving lyrics and timestamps to {output_lyric_file}...")
    with open(output_lyric_file, "w", encoding="utf-8") as f:
        for segment in segments:
            # Format: [Start_Time - End_Time] Lyric text
            f.write(f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text'].strip()}\n")

    # Step 2: Play the audio and sync the lyrics to the terminal
    print("\nStarting playback...\n" + "-"*30)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    start_time = time.time()
    current_segment = 0

    try:
        # Loop while the music is playing and we still have lyrics to show
        while pygame.mixer.music.get_busy() and current_segment < len(segments):
            # Calculate how much time has passed since the song started
            elapsed_time = time.time() - start_time
            segment = segments[current_segment]

            # If the elapsed time matches or passes the start time of the next lyric, print it
            if elapsed_time >= segment['start']:
                print(segment['text'].strip())
                current_segment += 1

            # Sleep briefly to prevent the loop from maxing out your CPU
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\nPlayback stopped by user.")
        pygame.mixer.music.stop()

    # Wait for the song to finish if the lyrics end early
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    print("\n" + "-"*30 + "\nDone!")

if __name__ == "__main__":
    # ---> REPLACE THIS WITH YOUR SONG'S FILENAME <---
    audio_file = "nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3"
    
    if os.path.exists(audio_file):
        generate_and_play_lyrics(audio_file)
    else:
        print(f"Error: Could not find the file '{audio_file}'. Please check the path and try again.")
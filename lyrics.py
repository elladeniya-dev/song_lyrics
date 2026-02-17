import pygame
import time
import os

# Initialize Pygame
pygame.init()

def play_pygame_karaoke(audio_path, lyric_file="lyrics.txt"):
    # Create the window (Karaoke Screen)
    screen = pygame.display.set_mode((1000, 400))
    pygame.display.set_caption("Sinhala Lyrics Player")
    
    # Load Sinhala Font (Windows built-in)
    try:
        font = pygame.font.SysFont("Nirmala UI", 55)
    except:
        font = pygame.font.SysFont("Iskoola Pota", 55)

    segments = []
    # Load lyrics file
    if os.path.exists(lyric_file):
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

    # Start audio playback
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    
    start_time = time.time()
    current_segment = 0
    running = True

    while running:
        screen.fill((15, 15, 15)) # Dark background
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        elapsed = time.time() - start_time
        
        if current_segment < len(segments):
            seg = segments[current_segment]
            
            # Line eka pennanna patan ganna welawa
            if elapsed >= seg['start']:
                duration = seg['end'] - seg['start']
                # Calculate progress based on time
                progress = min((elapsed - seg['start']) / (duration * 0.9), 1.0)
                
                # Typing effect logic
                # We render the whole line but only show a portion to keep spacing perfect
                num_chars = int(len(seg['text']) * progress)
                display_text = seg['text'][:num_chars]
                
                # Draw the text to screen
                text_surface = font.render(display_text, True, (0, 255, 255)) # Cyan color
                text_rect = text_surface.get_rect(center=(500, 200))
                screen.blit(text_surface, text_rect)
                
                # Move to next line after duration ends
                if elapsed > seg['end']:
                    current_segment += 1

        pygame.display.flip()
        time.sleep(0.01)

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    audio_file = "nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3"
    if os.path.exists(audio_file):
        play_pygame_karaoke(audio_file)
    else:
        print("Error: Audio file not found!")
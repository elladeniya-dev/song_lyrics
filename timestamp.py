import whisper
import warnings

# cspell:ignore ganumata nohaki wuwada suneera sumanga

# Hide unnecessary warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def get_vocal_timestamps(audio_file):
    print("⏳ AI model eka load wenawa. Poddak inna...")
    # 'base' or 'small' model eka use karanna puluwan. Small eka wada accurate.
    model = whisper.load_model("small") 
    
    print(f"🎵 '{audio_file}' scan karanawa...")
    # Language eka Sinhala ('si') widiyata denawa
    result = model.transcribe(audio_file, language="si")
    
    print("\n✅ Vocals detect karapu welawal:\n")
    for segment in result["segments"]:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        
        # Format eka lassanata print karanawa
        print(f"[{start:.2f} - {end:.2f}] (Detected Vocals)")

if __name__ == "__main__":
    get_vocal_timestamps("nela-ganumata-nohaki-wuwada-suneera-sumanga.mp3")
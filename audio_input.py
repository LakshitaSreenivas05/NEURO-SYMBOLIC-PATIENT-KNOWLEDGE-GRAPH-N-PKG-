import whisper
import os

model = whisper.load_model("base")

def transcribe_audio(audio_file_path):
    print(f"  -> Transcribing audio: {audio_file_path}")
    
    # Check file exists
    if not os.path.exists(audio_file_path):
        print(f"   File not found: {audio_file_path}")
        return None
    
    # Transcribe
    result = model.transcribe(audio_file_path)
    transcript = result["text"]
    
    print(f"   Transcription complete!")
    print(f"  -> Text: {transcript[:100]}...")  # Show first 100 chars
    
    return transcript
import sys

try:
    import whisper
except Exception as e:
    print(f"Step 2: Whisper FAILED ❌ - {e}")
    sys.exit()

try:
    import sounddevice as sd
except Exception as e:
    print(f"Step 3: sounddevice FAILED ❌ - {e}")
    sys.exit()

try:
    import numpy as np
    import scipy.io.wavfile as wav
    import tempfile
    import os
except Exception as e:
    print(f"Step 4: Import FAILED ❌ - {e}")
    sys.exit()

try:
    model = whisper.load_model("base")
except Exception as e:
    print(f"Step 6: Model load FAILED ❌ - {e}")
    sys.exit()

def record_audio(duration=10, sample_rate=16000):
    print(f"\n🎤 Recording for {duration} seconds...")
    print("Speak now!")
    audio_data = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='float32'
    )
    sd.wait()
    print("✅ Recording complete!")
    return audio_data, sample_rate

def transcribe_live(duration=10):
    try:
        audio_data, sample_rate = record_audio(duration)
        temp_file = tempfile.mktemp(suffix=".wav")
        wav.write(temp_file, sample_rate, audio_data)
        print("\n→ Transcribing...")
        result = model.transcribe(temp_file)
        transcript = result["text"]
        os.remove(temp_file)
        print(transcript)
        return transcript
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Wrap the test execution in this if statement:
if __name__ == "__main__":
    try:
        duration = int(input("Enter seconds to record (recommended 15-30): "))
        transcribe_live(duration=duration)
    except Exception as e:
        print(f"❌ Final error: {e}")
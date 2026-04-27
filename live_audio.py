import sys
import winsound

try:
    import whisper
except Exception as e:
    print(f"Step 2: Whisper FAILED  - {e}")
    sys.exit()

try:
    import sounddevice as sd
except Exception as e:
    print(f"Step 3: sounddevice FAILED  - {e}")
    sys.exit()

try:
    import numpy as np
    import scipy.io.wavfile as wav
    import tempfile
    import os
except Exception as e:
    print(f"Step 4: Import FAILED  - {e}")
    sys.exit()

try:
    model = whisper.load_model("base")
except Exception as e:
    print(f"Step 6: Model load FAILED  - {e}")
    sys.exit()

def record_audio(sample_rate=16000, silence_threshold=0.01, silence_duration=5.0):
    # Start beep
    winsound.Beep(1000, 300)
    print(f"\n Listening... (will stop after {silence_duration}s of silence)")
    
    recorded_chunks = []
    silent_chunks = 0
    chunk_size = 1024
    max_silent_chunks = int((silence_duration * sample_rate) / chunk_size)
    
    with sd.InputStream(samplerate=sample_rate, channels=1, blocksize=chunk_size) as stream:
        while True:
            data, overflowed = stream.read(chunk_size)
            recorded_chunks.append(data.copy())
            
            # Check volume (RMS)
            rms = np.sqrt(np.mean(data**2))
            
            if rms < silence_threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0
                
            # Stop if silence threshold met
            if silent_chunks > max_silent_chunks:
                break
            
            # Safety break after 60 seconds to prevent infinite recording
            if len(recorded_chunks) * chunk_size > sample_rate * 60:
                break
    # End beep
    winsound.Beep(800, 300)
    print("Silence detected. Recording complete!")
    
    audio_data = np.concatenate(recorded_chunks, axis=0)
    return audio_data, sample_rate

def transcribe_live():
    try:
        audio_data, sample_rate = record_audio()
        temp_file = tempfile.mktemp(suffix=".wav")
        wav.write(temp_file, sample_rate, audio_data)
        print("\n-> Transcribing...")
        result = model.transcribe(temp_file)
        transcript = result["text"]
        os.remove(temp_file)
        print(transcript)
        return transcript
    except Exception as e:
        print(f" Error: {e}")
        return None

# Wrap the test execution in this if statement:
if __name__ == "__main__":
    try:
        duration = int(input("Enter seconds to record (recommended 15-30): "))
        transcribe_live(duration=duration)
    except Exception as e:
        print(f" Final error: {e}")
        
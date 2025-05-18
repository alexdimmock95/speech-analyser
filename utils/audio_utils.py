# Load and inspect the audio file
def load_audio(file, target_sr=16000):
    import os
    import wave
    import numpy as np
    import librosa
    import soundfile as sf
    # Ensure file exists
    if not os.path.exists(file):
        raise FileNotFoundError(f"File '{file}' not found.")
    
    # Load the audio file
    with wave.open(file, 'rb') as wav_file:
        # Get audio file properties
        channels = wav_file.getnchannels()
        rate = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())
        # Convert byte data to numpy array
        # Assuming the audio is 16000Hz mono
        audio = np.frombuffer(frames, dtype=np.int16)
        duration = len(audio) / rate
        print(f"Name: '{file}', Channels: {channels}, Sample Rate: {rate}, Duration: {duration:.2f} seconds.")

    # Check if resampling to 16000Hz is necessary
    if rate != target_sr:
        original_rate = rate
        # Load the audio file
        audio, rate = librosa.load(file, sr=target_sr, mono=True)
        print(f"Resampled '{file}' from {original_rate}Hz to {target_sr}Hz")
        # Save the resampled audio to a new file
        output_filename = os.path.join(os.path.dirname(file), "resampled_" + os.path.basename(file))
        sf.write(output_filename, audio, target_sr)
        print(f"Resampled audio saved as '{output_filename}'")
        return audio, rate, output_filename
    else:
        audio, rate = librosa.load(file, sr=rate, mono=True)
        print(f"No resampling needed, loaded audio at {rate}Hz.")
        return audio, rate, file
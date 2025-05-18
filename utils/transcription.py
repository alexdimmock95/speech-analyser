# Transcribe the audio using Whisper

def transcribe_audio(filename, audio):
    import whisper
    # Load the Whisper model
    model = whisper.load_model("tiny")
    # Transcribe the audio
    result = model.transcribe(audio, language="en")
    # Print the transcription
    print(f"Transcribed message: {result['text']}")
    # Save the transcription to a file
    saved_filename = filename.split(".")[0]
    with open(f"{saved_filename}.txt", "w") as f:
        f.write(result["text"])
    # Print the segments with timestamps
    for segment in result["segments"]:
        # Print the start and end times of each segment
        print(f"[{segment['start']:.2f} → {segment['end']:.2f}] {segment['text']}")
    return result
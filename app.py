import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import streamlit as st
import subprocess
import tempfile
import uuid
from utils.audio_utils import load_audio
from utils.transcription import transcribe_audio
from utils.analysis import analyse_audio
from utils.textgrid import detect_hesitation

def check_conda_env_exists(env_name="mfa_env"):
    try:
        result = subprocess.run(["conda", "env", "list"], capture_output=True, text=True, check=True)
        return any(env_name in line for line in result.stdout.splitlines())
    except Exception:
        return False

MFA_AVAILABLE = check_conda_env_exists("mfa_env")

st.set_page_config(page_title="Speech Analyser", layout="centered")

st.title("🔊 Speech Analyser")

# --- Session State Init ---
if "used_audio_path" not in st.session_state:
    st.session_state["used_audio_path"] = None

st.subheader("📤 Upload Your Audio")

# --- Upload Audio ---
uploaded_file = st.file_uploader("Choose an audio file", type=["wav"])

if uploaded_file is not None:
    def save_audio_to_temp_folder(audio_bytes):
        unique_id = str(uuid.uuid4())
        audio_dir = os.path.join("/tmp", f"mfa_{unique_id}")
        os.makedirs(audio_dir, exist_ok=True)
        wav_path = os.path.join(audio_dir, "audio.wav")
        with open(wav_path, "wb") as f:
            f.write(audio_bytes)
        return wav_path, audio_dir

    # Save uploaded audio to a unique temp file
    audio_bytes = uploaded_file.read()
    tmp_path, mfa_audio_dir = save_audio_to_temp_folder(audio_bytes)

    audio_data, sr, used_audio_path = load_audio(tmp_path, target_sr=16000)
    
    st.session_state["used_audio_path"] = used_audio_path
    st.session_state["mfa_audio_dir"] = mfa_audio_dir

    st.success("✅ Audio uploaded and saved")
    st.audio(tmp_path)

if (
    "used_audio_path" in st.session_state
    and st.session_state["used_audio_path"] is not None
):
    st.markdown("---")
    st.subheader("📝 Step 2: Transcribe Audio")

    if "transcription_result" not in st.session_state:
        st.session_state.transcription_result = None  # Initialize session state for transcription result

    if st.button("Transcribe"):
        with st.spinner("Transcribing... please wait ⏳"):
            result = transcribe_audio(used_audio_path, audio_data)
            st.session_state.transcription_result = result  # Save result to session state
            st.success("✅ Transcription complete!")

    if st.session_state.transcription_result:
        st.text_area("Transcript", st.session_state.transcription_result["text"], height=130)

        st.markdown("---")
        st.subheader("🔬 Step 3: Audio Analysis")

        if "analysis_result" not in st.session_state:
            st.session_state.analysis_result = None  # Initialize session state for analysis result

        if st.button("Analyse"):
            with st.spinner("Analyzing... please wait ⏳"):
                analysis_result = analyse_audio(used_audio_path)
                st.session_state.analysis_result = analysis_result
                st.success("✅ Analysis complete!")
        
        if st.session_state.analysis_result:
            
            # Extract intensity and pitch data for plotting
            pitch = st.session_state.analysis_result['pitch']
            intensity = st.session_state.analysis_result['intensity']
            jitter = st.session_state.analysis_result['jitter']
            shimmer = st.session_state.analysis_result['shimmer']
            
            st.subheader("📊 Acoustic Analysis Results")

            # Define xticks for both plots
            x_min = min(min(pitch["time"]), min(intensity["time"]))
            x_max = max(max(pitch["time"]), max(intensity["time"]))
            x_ticks = np.arange(np.floor(x_min), np.ceil(x_max) + 1, step=1)

            # Intensity
            st.subheader("🔉 Intensity")
            st.write(f"**Mean**: {intensity['mean']:.2f} dB")
            st.write(f"**Min**: {intensity['min']:.2f} dB")
            st.write(f"**Max**: {intensity['max']:.2f} dB")
            st.write(f"**Label**: {intensity['label']}")

            # Plot intensity
            st.markdown("#### Intensity Plot")
            plt.figure(figsize=(10, 4))
            plt.plot(intensity["time"], intensity["values"], label="Intensity (dB)", color="blue")
            plt.xticks(x_ticks)
            plt.xlabel("Time (s)")
            plt.ylabel("Intensity (dB)")
            plt.title("Intensity Over Time")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(plt)
            plt.clf()

            st.info("🔊 *Intensity refers to the loudness of your voice. Higher intensity can signal enthusiasm, confidence, or urgency, while lower intensity may suggest calmness, hesitation, or insecurity.*"
            "\n\n"
            "*Consistent vocal intensity is often linked to assertiveness and engagement.*"
            "\n\n"
            "*Normal conversational speech typically ranges between 60 and 70 decibels (dB), with shouting exceeding 85 dB and whispering falling below 30 dB.*")

            # Shimmer
            st.subheader("✨ Shimmer")
            
            st.write(f"**Shimmer**: {shimmer['value']:.4f}")
            st.write(f"**Label**: {shimmer['label']}")

            st.info("🌫️ *Shimmer measures small, rapid fluctuations in loudness between vocal cycles. High shimmer may indicate breathiness, fatigue, or reduced vocal control.*"
            "\n\n"
            "*Shimmer is typically very low in healthy, clear voices — but can increase with stress, dehydration, or vocal fatigue.*")

            # Pitch
            st.subheader("🎵 Pitch")
            st.write(f"**Mean**: {pitch['mean']:.2f} Hz")
            st.write(f"**Min**: {pitch['min']:.2f} Hz")
            st.write(f"**Max**: {pitch['max']:.2f} Hz")
            st.write(f"**Range**: {pitch['range']:.2f} Hz")
            st.write(f"**Standard Deviation**: {pitch['std']:.2f}")

            # Plot pitch
            st.markdown("#### Pitch Plot")
            plt.figure(figsize=(10, 4))
            plt.plot(pitch["time"], pitch["values"], label="Pitch (Hz)", color="blue")
            plt.xticks(x_ticks)
            plt.xlabel("Time (s)")
            plt.ylabel("Pitch (Hz)")
            plt.title("Pitch Over Time")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(plt)
            plt.clf()

            st.info("💡 *Pitch is the perceived frequency of your voice. A higher pitch may indicate excitement or nervousness, while a lower pitch may suggest calmness or authority.*" \
            "\n\n" \
            "*A stable pitch is often associated with confidence and clarity in speech.*"
            "\n\n" \
            "*Female pitch ranges on average between 165Hz and 255Hz, while the male pitch ranges on average between 85Hz and 180Hz.*")

            # Jitter
            st.subheader("🌬️ Jitter")
            st.write(f"**Jitter**: {jitter['value']:.4f}")
            st.write(f"**Label**: {jitter['label']}")

            st.info("🎙️ *Jitter measures tiny, rapid variations in the pitch of your voice from cycle to cycle. High jitter can suggest vocal strain, tension, or instability.*"
            "\n\n"
            "*Jitter is typically very low in healthy, clear voices — but can increase with stress, dehydration, or vocal fatigue.*")

            if MFA_AVAILABLE:
                st.markdown("---")
                st.subheader("🗣️ Step 4: MFA Alignment")

                if st.button("Run MFA Alignment"):
                    with st.spinner("Running MFA... please wait ⏳"):
                        mfa_audio_dir = st.session_state["mfa_audio_dir"]
                        # Save the transcription result to the MFA audio directory
                        audio_filename = os.path.splitext(os.path.basename(used_audio_path))[0] # Get the filename without extension
                        transcription_path = os.path.join(mfa_audio_dir, f"{audio_filename}.txt") # Path for transcription file using the same filename as the audio
                        with open(transcription_path, "w") as f:
                            f.write(st.session_state.transcription_result["text"])
                        src_path = used_audio_path
                        dst_path = os.path.join(mfa_audio_dir, os.path.basename(used_audio_path))
                        if os.path.abspath(src_path) != os.path.abspath(dst_path):
                            shutil.copy2(src_path, dst_path) # Copy the audio file to the MFA directory only if it is not already there

                        print(f"Wrote transcript to {transcription_path}")
                        print("Listing contents of mfa_audio_dir:")
                        print(os.listdir(mfa_audio_dir))

                        # 🔍 Full paths (optional, helps with misnaming or path issues)
                        for f_name in os.listdir(mfa_audio_dir):
                            print("Full path:", os.path.join(mfa_audio_dir, f_name))

                        print("📂 Absolute path to MFA dir:", os.path.abspath(mfa_audio_dir))

                        # Call the bash script or subprocess to run MFA
                        with tempfile.TemporaryDirectory() as temp_output_dir:
                            mfa_command = [
                                "bash", "run_mfa.sh", 
                                mfa_audio_dir,  # Directory with audio and transcription
                                temp_output_dir # Temporary directory for MFA output
                            ]
                            result = subprocess.run(mfa_command, capture_output=True, text=True)

                            if result.returncode == 0:
                                st.success("✅ MFA Alignment complete!")
                                # st.text_area("MFA Output", result.stdout, height=200)
                                # st.markdown("📂 Files created by MFA:")
                                # st.write(os.listdir(temp_output_dir))

                                # 👇 Look for the TextGrid file
                                textgrid_path = None
                                for file in os.listdir(temp_output_dir):
                                    if file.endswith(".TextGrid"):
                                        textgrid_path = os.path.join(temp_output_dir, file)
                                        break
                                
                                if textgrid_path:
                                    st.markdown("### 📊 Speech Fluency Analysis")

                                    fillers = {"uh", "um", "ah", "like", "you know", "i mean"}
                                    analysis, used_filler_words, long_pauses = detect_hesitation(textgrid_path, fillers)

                                    for line in analysis:
                                        st.markdown(f"- {line}")
                                    
                                    def show_filler_feedback(used_filler_words):
                                        if used_filler_words:
                                            st.markdown("#### 🤔 Hmm... Noticed a few filler words in your speech.")
                                            filler_strings = [
                                                f"🗯️ {i+1}. '{word}'"
                                                for i, word in enumerate(used_filler_words)
                                            ]
                                            st.text("\n".join(filler_strings))
                                            st.info("💬 *“Do those ‘um’s and ‘like’s happen when you’re reaching for ideas you haven’t fully rehearsed?”*")
                                    
                                    def show_long_pause_feedback(pause_data):
                                        if pause_data:  # pause_data could be list of timestamps or durations
                                            st.markdown("#### 🕰️ Long pauses detected")
                                            pause_strings = [
                                                f"⏸️ {i+1}. {pause['start']:.2f}s → {pause['end']:.2f}s ({pause['duration']:.2f}s)"
                                                for i, pause in enumerate(pause_data)
                                            ]
                                            st.text("\n".join(pause_strings))
                                            
                                            st.info("💬 *“Did you need a moment to gather your thoughts here, or was this an intentional pause for emphasis?”*")
                                    
                                    show_filler_feedback(used_filler_words)

                                    show_long_pause_feedback(long_pauses)
                                
                                else:
                                    st.warning("⚠️ No TextGrid file found.")

                            else:
                                st.error("❌ MFA Alignment failed. See error message below:")
                                st.text_area("MFA Error", result.stderr, height=200)

            else:
                st.markdown("---")
                st.subheader("🗣️ Step 4: MFA Alignment")
                st.info("⚠️ Montreal Forced Aligner (MFA) is not available in this environment. This is highly possible with Streamlit Cloud runs.Phoneme alignment features are disabled.")

else:
    st.info("Upload an audio file to continue.")
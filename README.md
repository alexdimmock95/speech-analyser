# 🗣️ Speech Analyser App

An interactive Streamlit app that analyses your recorded or uploaded speech for vocal fluency, filler words, long pauses, and acoustic clarity — using Montreal Forced Aligner, Praat-Parselmouth, and custom heuristics.

https://speech-analyser.streamlit.app/

---

## 🚀 Quickstart

```bash
# Clone the repo
git clone https://github.com/alexdimmock95/speech-analyser.git
cd speech-analyser

# Create and activate virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# ⚠️ Note: If you want to use the phoneme alignment feature,
# you must install Montreal Forced Aligner (MFA) in a separate environment.
# See instructions in the "MFA Setup" section below.

# Run the Streamlit app
streamlit run app.py
```
## 🛠️ Installation & Setup
Before running the Speech Analyser app, make sure you have the following dependencies installed. You can install most Python packages using pip in your terminal or VS Code integrated terminal.

### 1. Python Version
Python 3.8+ (recommended: 3.12)
### 2. Python Packages
Install these packages (preferably in a virtual environment):

* streamlit – For the web app interface
* numpy – Numerical operations
* matplotlib – Plotting graphs
* librosa – Audio processing
* soundfile – Audio file reading/writing
* parselmouth – Praat integration for acoustic analysis
* openai-whisper – For transcription
### 3. Additional System Dependencies
* Praat: Required for parselmouth. Download from https://www.fon.hum.uva.nl/praat/.
* FFmpeg: Required for librosa and whisper. Install via:
** macOS: brew install ffmpeg
** Ubuntu: sudo apt-get install ffmpeg
** Windows: Download FFmpeg and add to PATH.
### 4. Montreal Forced Aligner (MFA)
Install MFA following instructions at https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html
Ensure mfa is available in your system PATH.

#### 🧩 Montreal Forced Aligner (MFA) Setup
To run the phoneme alignment component of this project, you'll need to install Montreal Forced Aligner (MFA). We strongly recommend installing MFA in a separate virtual environment to avoid package conflicts — especially since MFA has some heavy dependencies.

You can set it up like this:

```bash
conda create -n mfa_env python=3.10
conda activate mfa_env
pip install montreal-forced-aligner
```

Once MFA is installed, you don’t need to activate mfa_env manually when running the main app (app.py). The app handles MFA operations via a subprocess call, which internally accesses the environment to run the aligner. This keeps your working environment clean and avoids dependency chaos 🧼🐍.

#### 🗂️ Built-in English Acoustic & Dictionary References
For convenience and reproducibility, the required English acoustic model and pronunciation dictionary have been saved directly in this repository. This allows the app to access these reference files automatically without requiring the user to download them manually from MFA’s online model repository.

While the MFA binary itself is still executed via the default location in your system’s PATH (inside the mfa_env virtual environment), the app explicitly points to the local copies of the acoustic model and dictionary during alignment. This ensures consistent behaviour across machines and simplifies deployment or sharing of the project 🧳📦.

The files are located here:

```bash
├── requirements.txt     # Required installations
├── MFA                  # MFA dictionary and acoustic source
```

### 5. Bash
The app uses a bash script (run_mfa.sh). On Windows, use WSL or Git Bash.
### 6. VS Code Extensions (optional but recommended)
* Python extension
* Jupyter extension (for .ipynb notebooks)
* Streamlit extension (for easier app development)
* After installing the above, you can run the app with:

For more details, see the code in app.py and the utility modules in utils.

## 📦 Pre-trained Models Warning
⚠️ The official MFA English dictionary and acoustic models are large (~2GB+). This can significantly slow down processing — especially on first use.

💡 I recommend using the english_mfa tiny model, which is faster and lighter, for development and debugging.

You can set this manually in your run_mfa.sh or when calling MFA.

## 🧠 Features
* 🎙 Upload your own voice recording
* 🗯 Detect filler words (customisable list)
* ⏸ Highlight long pauses over a set threshold
* 🎚 Analyse pitch, intensity, jitter, shimmer
* 📊 Clean visual feedback with coaching-style questions

## 📁 Project Structure
```bash

├── app.py                  # Main Streamlit app
├── run_mfa.sh              # Bash script for MFA alignment
├── requirements.txt        # Python dependencies
├── output/                 # Stores analysis outputs (not tracked in Git)
```

## 🙌 Credits
* Montreal Forced Aligner
  * https://montreal-forced-aligner.readthedocs.io/en/latest/
* Praat-Parselmouth
  * https://github.com/YannickJadoul/Parselmouth

## 🔮 Future Plans
* Highlight confidence zones over time
* Visual timeline of acoustic metrics

## 📝 License
This project is licensed under the MIT License. See `LICENSE` for more details.

## 👥 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

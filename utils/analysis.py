def analyse_audio(filename):
    import parselmouth
    from parselmouth.praat import call
    import numpy as np
    import matplotlib.pyplot as plt
    # Load the audio file
    snd = parselmouth.Sound(filename)

    ## Vocal Energy
    # Extract intensity
    intensity = call(snd, "To Intensity", 75.0, 0.0)
    mean_intensity = call(intensity, "Get mean", 0, 0, "dB")
    min_intensity = call(intensity, "Get minimum", 0, 0, "Parabolic")
    max_intensity = call(intensity, "Get maximum", 0, 0, "Parabolic")
    # Get time series data for intensity
    intensity_times = intensity.xs()  # Time points
    intensity_values = [intensity.get_value(time) for time in intensity_times]  # Intensity values
    
    if mean_intensity == 0:
        print("No intensity detected.")
    else:
        print(f"Mean Intensity: {mean_intensity:.2f} dB")
    print(f"Min Intensity: {min_intensity:.2f} dB")
    print(f"Max Intensity: {max_intensity:.2f} dB")
    
    if mean_intensity < 60:
        energy_label = "🔵 Low vocal energy"
    elif mean_intensity < 70:
        energy_label = "🟢 Normal vocal energy"
    elif mean_intensity < 85:
        energy_label = "🟠 High vocal energy"
    else:
        energy_label = "🔴 Very high vocal energy"

    # Extract pitch
    pitch = snd.to_pitch(time_step=0.01, pitch_floor=75, pitch_ceiling=600)
    mean_pitch = call(pitch, "Get mean", 0, 0, "Hertz")
    min_pitch = call(pitch, "Get minimum", 0, 0, "Hertz", "Parabolic")
    max_pitch = call(pitch, "Get maximum", 0, 0, "Hertz", "Parabolic")
    pitch_range = max_pitch - min_pitch
    std_pitch = call(pitch, "Get standard deviation", 0, 0, "Hertz")
    pitch_times = pitch.xs()  # Time points
    pitch_values = pitch.selected_array["frequency"]  # Pitch values (transpose to get 1D array)
    pitch_values[pitch_values == 0] = np.nan
    
    print(f"Min Pitch: {min_pitch:.2f} Hz")
    print(f"Max Pitch: {max_pitch:.2f} Hz")
    print(f"Pitch Range: {pitch_range:.2f} Hz")
    if mean_pitch == 0:
        print("No pitch detected.")
    else:
        print(f"Mean Pitch: {mean_pitch:.2f} Hz")
    print(f"Pitch Standard Deviation: {std_pitch:.2f} Hz")

    ## Voice stability
    point_process = call(snd, "To PointProcess (periodic, cc)", 75, 500)

    # Extract jitter
    jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)

    print(f"Jitter: {jitter:.4f}")

    if jitter < 0.005:
        jitter_label = "🟢 Minimal jitter"
    elif jitter < 0.01:
        jitter_label = "🟡 Normal jitter"
    elif jitter < 0.02:
        jitter_label = "🟠 Moderate jitter"
    else:
        jitter_label = "🔴 High jitter"

    # Extract shimmer
    shimmer = call([snd, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    print(f"Shimmer: {shimmer:.4f}")
    if shimmer < 0.035:
        shimmer_label = "🟢 Normal shimmer"
    elif shimmer < 0.045:
        shimmer_label = "🟠 Moderate shimmer"
    else:
        shimmer_label = "🔴 High shimmer"

    return {
        "intensity": {
            "mean": mean_intensity,
            "min": min_intensity,
            "max": max_intensity,
            "label": energy_label,
            "time": intensity_times,
            "values": intensity_values
        },
        "pitch": {
            "mean": mean_pitch,
            "min": min_pitch,
            "max": max_pitch,
            "range": pitch_range,
            "std": std_pitch,
            "time": pitch_times,
            "values": pitch_values
        },
        "jitter": {
            "value": jitter,
            "label": jitter_label
        },
        "shimmer": {
            "value": shimmer,
            "label": shimmer_label
        }
    }
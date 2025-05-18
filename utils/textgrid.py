from textgrid import TextGrid

# Load the TextGrid file
def load_textgrid(filename):
    tg = TextGrid.fromFile(filename)

    # Inspect all tiers
    for tier in tg.tiers:
        print(f"Tier name: {tier.name}")
        for interval in tier.intervals:
            print(f"{interval.mark} - from {interval.minTime:.2f} to {interval.maxTime:.2f}")

## Speech fluency analysis
def detect_hesitation(filename, filler_set, threshold=0.7):
    tg = TextGrid.fromFile(filename)
    output = []
    used_filler_words = []
    long_pauses = []

    # Detecting long pauses near filler words
    for tier in tg.tiers:
        if "word" in tier.name.lower():
            intervals = tier.intervals
            for i, interval in enumerate(intervals):
                word = interval.mark.strip().lower()
                duration = interval.maxTime - interval.minTime

                if word in filler_set:
                    output.append(f"🗯️ Filler: '{word}' at {interval.minTime:.2f}-{interval.maxTime:.2f}s")
                    used_filler_words.append(word)

                if word == '' and duration > threshold:
                    long_pauses.append({
                        "start": interval.minTime,
                        "end": interval.maxTime,
                        "duration": duration
                    })
                    prev_word = intervals[i - 1].mark.strip().lower() if i > 0 else ''
                    next_word = intervals[i + 1].mark.strip().lower() if i < len(intervals) - 1 else ''

                    if prev_word in filler_set or next_word in filler_set:
                        output.append(f"⏸️ Long pause: {interval.minTime:.2f}-{interval.maxTime:.2f}s between '{prev_word}' and '{next_word}'")
    return output, used_filler_words, long_pauses
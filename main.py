import sys
from pathlib import Path
import time
import warnings
import logging

import whisperx
import torch

# Disable all logging calls
logging.disable(logging.CRITICAL + 1)

# Disable warnings
warnings.filterwarnings("ignore")

EXTRA_DELAY = 0.25   # seconds words stay longer
MIN_DURATION = 0.35  # minimum readable duration

STEP_WIDTH = 30  # adjusts print message spacing

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    millis = int((secs - int(secs)) * 1000)

    return f"{hours:02}:{minutes:02}:{int(secs):02},{millis:03}"


def write_srt(words, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, word in enumerate(words, start=1):
            start = format_time(word["start"])
            end = format_time(word["end"])

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{word['word']}\n\n")


def clean_words(words):
    """Remove words without timestamps"""
    clean = []
    for w in words:
        if "start" in w and "end" in w and w["word"].strip():
            clean.append(w)
    return clean


def adjust_timings(words):
    """Improve readability timing"""
    adjusted = []

    for i, word in enumerate(words):
        start = word["start"]

        if i < len(words) - 1:
            next_start = words[i + 1]["start"]
        else:
            next_start = word["end"] + EXTRA_DELAY

        end = max(word["end"], start + MIN_DURATION)

        # extend slightly but avoid overlap
        end = min(next_start, end + EXTRA_DELAY)

        adjusted.append({
            "start": start,
            "end": end,
            "word": word["word"].strip()
        })

    return adjusted


def start_step(message):
    print(f"{message + '...':<{STEP_WIDTH}}", end="", flush=True)


def end_step(start_time):
    elapsed = time.time() - start_time
    print(f"{elapsed:.2f}")


def main(audio_path):
    t = time.time()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"{device=}")

    start_step("Loading Whisper model")
    model = whisperx.load_model("large-v3", device)
    end_step(t)

    start_step("Loading audio")
    audio = whisperx.load_audio(audio_path)
    end_step(t)

    start_step("Transcribing")
    result = model.transcribe(audio, language="en")
    end_step(t)

    start_step("Loading alignment model")
    align_model, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    end_step(t)

    start_step("Aligning words")
    aligned = whisperx.align(result["segments"], align_model, metadata, audio, device)
    end_step(t)

    words = []
    for seg in aligned["segments"]:
        if "words" in seg:
            words.extend(seg["words"])

    start_step("Post-processing")
    words = clean_words(words)
    words = adjust_timings(words)
    end_step(t)

    start_step("Writing SRT")
    srt_path = Path(audio_path).with_suffix(".srt")
    write_srt(words, srt_path)
    end_step(t)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py main.py example.wav")
        sys.exit(1)
    
    main(sys.argv[1])
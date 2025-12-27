import os
from pathlib import Path
import whisper
import subprocess

from src.audio_extract import audio_extract
from src.audio_transcribe import transcribe_audio
from src.caption_gen import to_srt, to_vtt
from src.video_splitter import split_video_by_size
from src.embed_caption import embed_subtitles
from media_tool.media_tool import run

def main():
    WORKDIR = Path.cwd()
    print(f"Working directory: {WORKDIR}")

    # Create necessary directories
    DIRS = {
        "subbed": WORKDIR / "subbed",
        "srt": WORKDIR / "srt",
        "transcribed": WORKDIR / "transcribed",
        "audio": WORKDIR / "audio",
        "input_files": WORKDIR / "input_files",
    }
    for d in DIRS.values():
        d.mkdir(parents=True, exist_ok=True)

    # Directory where videos are stored
    video_root = Path("/mnt/c/Users/ingca/Videos/Diavoli S01 (2020) 1080p WEB-DL H264 iTA ENG AC3 - iDN_CreW")
    
    # Filter out certain episodes if needed
    mkv_files = [
        f for f in video_root.iterdir()
        if f.suffix == ".mkv" and all(ep not in f.name for ep in ["S01E08","S01E09","S01E10","S01E02","S01E03","S01E04","S01E05","S01E06","S01E07"])
    ]

    # Languages and model
    langs = ["eng", "ita"]
    default_lang = "eng"  # updated to match audio stream metadata
    model = whisper.load_model("medium")

    for video_path in mkv_files:
        print(f"Processing: {video_path.name}")

        # Step 0: Define output paths
        audio_file = DIRS["audio"] / f"{video_path.stem}_audio.wav"
        srt_file = DIRS["srt"] / f"{video_path.stem}_subtitles.srt"
        output_mkv = DIRS["subbed"] / f"{video_path.stem}_with_subs.mkv"

        # Step 1: Keep only selected languages
        video_filtered_path = run(
            input_path=video_path,
            output_dir=DIRS["input_files"],
            languages=langs,
            default_language=default_lang
        )

        # Step 2: Extract audio 
        audio_extract(filename=video_filtered_path, output_filename=audio_file, lang=default_lang)


        # Step 3: Transcribe to SRT
        try:
            srt_path = transcribe_audio(
                audio_file=audio_file,
                output_dir=DIRS["srt"],
                output_format="srt",
                model=model,
                language="english"
            )
        except Exception as e:
            print(f"Error during transcription: {type(e).__name__}: {e}")
            continue

        # Step 4: Embed subtitles
        try:
            embed_subtitles(
                input_mkv=video_path,
                subtitle_files=[{"file": srt_path, "language": default_lang}],
                output_mkv=output_mkv
            )
        except Exception as e:
            print(f"Error embedding subtitles: {type(e).__name__}: {e}")
            continue

        print(f"Completed {video_path.name} -> {output_mkv.name}")


if __name__ == "__main__":
    main()

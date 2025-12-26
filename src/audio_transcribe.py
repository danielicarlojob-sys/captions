from pathlib import Path
import whisper


def transcribe_audio(
    audio_file: str | Path,
    output_dir: str | Path,
    output_format: str = "srt",
    model=None,
    language: str | None = None
) -> Path:
    """
    Transcribe audio using Whisper and emit subtitle file.
    """
    audio_file = Path(audio_file)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if model is None:
        model = whisper.load_model("medium")

    result = model.transcribe(
        str(audio_file),
        language=language,
        verbose=False
    )

    output_path = output_dir / f"{audio_file.stem}.{output_format}"

    if output_format == "srt":
        _write_srt(result["segments"], output_path)
    elif output_format == "vtt":
        _write_vtt(result["segments"], output_path)
    else:
        raise ValueError("Unsupported output format")

    return output_path


def _format_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}".replace(".", ",")


def _write_srt(segments, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            f.write(f"{i}\n")
            f.write(f"{_format_ts(seg['start'])} --> {_format_ts(seg['end'])}\n")
            f.write(seg["text"].strip() + "\n\n")


def _write_vtt(segments, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for seg in segments:
            f.write(f"{_format_ts(seg['start']).replace(',', '.')} --> "
                    f"{_format_ts(seg['end']).replace(',', '.')}\n")
            f.write(seg["text"].strip() + "\n\n")

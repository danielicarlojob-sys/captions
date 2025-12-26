from pathlib import Path
from src.audio_transcribe import transcribe_audio


def to_srt(audio_file, output_dir, model=None, language=None):
    return transcribe_audio(
        audio_file=audio_file,
        output_dir=output_dir,
        output_format="srt",
        model=model,
        language=language
    )


def to_vtt(audio_file, output_dir, model=None, language=None):
    return transcribe_audio(
        audio_file=audio_file,
        output_dir=output_dir,
        output_format="vtt",
        model=model,
        language=language
    )

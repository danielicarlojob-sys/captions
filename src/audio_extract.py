from pathlib import Path
import subprocess


def audio_extract(filename: str, output_filename: str) -> Path:
    """
    Extracts audio from a video file and saves it as WAV (16kHz mono PCM).
    """
    input_path = Path(filename)
    output_path = Path(output_filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-acodec", "pcm_s16le",
        str(output_path)
    ]

    subprocess.run(cmd, check=True)
    return output_path

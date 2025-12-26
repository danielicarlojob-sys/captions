from pathlib import Path
import subprocess


def run(
    input_path: str | Path,
    output_dir: str | Path,
    languages: list[str],
    default_language: str
):
    """
    Keeps only selected audio languages and sets default.
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / input_path.name

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-map", "0:v"
    ]

    for lang in languages:
        cmd += ["-map", f"0:a:m:language:{lang}?"]

    cmd += [
        "-c", "copy",
        "-disposition:a:0", "default",
        str(output_path)
    ]

    subprocess.run(cmd, check=True)
    return output_path

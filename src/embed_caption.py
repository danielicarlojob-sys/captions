from pathlib import Path
import subprocess


def embed_subtitles(
    input_mkv: str | Path,
    subtitle_files: list[dict],
    output_mkv: str | Path
):
    """
    Embeds subtitles into an MKV file.
    """
    input_mkv = Path(input_mkv)
    output_mkv = Path(output_mkv)
    output_mkv.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["ffmpeg", "-y", "-i", str(input_mkv)]

    for sub in subtitle_files:
        cmd += ["-i", str(sub["file"])]

    cmd += ["-map", "0"]

    for i, sub in enumerate(subtitle_files, start=1):
        cmd += [
            "-map", str(i),
            "-metadata:s:s:{}".format(i - 1),
            f"language={sub['language']}"
        ]

    cmd += ["-c", "copy", str(output_mkv)]

    subprocess.run(cmd, check=True)

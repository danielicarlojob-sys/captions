from pathlib import Path
import subprocess


def split_video_by_size(
    input_video: str | Path,
    output_dir: str | Path,
    max_size_mb: int = 3900
) -> list[Path]:
    """
    Splits a video into chunks below max_size_mb.
    """
    input_video = Path(input_video)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = output_dir / f"{input_video.stem}_part_%03d.mkv"

    cmd = [
        "ffmpeg",
        "-i", str(input_video),
        "-c", "copy",
        "-map", "0",
        "-f", "segment",
        "-segment_size", str(max_size_mb * 1024 * 1024),
        str(output_pattern)
    ]

    subprocess.run(cmd, check=True)
    return sorted(output_dir.glob(f"{input_video.stem}_part_*.mkv"))

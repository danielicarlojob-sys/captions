import subprocess
from pathlib import Path

def audio_extract(
    filename: str | Path,
    output_filename: str | Path,
    stream_index: str | None = None,  # Specific FFmpeg stream index, e.g., "0:1"
    lang: str | None = None,          # Audio language code, e.g., "eng"
    channels: int = 1,                # Number of output audio channels
    sample_rate: int = 16000,         # Sampling rate in Hz
    codec: str = "pcm_s16le"          # Audio codec for output (default WAV)
) -> None:
    """
    Extracts an audio track from a video file and saves it as a WAV (or other format) file.

    The function can select the audio stream either by a specific FFmpeg stream index
    or by language code. If neither is specified, FFmpeg uses the default audio track.

    Parameters
    ----------
    filename : str | Path
        Path to the input video file.
    output_filename : str | Path
        Path where the extracted audio will be saved.
    stream_index : str | None, optional
        FFmpeg audio stream specifier (e.g., "0:1"). Overrides language selection.
    lang : str | None, optional
        ISO 639-2/ISO 639-3 language code (e.g., "eng"). Used if stream_index is None.
    channels : int, optional
        Number of audio channels in the output. Default is 1 (mono).
    sample_rate : int, optional
        Sampling rate of the output audio in Hz. Default is 16000.
    codec : str, optional
        Audio codec for the output file. Default is 'pcm_s16le' (WAV compatible).

    Raises
    ------
    subprocess.CalledProcessError
        If FFmpeg fails to extract the audio track.
    """

    # Convert Path objects to strings if needed
    filename = str(filename)
    output_filename = str(output_filename)

    # Base FFmpeg command
    cmd = ["ffmpeg", "-y", "-i", filename]

    # Select audio stream: priority -> stream_index > lang > default
    if stream_index is not None:
        cmd += ["-map", stream_index]  # Select specific stream by index
    elif lang is not None:
        # Select first audio stream matching the language tag
        cmd += ["-map", f"0:m:language:{lang}"]

    # Append audio extraction parameters
    cmd += [
        "-vn",                     # Ignore video streams
        "-ac", str(channels),      # Set number of audio channels
        "-ar", str(sample_rate),   # Set sampling rate
        "-acodec", codec,          # Set audio codec
        output_filename            # Output file path
    ]

    # Run FFmpeg command and handle errors
    try:
        subprocess.run(cmd, check=True)
        print(f"Audio extracted successfully: {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg failed to extract audio from {filename}")
        raise e

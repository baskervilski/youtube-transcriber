from rich import print
from pathlib import Path


EXTRACTION_DIR = Path("extracted")

if not EXTRACTION_DIR.exists():
    EXTRACTION_DIR.mkdir(parents=True, exist_ok=True)


def _download_yt_video(url) -> Path:
    from pytubefix import YouTube

    yt = YouTube(
        url,
        use_oauth=True,
        allow_oauth_cache=True,
    )

    video_stream = yt.streams.get_lowest_resolution()
    title = yt.title

    print(f"Downloading: {title}")
    filename = video_stream.download(
        output_path=str(EXTRACTION_DIR), filename=f"{title}.mp4"
    )
    print("Download complete!")
    print(f"Filename: {filename}")
    return Path(filename)


def _transcribe(audio_file: Path):
    if audio_file.suffix != ".mp3":
        raise ValueError(f"Please provide an .mp3 file. Got {audio_file!s}")

    import whisper

    print("[b yellow]Loading model...")
    model = whisper.load_model("base")
    print("[b yellow]Transcribing...")
    result = model.transcribe(str(audio_file))

    print("Writing transcript")
    txt_filename = audio_file.with_suffix(".txt")
    txt_filename.write_text(result["text"])
    print(f"Transcript written to {txt_filename}")


def _extract_audio(vid_file: Path) -> Path:
    from moviepy import VideoFileClip

    # Load the mp4 file
    video = VideoFileClip(vid_file)
    audio_file = vid_file.with_suffix(".mp3")

    # Extract audio from video
    video.audio.write_audiofile(audio_file)

    return audio_file


def main(url: str):
    filename = _download_yt_video(url)
    audio_file = _extract_audio(filename)
    _transcribe(audio_file)


if __name__ == "__main__":
    import sys

    url = sys.argv[1]
    main(url)

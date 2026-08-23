from functools import lru_cache
from pathlib import Path

from groq import Groq

from app.core.config import settings


# Groq Whisper model
WHISPER_MODEL = "whisper-large-v3-turbo"


@lru_cache
def get_groq_client() -> Groq:
    """
    Create and cache the Groq client.
    """

    if not settings.GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    return Groq(
        api_key=settings.GROQ_API_KEY
    )


def transcribe_audio(
    file_path: str,
) -> str:
    """
    Convert an audio file into text using
    Groq Whisper.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {file_path}"
        )

    if path.stat().st_size == 0:
        raise ValueError(
            "Audio file is empty."
        )

    client = get_groq_client()

    with path.open("rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=WHISPER_MODEL,
            response_format="text",
        )

    if not transcription:
        raise RuntimeError(
            "Whisper returned an empty transcript."
        )

    return str(transcription).strip()
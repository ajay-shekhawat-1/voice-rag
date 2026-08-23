import hashlib
import os
import uuid

from app.services.chunking import chunk_text
from app.services.embeddings import create_embeddings
from app.services.speech_to_text import transcribe_audio
from app.services.vector_store import (
    create_collection_if_not_exists,
    document_exists,
    upsert_text_chunks,
)


def calculate_file_hash(file_path: str) -> str:
    """
    Calculate SHA-256 hash of an audio file.

    The hash is used to detect duplicate uploads.
    """

    if not os.path.isfile(file_path):
        raise ValueError(
            f"Audio file not found: {file_path}"
        )

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as audio_file:
        for chunk in iter(
            lambda: audio_file.read(1024 * 1024),
            b"",
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def ingest_voice(
    file_path: str,
    source_name: str,
) -> dict:
    """
    Complete voice knowledge ingestion pipeline.

    Audio
      ↓
    SHA-256 duplicate check
      ↓
    Whisper
      ↓
    Transcript
      ↓
    Chunks
      ↓
    Embeddings
      ↓
    Qdrant
    """

    # -----------------------------------------
    # 1. Validate audio file
    # -----------------------------------------

    if not os.path.isfile(file_path):
        raise ValueError(
            f"Audio file not found: {file_path}"
        )

    # -----------------------------------------
    # 2. Calculate file hash
    # -----------------------------------------

    file_hash = calculate_file_hash(
        file_path
    )

    # -----------------------------------------
    # 3. Create collection if necessary
    # -----------------------------------------

    create_collection_if_not_exists()

    # -----------------------------------------
    # 4. Check for duplicate audio
    # -----------------------------------------

    if document_exists(file_hash):
        return {
            "success": True,
            "duplicate": True,
            "document_id": None,
            "source_name": source_name,
            "source_type": "audio",
            "file_hash": file_hash,
            "characters": 0,
            "chunks": 0,
            "vectors_stored": 0,
            "message": (
                "This audio file has already "
                "been ingested."
            ),
        }

    # -----------------------------------------
    # 5. Create unique document ID
    # -----------------------------------------

    document_id = str(uuid.uuid4())

    # -----------------------------------------
    # 6. Audio → transcript
    # -----------------------------------------

    transcript = transcribe_audio(
        file_path
    )

    if not transcript.strip():
        raise ValueError(
            "No speech could be detected in the audio."
        )

    # -----------------------------------------
    # 7. Transcript → chunks
    # -----------------------------------------

    chunks = chunk_text(
        transcript,
        chunk_size=800,
        chunk_overlap=120,
    )

    if not chunks:
        raise ValueError(
            "No usable chunks were created."
        )

    # -----------------------------------------
    # 8. Chunks → embeddings
    # -----------------------------------------

    embeddings = create_embeddings(
        chunks
    )

    if len(embeddings) != len(chunks):
        raise RuntimeError(
            "Embedding count does not match "
            "chunk count."
        )

    # -----------------------------------------
    # 9. Store vectors
    # -----------------------------------------

    stored_count = upsert_text_chunks(
        chunks=chunks,
        embeddings=embeddings,
        source_name=source_name,
        source_type="audio",
        document_id=document_id,
        file_hash=file_hash,
    )

    # -----------------------------------------
    # 10. Return complete result
    # -----------------------------------------

    return {
        "success": True,
        "duplicate": False,
        "document_id": document_id,
        "source_name": source_name,
        "source_type": "audio",
        "file_hash": file_hash,
        "characters": len(transcript),
        "chunks": len(chunks),
        "vectors_stored": stored_count,
        "message": (
            "Voice knowledge processed "
            "successfully."
        ),
    }
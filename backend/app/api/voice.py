import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.voice_ingestion import ingest_voice


router = APIRouter(
    prefix="/api/voice",
    tags=["Voice"],
)


ALLOWED_AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".webm",
}


@router.post("/ingest")
async def ingest_voice_endpoint(
    file: UploadFile = File(...),
):
    """
    Upload voice/audio knowledge and store
    its semantic representation in Qdrant.
    """

    # -----------------------------------------
    # 1. Validate filename
    # -----------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    # -----------------------------------------
    # 2. Validate audio extension
    # -----------------------------------------

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported audio format. "
                "Allowed formats: "
                "mp3, wav, m4a, webm."
            ),
        )

    temporary_path = None

    try:
        # -----------------------------------------
        # 3. Read uploaded audio
        # -----------------------------------------

        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded audio is empty.",
            )

        # -----------------------------------------
        # 4. Create temporary audio file
        # -----------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temporary_file:

            temporary_file.write(
                file_bytes
            )

            temporary_path = (
                temporary_file.name
            )

        # -----------------------------------------
        # 5. Process voice
        # -----------------------------------------

        result = ingest_voice(
            file_path=temporary_path,
            source_name=file.filename,
        )

        # -----------------------------------------
        # 6. Handle duplicate audio
        # -----------------------------------------

        if result.get("duplicate", False):
            return {
                "success": True,
                "duplicate": True,
                "message": result.get(
                    "message",
                    "This audio file has already "
                    "been ingested.",
                ),
                "source_name": result.get(
                    "source_name",
                    file.filename,
                ),
                "source_type": result.get(
                    "source_type",
                    "audio",
                ),
                "characters": result.get(
                    "characters",
                    0,
                ),
                "chunks": result.get(
                    "chunks",
                    0,
                ),
                "vectors_stored": result.get(
                    "vectors_stored",
                    0,
                ),
            }

        # -----------------------------------------
        # 7. Return successful ingestion result
        # -----------------------------------------

        return {
            "success": True,
            "duplicate": False,
            "message": (
                "Voice knowledge processed "
                "successfully."
            ),
            "source_name": result.get(
                "source_name",
                file.filename,
            ),
            "source_type": result.get(
                "source_type",
                "audio",
            ),
            "characters": result.get(
                "characters",
                0,
            ),
            "chunks": result.get(
                "chunks",
                0,
            ),
            "vectors_stored": result.get(
                "vectors_stored",
                0,
            ),
        }

    except HTTPException:
        raise

    except Exception as exc:

        print(
            "Voice ingestion error:",
            type(exc).__name__,
            str(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to process "
                "voice data."
            ),
        )

    finally:

        # -----------------------------------------
        # 8. Remove temporary audio file
        # -----------------------------------------

        if (
            temporary_path
            and os.path.exists(
                temporary_path
            )
        ):
            os.remove(
                temporary_path
            )
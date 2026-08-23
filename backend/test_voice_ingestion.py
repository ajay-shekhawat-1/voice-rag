import sys

from app.services.voice_ingestion import ingest_voice


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python test_voice_ingestion.py <audio_file>"
        )
        sys.exit(1)

    file_path = sys.argv[1]

    print()
    print("=" * 32)
    print("VOICE RAG INGESTION TEST")
    print("=" * 32)
    print()
    print(f"Audio: {file_path}")
    print()

    try:
        result = ingest_voice(
            file_path=file_path,
            source_name=file_path,
        )

        print("RESULT")
        print("-" * 32)
        print(f"Source: {result.get('source_name')}")
        print(f"Type: {result.get('source_type')}")

        # -----------------------------------------
        # Duplicate upload
        # -----------------------------------------

        if result.get("duplicate") is True:
            print("Status: DUPLICATE")
            print(
                "Message:",
                result.get(
                    "message",
                    "Audio has already been ingested.",
                ),
            )

        # -----------------------------------------
        # New upload
        # -----------------------------------------

        else:
            print(
                f"Characters: {result.get('characters', 0)}"
            )
            print(
                f"Chunks: {result.get('chunks', 0)}"
            )
            print(
                f"Vectors stored: "
                f"{result.get('vectors_stored', 0)}"
            )

        print()

    except Exception as exc:
        print("ERROR:")
        print(
            f"{type(exc).__name__}: {exc}"
        )


if __name__ == "__main__":
    main()
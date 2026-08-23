import sys

from app.services.speech_to_text import transcribe_audio


def main():

    if len(sys.argv) != 2:
        print(
            "Usage:"
            " python test_speech_to_text.py <audio_file>"
        )
        return

    audio_path = sys.argv[1]

    print("\n================================")
    print("WHISPER SPEECH-TO-TEXT TEST")
    print("================================")

    print(f"\nAudio file:")
    print(audio_path)

    try:

        transcript = transcribe_audio(
            audio_path
        )

        print("\nTranscript:")
        print("--------------------------------")

        print(transcript)

        print("--------------------------------")

        print(
            f"\nCharacters: {len(transcript)}"
        )

        print("\n================================")
        print("WHISPER TEST SUCCESSFUL")
        print("================================\n")

    except Exception as exc:

        print("\nERROR:")
        print(
            f"{type(exc).__name__}: {exc}"
        )


if __name__ == "__main__":
    main()
    
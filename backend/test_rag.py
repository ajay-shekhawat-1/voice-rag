from app.services.rag import ask_rag


def main():
    questions = [
        "When was the company founded?",
        "How many paid holidays do employees receive?",
        "What is the refund policy?",
        "What is the company's stock price?",
    ]

    print("\n================================")
    print("RAG TEST")
    print("================================")

    for question in questions:
        print(f"\nQUESTION:")
        print(question)

        result = ask_rag(
            question=question,
            top_k=5,
        )

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")

        for source in result["sources"]:
            print(
                f"- {source['source_name']} "
                f"(chunk {source['chunk_index']}, "
                f"score={source['score']:.4f})"
            )

        print("\n--------------------------------")

    print("\n================================")
    print("RAG TEST COMPLETE")
    print("================================\n")


if __name__ == "__main__":
    main()
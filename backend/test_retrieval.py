from app.services.embeddings import create_embedding
from app.services.vector_store import search_vectors


def main():
    question = "When was the company founded?"

    print("\n================================")
    print("VECTOR SEARCH TEST")
    print("================================")

    print(f"\nQuestion: {question}")

    query_vector = create_embedding(question)

    results = search_vectors(
        query_vector=query_vector,
        limit=3,
    )

    print(f"\nRetrieved {len(results)} results.")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Score: {result.score}")
        print(f"Source: {result.payload.get('source_name')}")
        print(f"Text: {result.payload.get('text')}")

    print("\n================================\n")


if __name__ == "__main__":
    main()
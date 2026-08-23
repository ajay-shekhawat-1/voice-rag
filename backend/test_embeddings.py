from app.services.embeddings import create_embedding


def main():
    text = "This is a test sentence for our Voice RAG system."

    vector = create_embedding(text)

    print("\n================================")
    print("EMBEDDING TEST")
    print("================================")
    print(f"Input text: {text}")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")
    print("================================\n")


if __name__ == "__main__":
    main()
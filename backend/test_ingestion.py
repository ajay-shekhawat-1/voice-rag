from app.services.chunking import chunk_text
from app.services.embeddings import create_embeddings
from app.services.vector_store import (
    create_collection_if_not_exists,
    upsert_text_chunks,
)


def main():
    text = """
    Our company was founded in 2015.

    The company provides artificial intelligence
    and machine learning solutions for businesses.

    Employees receive 24 paid holidays every year.

    Customers can request a refund within 30 days
    of their original purchase.

    Customer support is available Monday through Friday.
    """

    print("\n================================")
    print("VOICE RAG INGESTION TEST")
    print("================================")

    print("\n1. Creating chunks...")

    chunks = chunk_text(
        text,
        chunk_size=200,
        chunk_overlap=40,
    )

    print(f"Created {len(chunks)} chunks.")

    print("\n2. Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print(
        f"Created {len(embeddings)} embeddings."
    )

    print(
        f"Embedding dimensions: {len(embeddings[0])}"
    )

    print("\n3. Checking Qdrant collection...")

    create_collection_if_not_exists()

    print("Collection ready.")

    print("\n4. Storing vectors...")

    stored_count = upsert_text_chunks(
        chunks=chunks,
        embeddings=embeddings,
        source_name="test_company_information.txt",
        source_type="text",
    )

    print(
        f"Successfully stored {stored_count} vectors."
    )

    print("\n================================")
    print("INGESTION SUCCESSFUL")
    print("================================\n")


if __name__ == "__main__":
    main()
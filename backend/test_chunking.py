from app.services.chunking import chunk_text


def main():
    text = """
    Our company was founded in 2015.
    The company provides artificial intelligence solutions
    for businesses across multiple industries.

    Employees receive 24 paid holidays every year.
    The refund policy allows customers to request a refund
    within 30 days of purchase.

    Customer support is available Monday through Friday.
    """

    chunks = chunk_text(
        text,
        chunk_size=150,
        chunk_overlap=30,
    )

    print("\n================================")
    print("CHUNKING TEST")
    print("================================")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {index} ---")
        print(chunk)

    print("\n================================")
    print(f"Total chunks: {len(chunks)}")
    print("================================\n")


if __name__ == "__main__":
    main()
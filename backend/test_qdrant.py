from qdrant_client import QdrantClient

from app.core.config import settings


def main():
    if not settings.QDRANT_URL:
        raise RuntimeError("QDRANT_URL is not configured.")

    if not settings.QDRANT_API_KEY:
        raise RuntimeError("QDRANT_API_KEY is not configured.")

    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )

    collections = client.get_collections()

    print("\n================================")
    print("QDRANT CONNECTION SUCCESSFUL")
    print("================================")
    print(f"Cluster URL: {settings.QDRANT_URL}")
    print(f"Collections: {collections.collections}")
    print("================================\n")


if __name__ == "__main__":
    main()
    
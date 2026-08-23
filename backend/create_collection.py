from app.services.vector_store import create_collection_if_not_exists
from app.core.config import settings


def main():
    create_collection_if_not_exists()

    print("\n================================")
    print("COLLECTION READY")
    print("================================")
    print(f"Collection: {settings.QDRANT_COLLECTION}")
    print("Vector size: 384")
    print("Distance: COSINE")
    print("================================\n")


if __name__ == "__main__":
    main()
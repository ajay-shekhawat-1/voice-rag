from app.core.config import settings
from app.services.vector_store import get_qdrant_client


def main():
    client = get_qdrant_client()
    collection = settings.QDRANT_COLLECTION

    print("=" * 50)
    print("CLEARING TEST DATA")
    print("=" * 50)
    print(f"Collection: {collection}")

    response = client.scroll(
        collection_name=collection,
        limit=100,
        with_payload=False,
        with_vectors=False,
    )

    points = response[0]

    if not points:
        print("No points found.")
        return

    point_ids = [point.id for point in points]

    print(f"Deleting {len(point_ids)} points...")

    client.delete(
        collection_name=collection,
        points_selector=point_ids,
    )

    print("All test points deleted successfully.")


if __name__ == "__main__":
    main()
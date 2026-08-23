from functools import lru_cache
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.core.config import settings


# ============================================================
# VECTOR CONFIGURATION
# ============================================================

# all-MiniLM-L6-v2 produces 384-dimensional embeddings.
VECTOR_SIZE = 384


# ============================================================
# QDRANT CLIENT
# ============================================================

@lru_cache
def get_qdrant_client() -> QdrantClient:
    if not settings.QDRANT_URL:
        raise RuntimeError("QDRANT_URL is not configured.")

    if not settings.QDRANT_API_KEY:
        raise RuntimeError("QDRANT_API_KEY is not configured.")

    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )


# ============================================================
# CREATE COLLECTION
# ============================================================

def create_collection_if_not_exists() -> None:
    client = get_qdrant_client()

    collections = client.get_collections()

    existing_collections = {
        collection.name
        for collection in collections.collections
    }

    if settings.QDRANT_COLLECTION not in existing_collections:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    # Create payload index for duplicate detection.
    # Qdrant requires an index before filtering by file_hash.
    try:
        client.create_payload_index(
            collection_name=settings.QDRANT_COLLECTION,
            field_name="file_hash",
            field_schema="keyword",
        )
    except Exception as exc:
        # Index may already exist.
        print(
            f"file_hash index check: {type(exc).__name__}: {exc}"
        )


# ============================================================
# CHECK DUPLICATE AUDIO
# ============================================================

def document_exists(file_hash: str) -> bool:
    """
    Check whether an audio file with the same SHA-256
    hash has already been stored in Qdrant.
    """

    if not file_hash:
        return False

    client = get_qdrant_client()

    result = client.scroll(
        collection_name=settings.QDRANT_COLLECTION,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="file_hash",
                    match=MatchValue(value=file_hash),
                )
            ]
        ),
        limit=1,
        with_payload=False,
        with_vectors=False,
    )

    points = result[0]

    return len(points) > 0


# ============================================================
# UPSERT AUDIO TRANSCRIPT CHUNKS
# ============================================================

def upsert_text_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    source_name: str,
    source_type: str,
    document_id: str,
    file_hash: str,
) -> int:
    """
    Store transcript chunks and embeddings in Qdrant.

    Qdrant stores:
    - transcript text
    - source name
    - source type
    - document ID
    - file hash
    - chunk index
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks must match number of embeddings."
        )

    if not chunks:
        return 0

    if not document_id:
        raise ValueError("document_id is required.")

    if not file_hash:
        raise ValueError("file_hash is required.")

    client = get_qdrant_client()

    points = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "source_name": source_name,
                "source_type": source_type,
                "document_id": document_id,
                "file_hash": file_hash,
                "chunk_index": index,
            },
        )

        points.append(point)

    client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=points,
    )

    return len(points)


# ============================================================
# SEARCH VECTORS
# ============================================================

def search_vectors(
    query_vector: list[float],
    limit: int = 5,
):
    client = get_qdrant_client()

    return client.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=query_vector,
        limit=limit,
    ).points
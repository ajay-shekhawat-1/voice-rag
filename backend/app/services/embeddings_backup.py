from functools import lru_cache

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache
def get_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model once and reuse it.
    """

    return SentenceTransformer(MODEL_NAME)


def create_embedding(text: str) -> list[float]:
    """
    Convert one piece of text into a 384-dimensional vector.
    """

    if not text or not text.strip():
        raise ValueError("Cannot create an embedding from empty text.")

    model = get_embedding_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()


def create_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convert multiple text chunks into embeddings.
    """

    if not texts:
        return []

    cleaned_texts = [
        text.strip()
        for text in texts
        if text and text.strip()
    ]

    if not cleaned_texts:
        return []

    model = get_embedding_model()

    embeddings = model.encode(
        cleaned_texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()
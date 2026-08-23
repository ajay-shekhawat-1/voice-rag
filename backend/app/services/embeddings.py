from functools import lru_cache

from fastembed import TextEmbedding


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache
def get_embedding_model() -> TextEmbedding:
    """
    Load the FastEmbed model once and reuse it.

    FastEmbed uses ONNX Runtime instead of the
    heavyweight PyTorch/Sentence-Transformers runtime.
    """
    return TextEmbedding(model_name=MODEL_NAME)


def create_embedding(text: str) -> list[float]:
    """
    Convert one text string into a 384-dimensional vector.
    """

    if not text or not text.strip():
        raise ValueError(
            "Cannot create an embedding from empty text."
        )

    model = get_embedding_model()

    embedding = next(
        model.embed([text.strip()])
    )

    return embedding.tolist()


def create_embeddings(
    texts: list[str],
) -> list[list[float]]:
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

    embeddings = model.embed(cleaned_texts)

    return [
        embedding.tolist()
        for embedding in embeddings
    ]
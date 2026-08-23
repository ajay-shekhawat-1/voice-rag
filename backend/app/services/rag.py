from app.services.embeddings import create_embedding
from app.services.llm import generate_answer
from app.services.vector_store import search_vectors


def build_context(results) -> str:
    """
    Convert Qdrant search results into LLM context.
    """

    context_parts = []

    for index, result in enumerate(results, start=1):
        text = result.payload.get("text", "")
        source_name = result.payload.get(
            "source_name",
            "Unknown source",
        )

        chunk_index = result.payload.get(
            "chunk_index",
            0,
        )

        context_parts.append(
            f"""
SOURCE {index}
Source name: {source_name}
Chunk: {chunk_index}

Content:
{text}
"""
        )

    return "\n".join(context_parts)


def ask_rag(
    question: str,
    top_k: int = 5,
) -> dict:
    """
    Complete RAG pipeline:

    question
        ↓
    embedding
        ↓
    Qdrant search
        ↓
    context
        ↓
    Groq LLM
        ↓
    answer
    """

    if not question or not question.strip():
        raise ValueError(
            "Question cannot be empty."
        )

    question = question.strip()

    # 1. Create question embedding
    query_vector = create_embedding(question)

    # 2. Search Qdrant
    results = search_vectors(
        query_vector=query_vector,
        limit=top_k,
    )

    # 3. Handle no results
    if not results:
        return {
            "question": question,
            "answer": (
                "I could not find relevant information "
                "in the knowledge base."
            ),
            "sources": [],
        }

    # 4. Build context
    context = build_context(results)

    # 5. Generate answer
    answer = generate_answer(
        question=question,
        context=context,
    )

    # 6. Prepare source information
    sources = []

    for result in results:
        sources.append(
            {
                "source_name": result.payload.get(
                    "source_name",
                    "Unknown source",
                ),
                "source_type": result.payload.get(
                    "source_type",
                    "unknown",
                ),
                "chunk_index": result.payload.get(
                    "chunk_index",
                    0,
                ),
                "score": result.score,
            }
        )

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }
from functools import lru_cache

from groq import Groq

from app.core.config import settings


LLM_MODEL = "openai/gpt-oss-20b"


@lru_cache
def get_groq_client() -> Groq:
    if not settings.GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    return Groq(
        api_key=settings.GROQ_API_KEY
    )


def generate_answer(
    question: str,
    context: str,
) -> str:
    """
    Generate a grounded answer using the retrieved RAG context.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if not context.strip():
        return (
            "I could not find relevant information "
            "in the knowledge base."
        )

    client = get_groq_client()

    system_prompt = """
You are a helpful RAG assistant.

Your job is to answer the user's question using ONLY
the information provided in the CONTEXT.

Rules:

1. Do not invent or assume information.
2. Do not use outside knowledge.
3. If the answer cannot be found in the context,
   clearly say that the information is not available
   in the provided knowledge base.
4. Give a concise and direct answer.
5. When possible, explain the answer using the
   relevant information from the context.
"""

    user_prompt = f"""
CONTEXT:
----------------
{context}
----------------

QUESTION:
{question}

Answer the question using only the context above.
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0,
        max_tokens=500,
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError(
            "Groq returned an empty response."
        )

    return answer.strip()
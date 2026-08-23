from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag import ask_rag


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    question: str


@router.post("")
async def chat(request: ChatRequest):
    try:
        result = ask_rag(
            question=request.question,
            top_k=5,
        )

        return {
            "success": True,
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        print(
            f"RAG error: {type(exc).__name__}: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to generate RAG answer.",
        )
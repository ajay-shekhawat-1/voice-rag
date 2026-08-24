from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.voice import router as voice_router


app = FastAPI(
    title="Voice RAG API",
    description="Deployment-ready Voice RAG backend",
    version="1.0.0",
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

ALLOWED_ORIGINS = [
    # Local Vite development
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",

    # Vercel production
    "https://voice-r2qz6zqfc-ajay-2382.vercel.app",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTERS
# ============================================================

app.include_router(chat_router)
app.include_router(voice_router)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():
    return {
        "message": "Voice RAG API is running",
        "status": "success",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "voice-rag-backend",
    }
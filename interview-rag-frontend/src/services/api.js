import axios from "axios";

// Production Render backend
// VITE_API_BASE_URL can override this when configured in Vercel.
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "https://voice-rag-2rq5.onrender.com";

const api = axios.create({
  baseURL: API_BASE_URL,
});

// ============================================================
// UPLOAD VOICE / AUDIO KNOWLEDGE
// ============================================================

export const ingestVoice = async (audioFile) => {
  const formData = new FormData();

  formData.append("file", audioFile);

  const response = await api.post(
    "/api/voice/ingest",
    formData
  );

  return response.data;
};

// ============================================================
// ASK QUESTION USING RAG
// ============================================================

export const askQuestion = async (question) => {
  const response = await api.post(
    "/api/chat",
    {
      question: question,
    }
  );

  return response.data;
};

export default api;
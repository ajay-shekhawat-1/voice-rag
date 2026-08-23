import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Upload voice/audio knowledge
export const ingestVoice = async (audioFile) => {
  const formData = new FormData();

  formData.append("file", audioFile);

  const response = await api.post(
    "/api/voice/ingest",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

// Ask a question using RAG
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
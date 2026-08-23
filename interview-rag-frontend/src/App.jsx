import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [page, setPage] = useState("knowledge");

  return (
    <div className="vr-app">

      <aside className="vr-sidebar">

        <div className="vr-logo">
          <div className="vr-logo-mark">
            <span>V</span>
          </div>

          <div>
            <div className="vr-logo-name">
              Voice<span>RAG</span>
            </div>

            <div className="vr-logo-sub">
              AI KNOWLEDGE
            </div>
          </div>
        </div>

        <div className="vr-nav-title">
          WORKSPACE
        </div>

        <nav className="vr-nav">

          <button
            className={`vr-nav-item ${
              page === "knowledge" ? "selected" : ""
            }`}
            onClick={() => setPage("knowledge")}
          >
            <span className="vr-nav-icon">▣</span>
            <span>Knowledge</span>
          </button>

          <button
            className={`vr-nav-item ${
              page === "assistant" ? "selected" : ""
            }`}
            onClick={() => setPage("assistant")}
          >
            <span className="vr-nav-icon">✦</span>
            <span>AI Assistant</span>
          </button>

        </nav>

        <div className="vr-sidebar-bottom">

          <div className="vr-connection">

            <div className="vr-connection-dot"></div>

            <div>
              <strong>All systems operational</strong>
              <span>Backend connected</span>
            </div>

          </div>

          <div className="vr-sidebar-footer">
            Voice RAG <span>•</span> v1.0
          </div>

        </div>

      </aside>

      <main className="vr-main">

        <header className="vr-header">

          <div>
            <div className="vr-breadcrumb">
              WORKSPACE <span>/</span>{" "}
              {page === "knowledge"
                ? "KNOWLEDGE"
                : "AI ASSISTANT"}
            </div>

            <h1>
              {page === "knowledge"
                ? "Knowledge workspace"
                : "AI knowledge assistant"}
            </h1>
          </div>

          <div className="vr-header-status">
            <span></span>
            AI READY
          </div>

        </header>

        {page === "knowledge" ? (
          <KnowledgePage />
        ) : (
          <AssistantPage />
        )}

      </main>

    </div>
  );
}


/* =========================================================
   KNOWLEDGE PAGE
========================================================= */

function KnowledgePage() {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const selectFile = (selectedFile) => {
    if (!selectedFile) return;

    const allowed = [
      "audio/mpeg",
      "audio/wav",
      "audio/x-wav",
      "audio/mp4",
      "audio/webm",
      "audio/x-m4a",
    ];

    const extension = selectedFile.name
      .split(".")
      .pop()
      .toLowerCase();

    if (
      !allowed.includes(selectedFile.type) &&
      !["mp3", "wav", "m4a", "webm"].includes(extension)
    ) {
      setError(
        "Unsupported audio format. Use MP3, WAV, M4A or WEBM."
      );
      return;
    }

    setError("");
    setResult(null);
    setFile(selectedFile);
  };

  const uploadFile = async () => {
    if (!file) {
      setError("Please select an audio file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/voice/ingest`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to process audio."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the Voice RAG backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="vr-page">

      <section className="vr-intro">

        <div>
          <div className="vr-section-label">
            KNOWLEDGE INGESTION
          </div>

          <h2>
            Build your AI knowledge base
          </h2>

          <p>
            Upload a voice recording and transform it into
            searchable semantic knowledge.
          </p>
        </div>

        <div className="vr-engine-pill">
          <span className="pulse"></span>
          WHISPER + QDRANT
        </div>

      </section>


      <section className="vr-upload-layout">

        <div
          className={`vr-dropzone ${
            dragging ? "dragging" : ""
          } ${file ? "has-file" : ""}`}
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragging(false);
            selectFile(e.dataTransfer.files[0]);
          }}
          onClick={() =>
            document.getElementById("audio-input").click()
          }
        >

          <input
            id="audio-input"
            type="file"
            accept=".mp3,.wav,.m4a,.webm,audio/*"
            hidden
            onChange={(e) =>
              selectFile(e.target.files[0])
            }
          />

          {!file ? (
            <>
              <div className="vr-upload-icon">
                ↑
              </div>

              <h3>
                Drop your voice recording here
              </h3>

              <p>
                or click to browse your computer
              </p>

              <div className="vr-file-types">
                MP3 <span>•</span> WAV <span>•</span> M4A
                <span>•</span> WEBM
              </div>
            </>
          ) : (
            <div className="vr-selected-file">

              <div className="vr-audio-icon">
                ♪
              </div>

              <div className="vr-file-info">

                <strong>
                  {file.name}
                </strong>

                <span>
                  {formatFileSize(file.size)}
                </span>

              </div>

              <button
                className="vr-remove"
                onClick={(e) => {
                  e.stopPropagation();
                  setFile(null);
                  setResult(null);
                }}
              >
                ×
              </button>

            </div>
          )}

        </div>


        <div className="vr-process-card">

          <div className="vr-card-header">
            <div>
              <div className="vr-card-label">
                PROCESSING PIPELINE
              </div>

              <h3>
                From voice to knowledge
              </h3>
            </div>

            <div className="vr-ai-symbol">
              ✦
            </div>
          </div>

          <div className="vr-pipeline">

            <PipelineStep
              number="01"
              title="Speech recognition"
              description="Whisper transcription"
            />

            <PipelineLine />

            <PipelineStep
              number="02"
              title="Semantic chunking"
              description="Context preservation"
            />

            <PipelineLine />

            <PipelineStep
              number="03"
              title="Vector embedding"
              description="AI representation"
            />

            <PipelineLine />

            <PipelineStep
              number="04"
              title="Knowledge storage"
              description="Qdrant vector DB"
            />

          </div>

          <button
            className="vr-primary-button"
            disabled={!file || loading}
            onClick={uploadFile}
          >
            {loading ? (
              <>
                <span className="vr-spinner"></span>
                Processing knowledge...
              </>
            ) : (
              <>
                Process voice knowledge
                <span>→</span>
              </>
            )}
          </button>

        </div>

      </section>


      {error && (
        <div className="vr-alert error">
          <strong>Processing failed</strong>
          <span>{error}</span>
        </div>
      )}


      {result && (
        <div className="vr-success">

          <div className="vr-success-top">

            <div className="vr-success-check">
              ✓
            </div>

            <div>
              <strong>
                Knowledge successfully added
              </strong>

              <span>
                Your voice recording is now searchable.
              </span>
            </div>

          </div>

          <div className="vr-metrics">

            <Metric
              label="Characters"
              value={result.characters ?? 0}
            />

            <Metric
              label="Chunks"
              value={result.chunks ?? 0}
            />

            <Metric
              label="Vectors stored"
              value={result.vectors_stored ?? 0}
            />

            <Metric
              label="Source"
              value={result.source_name || file?.name}
            />

          </div>

        </div>
      )}

    </div>
  );
}


/* =========================================================
   ASSISTANT PAGE
========================================================= */

function AssistantPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to generate answer."
        );
      }

      setAnswer(
        data.answer ||
          data.response ||
          data.message ||
          "No answer returned."
      );
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const speakAnswer = () => {
    if (!answer) return;

    window.speechSynthesis.cancel();

    const speech =
      new SpeechSynthesisUtterance(answer);

    speech.rate = 0.95;
    speech.pitch = 1;

    window.speechSynthesis.speak(speech);
  };

  return (
    <div className="vr-page">

      <section className="vr-intro">

        <div>
          <div className="vr-section-label">
            AI KNOWLEDGE ASSISTANT
          </div>

          <h2>
            Ask your knowledge anything
          </h2>

          <p>
            Ask questions about the voice recordings
            stored in your vector knowledge base.
          </p>
        </div>

        <div className="vr-engine-pill">
          <span className="pulse"></span>
          GROQ + QDRANT
        </div>

      </section>


      <section className="vr-chat-card">

        <div className="vr-chat-header">

          <div className="vr-chat-avatar">
            ✦
          </div>

          <div>
            <strong>
              Voice RAG Assistant
            </strong>

            <span>
              Grounded in your private knowledge
            </span>
          </div>

          <div className="vr-chat-online">
            <span></span>
            ONLINE
          </div>

        </div>


        <div className="vr-chat-body">

          {!answer && !loading && (
            <div className="vr-empty-chat">

              <div className="vr-empty-orb">
                ✦
              </div>

              <h3>
                What would you like to know?
              </h3>

              <p>
                Ask a question and I'll search your
                uploaded voice knowledge.
              </p>

              <div className="vr-suggestions">

                <button
                  onClick={() =>
                    setQuestion(
                      "What are the main topics discussed?"
                    )
                  }
                >
                  What are the main topics?
                </button>

                <button
                  onClick={() =>
                    setQuestion(
                      "Give me a summary of the knowledge."
                    )
                  }
                >
                  Give me a summary
                </button>

              </div>

            </div>
          )}


          {loading && (
            <div className="vr-loading-answer">

              <div className="vr-thinking">
                <span></span>
                <span></span>
                <span></span>
              </div>

              <strong>
                Searching your knowledge...
              </strong>

              <p>
                Retrieving relevant context from Qdrant
              </p>

            </div>
          )}


          {answer && !loading && (
            <div className="vr-answer">

              <div className="vr-answer-label">
                <span>✦</span>
                AI RESPONSE
              </div>

              <p>
                {answer}
              </p>

              <div className="vr-answer-actions">

                <button onClick={speakAnswer}>
                  🔊 Listen
                </button>

                <button
                  onClick={() =>
                    navigator.clipboard.writeText(answer)
                  }
                >
                  Copy
                </button>

                <button
                  onClick={() => setAnswer("")}
                >
                  New question
                </button>

              </div>

            </div>
          )}

        </div>


        {error && (
          <div className="vr-alert error">
            {error}
          </div>
        )}


        <div className="vr-question-area">

          <textarea
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            onKeyDown={(e) => {
              if (
                e.key === "Enter" &&
                !e.shiftKey
              ) {
                e.preventDefault();
                askQuestion();
              }
            }}
            placeholder="Ask something about your voice knowledge..."
          />

          <div className="vr-question-footer">

            <span>
              Enter to ask • Shift + Enter for new line
            </span>

            <button
              className="vr-send-button"
              disabled={
                !question.trim() || loading
              }
              onClick={askQuestion}
            >
              {loading ? "..." : "Ask AI →"}
            </button>

          </div>

        </div>

      </section>

    </div>
  );
}


/* =========================================================
   COMPONENTS
========================================================= */

function PipelineStep({
  number,
  title,
  description,
}) {
  return (
    <div className="vr-pipeline-step">

      <div className="vr-pipeline-number">
        {number}
      </div>

      <div>
        <strong>{title}</strong>
        <span>{description}</span>
      </div>

    </div>
  );
}


function PipelineLine() {
  return (
    <div className="vr-pipeline-line">
      ↓
    </div>
  );
}


function Metric({ label, value }) {
  return (
    <div className="vr-metric">

      <span>{label}</span>

      <strong>
        {value}
      </strong>

    </div>
  );
}


function formatFileSize(bytes) {
  if (!bytes) return "0 KB";

  const mb = bytes / (1024 * 1024);

  if (mb >= 1) {
    return `${mb.toFixed(2)} MB`;
  }

  return `${Math.round(bytes / 1024)} KB`;
}


export default App;
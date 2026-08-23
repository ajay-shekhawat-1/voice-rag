import { useState } from "react";
import { askQuestion } from "../services/api";

function AskQuestion() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAsk = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const data = await askQuestion(
        question.trim()
      );

      console.log("RAG response:", data);

      /*
       * We will inspect the exact response structure
       * from your backend if necessary.
       */

      setAnswer(
        data.answer ||
        data.response ||
        data.message ||
        "No answer was returned."
      );
    } catch (err) {
      console.error("Question error:", err);

      const message =
        err.response?.data?.detail ||
        "Failed to generate answer.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Ask Your Knowledge</h2>

      <p className="description">
        Ask a question about the voice knowledge
        stored in your vector database.
      </p>

      <textarea
        value={question}
        onChange={(event) =>
          setQuestion(event.target.value)
        }
        placeholder="Ask something about your uploaded audio..."
        rows={5}
      />

      <button
        onClick={handleAsk}
        disabled={loading}
      >
        {loading
          ? "Generating Answer..."
          : "Ask Question"}
      </button>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {answer && (
        <div className="answer">
          <h3>Answer</h3>

          <p>{answer}</p>
        </div>
      )}
    </section>
  );
}

export default AskQuestion;
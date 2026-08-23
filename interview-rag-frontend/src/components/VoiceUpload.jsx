import { useState } from "react";
import { ingestVoice } from "../services/api";

function VoiceUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setFile(selectedFile || null);
    setResult(null);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an audio file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await ingestVoice(file);

      setResult(data);
    } catch (err) {
      console.error(err);

      const message =
        err.response?.data?.detail ||
        "Failed to process voice data.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Voice Knowledge Ingestion</h2>

      <p className="description">
        Upload audio to convert speech into searchable
        knowledge.
      </p>

      <input
        type="file"
        accept=".mp3,.wav,.m4a,.webm,audio/*"
        onChange={handleFileChange}
      />

      {file && (
        <p className="selected-file">
          Selected: {file.name}
        </p>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || loading}
      >
        {loading ? "Processing..." : "Upload & Process"}
      </button>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {result && (
        <div className="result">
          <h3>
            {result.duplicate
              ? "Already Ingested"
              : "Processing Complete"}
          </h3>

          <p>
            <strong>Source:</strong>{" "}
            {result.source_name}
          </p>

          <p>
            <strong>Characters:</strong>{" "}
            {result.characters}
          </p>

          <p>
            <strong>Chunks:</strong>{" "}
            {result.chunks}
          </p>

          <p>
            <strong>Vectors Stored:</strong>{" "}
            {result.vectors_stored}
          </p>

          <p>{result.message}</p>
        </div>
      )}
    </section>
  );
}

export default VoiceUpload;
import { useState } from "react";
import { uploadDocument } from "../api/upload";
import type { ExtractedData } from "../types/extracted";

type Props = {
  onDataExtracted: (data: ExtractedData) => void;
};

export default function FileUpload({ onDataExtracted }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) return;

    try {
      setLoading(true);
      setError(null);

      const result = await uploadDocument(file);
      onDataExtracted(result); // ✅ send data to Home

    } catch {
      setError("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />

      <button onClick={handleUpload} disabled={!file || loading}>
        {loading ? "Processing..." : "Upload"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

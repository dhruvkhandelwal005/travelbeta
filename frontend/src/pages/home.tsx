import { useState } from "react";
import { logout } from "../components/auth";
import FileUpload from "../components/FileUpload";
import type { ExtractedData } from "../types/extracted";

export default function Home() {
  const [data, setData] = useState<ExtractedData | null>(null);
  const user_email=localStorage.getItem("user_email");

  return (
    <>
    <h3>{user_email}</h3>
      <FileUpload onDataExtracted={setData} />

      <button onClick={logout}>Logout</button>

      {data && (
        <div style={{ padding: "2rem" }}>
          <h2>Extracted Data</h2>

          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </>
  );
}

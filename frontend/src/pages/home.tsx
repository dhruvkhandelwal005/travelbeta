import { useState, useEffect} from "react";
import { logout } from "../components/auth";
import FileUpload from "../components/FileUpload";
import type { ExtractedData } from "../types/extracted";

export default function Home() {
        useEffect(() => {
  const email = localStorage.getItem("user_email");
  if (!email) return;

  const cached = localStorage.getItem(`ticket`);
  if (cached) {
    setData(JSON.parse(cached));
  }
}, []);




  const [data, setData] = useState<ExtractedData | null>(null);
  const user_email=localStorage.getItem("user_email")||"";
  const REQUIRED_FIELD_COUNT = 7;

  function isValidTicket(data: ExtractedData): boolean {
           const values = Object.values(data);
            const nonNullCount = values.filter(v => v !== null && v !== "").length;
      return nonNullCount >= REQUIRED_FIELD_COUNT;
    } 

      function saveTicketLocally(ticket: any) {
  localStorage.setItem(
    `ticket`,
    JSON.stringify(ticket)
  );
}
async function saveTicketToBackend(ticket: any) {
  await fetch("http://localhost:8000/tickets", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ticket)
  });
}

const handleExtractedData = async (data: ExtractedData) => {
  if (!isValidTicket(data)) return;

  saveTicketLocally(data);
  await saveTicketToBackend(data);

  setData(data);
};
     function remove_ticket(){
      localStorage.removeItem("ticket");
      window.location.href = "/home"
    }





  return (
    <>
    <h3>{user_email}</h3>
      <FileUpload onDataExtracted={handleExtractedData} />

      <button onClick={logout}>Logout</button>
      <button onClick={remove_ticket}>Remove ticket</button>

      {data && (
        <div style={{ padding: "2rem" }}>
          <h2>Extracted Data</h2>

          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </>
  );
}

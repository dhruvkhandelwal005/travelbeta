import { useState, useEffect} from "react";
import { logout } from "../components/api";
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


   const [matches, setMatches] = useState<any[]>([]);
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

    async function find_matches (){
      if(data){
      const res = await fetch("http://localhost:8000/matches", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
    res.json().then(setMatches);
      } else{
        alert("No ticket uploaded");
      }
    }



  return (
    <>
    <h3>{user_email}</h3>
      <FileUpload onDataExtracted={handleExtractedData} />

      <button onClick={logout}>Logout</button>
      <button onClick={remove_ticket}>Remove ticket</button>
      <button onClick={find_matches}>Find TravelMates</button>

      {data && (
        <div style={{ padding: "2rem" }}>
          <h2>Extracted Data</h2>

          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
     
 <div style={{ padding: "2rem" }}>
      <h2>Travel Matches</h2>

      {matches.length === 0 && <p>No matches</p>}

      {matches.map((m, i) => (
        <div key={i} style={{ border: "1px solid #ccc", padding: "1rem", marginBottom: "1rem" }}>
          <p><b>Score:</b> {m.score}</p>
          <p><b>Category:</b> {m.category}</p>
          <p> {m.ticket.name}</p>
          <p> {m.ticket.date}</p>
          <p> {m.ticket.source}</p>
          <p> {m.ticket.destination}</p>
          <p> {m.ticket.vehicle_name}</p>
          <p> {m.ticket.vehicle_type}</p>
          <p> {m.ticket.departure_time}</p>
          <p> {m.ticket.arrival_time}</p>
          <p> {m.ticket.travel_class}</p>
        </div>
      ))}
    </div>


    </>
  );
}

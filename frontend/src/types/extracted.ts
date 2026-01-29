export interface ExtractedData {
  name: string | null;
  source: string | null;
  destination: string | null;
  date: string | null; // YYYY-MM-DD
  departure_time: string | null; // HH:MM
  arrival_time: string | null; // HH:MM
  vehicle_type: "train" | "flight" | "bus" | null;
  vehicle_name: string | null;
  travel_class: string | null;
}

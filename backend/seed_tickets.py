import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")

client = MongoClient(MONGO_URI)

# CHANGE DB NAME ONLY IF YOUR PROJECT USES A DIFFERENT ONE
db = client["travel"]
tickets = db["tickets"]

# Optional: clear existing tickets (comment if not needed)
tickets.delete_many({})

dummy_tickets = [
    # 🔥 PERFECT / SAME JOURNEY
    {
        "name": "Rakesh Kumar",
        "source": "JAISALMER (JSM)",
        "destination": "SABARMATI BG (SBIB)",
        "date": "2023-05-15",
        "departure_time": "15:10",
        "arrival_time": "05:30",
        "vehicle_type": "train",
        "vehicle_name": "14803/JSM SBIB EXP",
        "travel_class": "THIRD AC (3A)"
    },

    # 🔥 VERY SIMILAR (10 min diff)
    {
        "name": "Amit Shah",
        "source": "JAISALMER (JSM)",
        "destination": "SABARMATI BG (SBIB)",
        "date": "2023-05-15",
        "departure_time": "15:20",
        "arrival_time": "05:40",
        "vehicle_type": "train",
        "vehicle_name": "14803/JSM SBIB EXP",
        "travel_class": "THIRD AC (3A)"
    },

    # 🟡 POSSIBLE TRAVEL MATE (same train, different class)
    {
        "name": "Neha Verma",
        "source": "JAISALMER (JSM)",
        "destination": "SABARMATI BG (SBIB)",
        "date": "2023-05-15",
        "departure_time": "15:05",
        "arrival_time": "05:25",
        "vehicle_type": "train",
        "vehicle_name": "14803/JSM SBIB EXP",
        "travel_class": "SLEEPER (SL)"
    },

    # 🟡 POSSIBLE (different train, same time range)
    {
        "name": "Kunal Mehta",
        "source": "JAISALMER (JSM)",
        "destination": "SABARMATI BG (SBIB)",
        "date": "2023-05-15",
        "departure_time": "16:00",
        "arrival_time": "06:00",
        "vehicle_type": "train",
        "vehicle_name": "22931/BKN SBIB SF EXP",
        "travel_class": "THIRD AC (3A)"
    },

    # ❌ FILTERED OUT (different date)
    {
        "name": "Ignored Date",
        "source": "JAISALMER (JSM)",
        "destination": "SABARMATI BG (SBIB)",
        "date": "2023-05-16",
        "departure_time": "15:10",
        "arrival_time": "05:30",
        "vehicle_type": "train",
        "vehicle_name": "14803/JSM SBIB EXP",
        "travel_class": "THIRD AC (3A)"
    },

    # ❌ FILTERED OUT (different source)
    {
        "name": "Ignored Source",
        "source": "JODHPUR (JU)",
        "destination": "SABARMATI BG (SBIB)",
        "date": "2023-05-15",
        "departure_time": "15:10",
        "arrival_time": "05:30",
        "vehicle_type": "train",
        "vehicle_name": "14803/JSM SBIB EXP",
        "travel_class": "THIRD AC (3A)"
    },

    # ❌ FILTERED OUT (different destination)
    {
        "name": "Ignored Destination",
        "source": "JAISALMER (JSM)",
        "destination": "AHMEDABAD JN (ADI)",
        "date": "2023-05-15",
        "departure_time": "15:10",
        "arrival_time": "05:30",
        "vehicle_type": "train",
        "vehicle_name": "14803/JSM SBIB EXP",
        "travel_class": "THIRD AC (3A)"
    }
]


tickets.insert_many(dummy_tickets)

print(f"✅ Inserted {len(dummy_tickets)} dummy tickets into Atlas")

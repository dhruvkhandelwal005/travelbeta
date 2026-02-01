from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.extractor import extract_text
from services.llm import process_with_llm
from database import db
from schema.schemas import SignupSchema, LoginSchema, Ticket 
from auth import hash_password, verify_password
from utils.jwt_utils import create_access_token
from pymongo import MongoClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = db.users
tickets_collection = db.tickets

@app.on_event("startup")
def create_indexes():
    db.tickets.create_index(
        [
            ("name", 1),
            ("source", 1),
            ("destination", 1),
            ("date", 1),
            ("departure_time", 1),
            ("vehicle_name", 1),
            ("travel_class", 1),
        ],
        unique=True
    )



@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        text = await extract_text(file)
        result = process_with_llm(text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/signup")
def signup(user: SignupSchema):
    existing = users.find_one({"email": user.email})
    
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    users.insert_one({
        "email": user.email,
        "password": hash_password(user.password)
    })

    return {"message": "User created successfully"}

@app.post("/login")
def login(data: LoginSchema):
    user = users.find_one({"email": data.email})

    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": str(user["_id"]),
        "email": user["email"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_email":data.email,
    }


@app.post("/tickets")
def save_ticket(ticket: Ticket):
    ticket_data = ticket.dict(exclude_none=True)

    existing = db.tickets.find_one(ticket_data)
    if existing:
        return {"status": "already_exists"}

    db.tickets.insert_one(ticket_data)
    return {"status": "saved"}


















def time_to_minutes(t):
    if not t:
        return None
    h, m = map(int, t.split(":"))
    return h * 60 + m


def calculate_score(base, other):
    score = 0

    if base.get("vehicle_name") == other.get("vehicle_name"):
        score += 40

    if base.get("vehicle_type") == other.get("vehicle_type"):
        score += 15

    bd = time_to_minutes(base.get("departure_time"))
    od = time_to_minutes(other.get("departure_time"))

    if bd is not None and od is not None:
        diff = abs(bd - od)
        if diff <= 15:
            score += 25
        elif diff <= 30:
            score += 20
        elif diff <= 60:
            score += 10
        elif diff <= 120:
            score += 5

    ba = time_to_minutes(base.get("arrival_time"))
    oa = time_to_minutes(other.get("arrival_time"))

    if ba is not None and oa is not None:
        diff = abs(ba - oa)
        if diff <= 30:
            score += 10
        elif diff <= 60:
            score += 5

    if base.get("travel_class") == other.get("travel_class"):
        score += 10

    return score

def category(score):
    if score >= 80:
        return "Same Journey"
    if score >= 60:
        return "Very Similar"
    return "Possible Travel Mate"

def find_matches(current_ticket: dict):
    results = []

    # fetch tickets from DB (cursor)
    all_tickets = tickets_collection.find()

    for t in all_tickets:

        # ❌ skip same journey (basic equality check)
        if (
            t.get("name") == current_ticket.get("name") and
            t.get("source") == current_ticket.get("source") and
            t.get("destination") == current_ticket.get("destination") and
            t.get("date") == current_ticket.get("date") and
            t.get("departure_time") == current_ticket.get("departure_time")
        ):
            continue

        score = calculate_score(current_ticket, t)


        results.append({
            "score": score,
            "category": category(score),
            "ticket": {
                "name": t.get("name"),
                "source": t.get("source"),
                "destination": t.get("destination"),
                "vehicle_name": t.get("vehicle_name"),
                "vehicle_type": t.get("vehicle_type"),
                "departure_time": t.get("departure_time"),
                "arrival_time": t.get("arrival_time"),
                "travel_class": t.get("travel_class"),
                "date": t.get("date"),
            }
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results




@app.post("/matches")
def get_matches(ticket: Ticket):
    return find_matches(ticket.dict())

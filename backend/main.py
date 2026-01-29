from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.extractor import extract_text
from services.llm import process_with_llm
from database import db
from schema.schemas import SignupSchema, LoginSchema
from auth import hash_password, verify_password
from utils.jwt_utils import create_access_token
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = db.users

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

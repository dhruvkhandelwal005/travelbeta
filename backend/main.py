from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.extractor import extract_text
from services.llm import process_with_llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

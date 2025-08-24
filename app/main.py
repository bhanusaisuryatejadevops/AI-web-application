
from fastapi import FastAPI
import requests
import os

app = FastAPI()

TEXT_API_URL = os.getenv("TEXT_API_URL", "http://text-processing.com/api/sentiment/")
EXTERNAL_API_TIMEOUT = int(os.getenv("EXTERNAL_API_TIMEOUT", 10))

@app.get("/")
def root():
    return {"message": "AI App is running!"}

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}

@app.post("/analyze")
def analyze_text(text: str):
    try:
        response = requests.post(TEXT_API_URL, data={"text": text}, timeout=EXTERNAL_API_TIMEOUT)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


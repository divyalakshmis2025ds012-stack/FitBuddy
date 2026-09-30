"""
main.py
FastAPI entry point. Run with:
    uvicorn app.main:app --reload
Then visit http://127.0.0.1:8000  (and http://127.0.0.1:8000/docs for the API).
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.database import init_db
from app.routes import router

load_dotenv()  # loads GOOGLE_API_KEY from .env

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

init_db()

app.include_router(router)

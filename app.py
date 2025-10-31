# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from weather_engine import summarize
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Weather API", version="1.0")

# CORS so your frontend (React/Next.js) can access it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for dev; restrict to your domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weather")
def get_weather(city: str):
    try:
        return summarize(city)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

import os
import sys
import uvicorn as uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import initialize_database
from routes import letalo, pilot, polet

app = FastAPI()

allowed_origins = [
    "https://rirs-evidencaletenjaprojekt-3.onrender.com",  # Deployed frontend
    "http://localhost",  # Localhost without port
    "http://localhost:5173",  # React dev server or similar
    "http://127.0.0.1",  # Localhost with IP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

initialize_database()

app.include_router(polet.router)
app.include_router(letalo.router)
app.include_router(pilot.router)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


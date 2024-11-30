import uvicorn as uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from core.database import initialize_database
from tests.testna_baza_setup import test_db
from routes import letalo, pilot, polet
from fastapi.testclient import TestClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add your frontend origin here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

initialize_database()
#test_db()

app.include_router(polet.router)
app.include_router(letalo.router)
app.include_router(pilot.router)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
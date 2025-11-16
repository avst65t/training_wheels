# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as contract_router
import os
import uvicorn

app = FastAPI(title="Contract Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("contracts", exist_ok=True)
app.include_router(contract_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

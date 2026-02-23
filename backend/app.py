from fastapi import FastAPI
import json

app = FastAPI()

def load_data(file):
    with open(f"../data/{file}.json") as f:
        return json.load(f)

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/planets")
def get_planets():
    return load_data("planets")

@app.get("/characters")
def get_characters():
    return load_data("characters")

@app.get("/films")
def get_films():
    return load_data("films")

@app.get("/coordinates")
def get_coordinates():
    return load_data("coordinates")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
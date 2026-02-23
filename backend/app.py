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

from graph_engine import find_shortest_path, top_characters

@app.get("/graph/path")
def graph_path(source: str, target: str):
    return {"path": find_shortest_path(source, target)}

@app.get("/graph/top-characters")
def graph_top():
    return {"top": top_characters()}

from semantic_engine import semantic_search

@app.get("/search")
def search(query: str):
    return {"results": semantic_search(query)}
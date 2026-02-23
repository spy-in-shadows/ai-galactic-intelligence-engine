import json
import networkx as nx

DATA_DIR = "../data"

with open(f"{DATA_DIR}/planets.json") as f:
    planets = json.load(f)

with open(f"{DATA_DIR}/characters.json") as f:
    characters = json.load(f)

with open(f"{DATA_DIR}/films.json") as f:
    films = json.load(f)

G = nx.Graph()

# Add planet nodes
for planet in planets:
    G.add_node(planet["name"], type="planet")

# Add character nodes
for char in characters:
    G.add_node(char["name"], type="character")

# Add film nodes
for film in films:
    G.add_node(film["title"], type="film")

# Connect characters to planets (homeworld)
for char in characters:
    homeworld_url = char["homeworld"]
    for planet in planets:
        if planet["url"] == homeworld_url:
            G.add_edge(char["name"], planet["name"])

# Connect characters to films
for char in characters:
    for film_url in char["films"]:
        for film in films:
            if film["url"] == film_url:
                G.add_edge(char["name"], film["title"])

def find_shortest_path(source, target):
    try:
        return nx.shortest_path(G, source=source, target=target)
    except:
        return []

def top_characters(n=5):
    centrality = nx.degree_centrality(G)
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    return sorted_nodes[:n]
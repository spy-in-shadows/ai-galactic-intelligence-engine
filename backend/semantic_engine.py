import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

DATA_DIR = "../data"

with open(f"{DATA_DIR}/planets.json") as f:
    planets = json.load(f)

# Create textual descriptions for planets
planet_texts = []
planet_names = []

climate_map = {
    "arid": "desert dry sandy",
    "frozen": "ice snowy cold",
    "hot": "heat lava warm",
    "tropical": "jungle forest humid",
    "murky": "swamp wet dark",
}

for planet in planets:
    extra_keywords = ""
    for key, value in climate_map.items():
        if key in planet['climate']:
            extra_keywords += " " + value
    
    description = f"""
    Name: {planet['name']}.
    Climate: {planet['climate']}.
    Terrain: {planet['terrain']}.
    Population: {planet['population']}.
    Keywords: {extra_keywords}.
    """
    planet_texts.append(description)
    planet_names.append(planet["name"])

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(planet_texts)

# Convert to float32
embeddings = np.array(embeddings).astype("float32")

# Normalize embeddings for cosine similarity
faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # Inner product = cosine similarity after normalization
index.add(embeddings)

def semantic_search(query, k=3):
    query_lower = query.lower()

    query_embedding = model.encode([query]).astype("float32")
    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, len(planet_names))

    scored_results = []

    for rank, idx in enumerate(indices[0]):
        planet_name = planet_names[idx]
        base_score = distances[0][rank]

        bonus = 0

        # Keyword boosting
        if "desert" in query_lower:
            if "arid" in planets[idx]["climate"].lower():
                bonus += 0.3

        if "forest" in query_lower:
            if "forest" in planets[idx]["terrain"].lower():
                bonus += 0.3

        if "ice" in query_lower or "frozen" in query_lower:
            if "frozen" in planets[idx]["climate"].lower():
                bonus += 0.3
        
        if "population" in query_lower or "huge" in query_lower or "large" in query_lower:
            try:
                pop = planets[idx]["population"]
                if pop.isdigit():
                    pop_value = int(pop)
                    bonus += min(pop_value / 1_000_000_000, 0.5)  # boost big populations
            except:
                pass
        
        if "city" in query_lower:
            if "city" in planets[idx]["terrain"].lower():
                bonus += 0.5
        
        if "lava" in query_lower or "volcanic" in query_lower:
            terrain_string = planets[idx]["terrain"].lower()
            if "lava" in terrain_string or "volcano" in terrain_string:
                bonus += 0.6

        final_score = base_score + bonus

        scored_results.append((planet_name, final_score))

    # Sort by final_score descending
    scored_results.sort(key=lambda x: x[1], reverse=True)

    return [name for name, _ in scored_results[:k]]
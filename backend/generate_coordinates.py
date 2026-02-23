import json
import numpy as np
from sklearn.cluster import KMeans
import os
import random

DATA_DIR = "../data"

with open(f"{DATA_DIR}/planets.json") as f:
    planets = json.load(f)

num_planets = len(planets)

# Generate initial random 3D points
points = np.random.rand(num_planets, 3) * 100

# Cluster into 3 galactic regions
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(points)

coordinates = []

for i, planet in enumerate(planets):
    region = clusters[i]

    if region == 0:
        scale = 20  # Core
    elif region == 1:
        scale = 50  # Mid Rim
    else:
        scale = 90  # Outer Rim

    x, y, z = np.random.randn(3) * scale

    coordinates.append({
        "name": planet["name"],
        "x": float(x),
        "y": float(y),
        "z": float(z),
        "region": int(region)
    })

with open(f"{DATA_DIR}/coordinates.json", "w") as f:
    json.dump(coordinates, f, indent=4)

print("Coordinates generated.")
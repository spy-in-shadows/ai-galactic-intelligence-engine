import requests
import json
import os

BASE_URL = "https://swapi.dev/api"

DATA_DIR = "../data"

os.makedirs(DATA_DIR, exist_ok=True)

def fetch_all(endpoint):
    url = f"{BASE_URL}/{endpoint}/"
    results = []

    while url:
        response = requests.get(url)
        data = response.json()
        results.extend(data["results"])
        url = data["next"]

    return results


def save_data(name, data):
    with open(f"{DATA_DIR}/{name}.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    print("Fetching planets...")
    planets = fetch_all("planets")
    save_data("planets", planets)

    print("Fetching people...")
    people = fetch_all("people")
    save_data("characters", people)

    print("Fetching films...")
    films = fetch_all("films")
    save_data("films", films)

    print("Data fetch complete.")
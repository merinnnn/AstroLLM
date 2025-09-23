import os
import requests
import json
from dotenv import load_dotenv
from tqdm import tqdm
import random

load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

OUTPUT_DIR = "data"
OUTPUT_NAME = "astro_dataset.jsonl"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, OUTPUT_NAME)

def save_entry(file, instruction, context, answer):
    entry = {
        "instruction": instruction,
        "input": context,
        "output": answer
    }
    file.write(json.dumps(entry) + "\n")

# ---- Fetch functions ----
def fetch_apod(count=1000):
    """
    Fetch Astronomy Picture of the Day (APOD) entries.
    """
    url = f"https://api.nasa.gov/planetary/apod"
    params = {"api_key": NASA_API_KEY, "count": count}
    resp = requests.get(url, params=params).json()

    samples = []
    for item in resp:
        if "title" in item and "explanation" in item:
            samples.append({
                "question": f"What is '{item['title']}'?",
                "context": item.get("date", ""),
                "answer": item["explanation"]
            })
    return samples


def fetch_mars_rover_photos(total=1000):
    """
    Fetch Mars rover photos spread across random sols.
    """
    url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    samples = []
    sols = random.sample(range(0, 2000), 50)  # spread across sols

    for sol in sols:
        params = {"sol": sol, "api_key": NASA_API_KEY}
        resp = requests.get(url, params=params).json()
        photos = resp.get("photos", [])
        for p in photos[: total // len(sols)]:
            rover = p["rover"]["name"]
            camera = p["camera"]["full_name"]
            date = p["earth_date"]
            img_url = p["img_src"]
            samples.append({
                "question": f"What did the {rover} rover capture on {date}?",
                "context": f"Camera: {camera}, Sol: {sol}, Image: {img_url}",
                "answer": f"A photo taken by {rover}'s {camera} on {date}. URL: {img_url}"
            })
    return samples[:total]


def fetch_exoplanets(limit=1000):
    """
    Fetch exoplanet data from NASA Exoplanet Archive.
    """
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    query = f"select top {limit} pl_name,hostname,discoverymethod,disc_year,sy_dist from ps"
    params = {"query": query, "format": "json"}

    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("Exoplanet API request failed:", resp.text[:200])
        return []

    try:
        data = resp.json()
    except Exception:
        print("Failed to parse JSON. Response looked like:")
        print(resp.text[:200])
        return []

    samples = []
    for exo in data:
        name = exo.get("pl_name", "Unknown planet")
        host = exo.get("hostname", "Unknown star")
        method = exo.get("discoverymethod", "Unknown method")
        year = exo.get("disc_year", "Unknown year")
        dist = exo.get("sy_dist", "Unknown distance")

        samples.append({
            "question": f"What is {name}?",
            "context": f"Host star: {host}, Discovery method: {method}, Year: {year}, Distance: {dist} pc",
            "answer": f"{name} is an exoplanet discovered in {year} using {method}. "
                      f"It orbits {host} and is approximately {dist} parsecs away."
        })
    return samples


# ---- Main ----
if __name__ == "__main__":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        print("Fetching APOD data...")
        for s in tqdm(fetch_apod(1000)):
            save_entry(f, s["question"], s["context"], s["answer"])

        print("Fetching Mars Rover data...")
        for s in tqdm(fetch_mars_rover_photos(total=1000)):
            save_entry(f, s["question"], s["context"], s["answer"])

        print("Fetching Exoplanet data...")
        for s in tqdm(fetch_exoplanets(1000)):
            save_entry(f, s["question"], s["context"], s["answer"])

    print(f"\n✅ Dataset saved to {OUTPUT_FILE}")

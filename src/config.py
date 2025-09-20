from dotenv import load_dotenv
import os

# Explicit path
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / ".env"
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

NASA_API_KEY = os.getenv("NASA_API_KEY")
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if not NASA_API_KEY:
    raise ValueError("NASA_API_KEY not found in .env file")

if not HUGGING_FACE_TOKEN:
    raise ValueError("Hugging Face token not found in .env file")
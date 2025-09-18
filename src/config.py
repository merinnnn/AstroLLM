from dotenv import load_dotenv
import os

# Explicit path
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / ".env"
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

NASA_API_KEY = os.getenv("NASA_API_KEY")

if not NASA_API_KEY:
    raise ValueError("NASA_API_KEY not found in .env file")

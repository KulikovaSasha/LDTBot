import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")

if not TG_TOKEN:
    raise ValueError("TG_TOKEN is not set in .env file")
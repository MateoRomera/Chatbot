import os
from dotenv import load_dotenv

# Load variables from .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

POSTGRES_CONN = os.getenv("POSTGRES_CONN")

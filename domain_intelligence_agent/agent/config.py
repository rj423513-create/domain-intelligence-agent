import os
from dotenv import load_dotenv

# Load .env from root
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

BUILTWITH_API_KEY = os.getenv("BUILTWITH_API_KEY", "")
RATE_LIMIT_DELAY = int(os.getenv("RATE_LIMIT_DELAY", 2))

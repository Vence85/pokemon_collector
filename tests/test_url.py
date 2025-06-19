from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

print(urlparse(os.getenv("DATABASE_URL")))

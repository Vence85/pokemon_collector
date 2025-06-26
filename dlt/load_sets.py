import os
import sys
import requests
from postgrest.exceptions import APIError
from dotenv import load_dotenv
from supabase import create_client
load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

API_KEY = os.getenv("API_KEY")
SETS_URL = os.getenv("SETS_URL")
HEADERS = {"X-Api-key: API_KEY"} if API_KEY else {}

def get_all_sets():
    sets = []
    page, page_size = 1, 150
    while True:
        print(f"Hämtar sida{page} av set...")
        params= {"page": page, "page_size": page_size}

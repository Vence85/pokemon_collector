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
HEADERS  = {"X-Api-Key": API_KEY} if API_KEY else {}

def get_all_sets():
    sets = []
    page, page_size = 1, 150
    while True:
        print(f"Hämtar sida{page} av set...")
        params= {"page": page, "pageSize": page_size}
        resp = requests.get(SETS_URL, headers=HEADERS, params=params)
        data = resp.json().get("data", [])
        if not data:
            break
        sets.extend(data)
        page += 1

    print(f"Total {len(sets)} sets hämtades!")
    return sets

def save_sets_to_db(sets_list):
    sets_to_add = []
    for s in sets_list:
        sets_to_add.append({
            "id":            s["id"],
            "name":          s["name"],
            "series":        s.get("series"),
            "printed_total": s.get("printedTotal"),
            "total":         s.get("total"),
            "release_date":  s.get("releaseDate"),
            "cards_loaded":  False
        })
    
    try:
        resp = supabase.table("sets").insert(sets_to_add).execute()
        print(f"Infogade {len(resp.data or [])} set i databasen")
        
    except APIError as e:
        print(f"❌❌❌❌❌ Misslyckades att spara set ❌❌❌❌❌")


if __name__ == "__main__":
    # Kör allt i ett svep
    all_sets = get_all_sets()         # Hämta
    save_sets_to_db(all_sets)         # Spara

    
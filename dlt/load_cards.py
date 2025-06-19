import os
import sys
import requests
import psycopg2
from dotenv import load_dotenv
from supabase import create_client
load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

API_KEY = os.getenv("API_KEY")
CARDS_URL = os.getenv("CARDS_URL")

HEADERS = {"X-Api-Key": API_KEY} if API_KEY else {}

def get_cards_for_set(set_id):
    cards = []
    page = 1
    page_size = 250

    while True:
        print(f"Hämtar sida{page} för set {set_id}")
        params = {
            "q": f"set.id:{set_id}",
            "page": page,
            "pageSize": page_size
        }

        response = requests.get(CARDS_URL, headers = HEADERS, params=params)
        response.raise_for_status()
        data = response.json()["data"]

        if not data:
            break

        cards.extend(data)
        page += 1

    print(f"Totalt {len(cards)} kort hämtades för set {set_id}")
    return cards

def save_cards_to_db(cards, set_id):
    # För varje kort, bygg en dict med de kolumner du vill sätta
    to_insert = []
    for c in cards:
        small_img = c["images"].get("small")
        large_img = c["images"].get("large")

        if not small_img or not large_img:
            print(f"⚠️ Kort {c['id']} saknar bild, sparar ändå med None.")

        to_insert.append({
            "id":          c["id"],
            "name":        c["name"],
            "set_id":      set_id,
            "number":      c["number"],
            "rarity":      c.get("rarity"),
            "image_small": small_img,
            "image_large": large_img
        })

    # Batch-insertar alla kort
    resp = supabase.table("cards").insert(to_insert).execute()
    if resp.get("status_code") not in (200, 201):
        print("❌ Fel vid insert:", resp)
    else:
        print(f"💾 {len(cards)} kort skickades till Supabase via REST")

    # Markera setet som klart
    supabase.table("sets").update({"cards_loaded": True}).eq("id", set_id).execute()
    print(f"📌 Markerade cards_loaded=true för set {set_id}")


if __name__ == "__main__":
    # Heartbeat-prints för felsökning
    print("▶️  __main__-sektionen körs")
    if len(sys.argv) < 2:
        print("Användning: python dlt/load_cards.py <set_id>")
        sys.exit(1)

    set_id = sys.argv[1]
    print(f"▶️  Kommer att hämta set: {set_id}")

    cards = get_cards_for_set(set_id)
    save_cards_to_db(cards, set_id)


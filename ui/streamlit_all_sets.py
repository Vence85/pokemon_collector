import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
SUPA_URL = os.getenv("SUPABASE_URL")
SUPA_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPA_URL, SUPA_KEY)

st.set_page_config(
    page_title= "Pokémon-kort",
    layout="wide"
)

st.title("Pokémon-kort")
st.markdown("Välj ett set nedan för att se alla kort som ingår.")

def fetch_set():
    results =(
        supabase
        .table("sets")
        .select("id,name")
        .order("name")
        .execute()
    )
    return results.data or []

sets = fetch_set()
if not sets:
    st.error("Det setet finns tyvärr inte i databasen.")
    st.stop()

query = st.text_input("Sök efter ett set", "")
if query:
    filtered = [s for s in sets if query.lower() in s["name"].lower()]
else:
    filtered = sets

if not filtered:
    st.warning("Inga set matchade din sökning.")
    st.stop()
set_ids = [s["id"] for s in filtered]
set_names = {s["id"]: s["name"] for s in filtered}

selected = st.selectbox(
    "Välj set att visa kort från.",
    options=[""] + set_ids,
    format_func=lambda x: set_names.get(x, "---välj set---") 
)

if selected:
    @st.cache_data
    def fetch_cards(set_id):
        res = (
            supabase
            .table("cards")
            .select("number,name,image_small,rarity")
            .eq("set_id", set_id)
            .order("name")
            .execute()
        )
        return res.data or []

    cards = fetch_cards(selected)
    st.markdown(f"## {set_names[selected]} — {len(cards)} kort")

    cols_per_row = 5
    for i in range(0, len(cards), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, card in zip(cols, cards[i:i+cols_per_row]):
            with col:
                st.image(
                    card["image_small"],
                    caption=f"{card['number']}: {card['name']}\nRarity: {card.get('rarity','–')}",
                    use_container_width=True
                )

# --- Utrymme för framtida formulär att lägga till egna kort ---
st.markdown("---")
st.info("I kommande version kan du lägga till dina egna kort här och koppla dem mot ett set.")
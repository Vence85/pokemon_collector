import os
import sys
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.api import get_sets

st.title("Tillgängliga Pokémonsets")

sets = get_sets()

for index,s in enumerate(sets, start=1):
    st.write(f"{index}. **{s['name']}** ({s['id']}) – {s['releaseDate']}")


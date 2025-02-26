# ======================================================================
# File: requests.py
# Description: This file contains functions to make requests to the Jikan API.
# ======================================================================


import requests
import json
from rich.console import Console

console = Console()

# ----------------------------------------------------------------------
# Jikan API Functions
# ----------------------------------------------------------------------

def get_full_anime_info(mal_id: int) -> json:
    """Get full anime information from the Jikan API."""
    url = f"https://api.jikan.moe/v4/anime/{mal_id}"
    response = requests.get(url)
    return response.json()["data"]

def parse_anime_info(anime_info: json) -> dict:
    """Filter the anime information to only include the relevant fields."""
    return {
        "mal_id": anime_info["mal_id"],
        "title": anime_info["title"],
        "synopsis": anime_info["synopsis"],
        "episodes": anime_info["episodes"],
        "status": anime_info["status"],
        "aired_from": anime_info["aired"]["from"],
        "aired_to": anime_info["aired"]["to"],
        "broadcast": anime_info["broadcast"]["string"],
    }


if __name__ == "__main__":
    print(parse_anime_info(get_full_anime_info(1)))

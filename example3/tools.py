import json
from pathlib import Path

from strands import tool

ATTRACTIONS = {
    "Kyoto": ["Fushimi Inari", "Kiyomizu-dera", "Arashiyama"],
    "Osaka": ["Osaka Castle", "Dotonbori"],
}

HOURS = {
    "Fushimi Inari": "Always open",
    "Kiyomizu-dera": "6:00-18:00",
    "Arashiyama": "Always open",
    "Osaka Castle": "9:00-17:00",
    "Dotonbori": "Always open",
}


@tool
def list_attractions(city: str) -> list[str]:
    """Return a list of attractions for a city."""
    return ATTRACTIONS.get(city, [])


@tool
def read_attractions_file(city: str) -> list[dict]:
    """Return a list of attractions for a city from the JSON data file."""
    data_path = Path(__file__).parent / "solution" / "data.json"
    if not data_path.exists():
        return []

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    return data.get(city, [])


@tool
def get_hours(place: str) -> str:
    """Return hours for a place."""
    return HOURS.get(place, "Hours unavailable")

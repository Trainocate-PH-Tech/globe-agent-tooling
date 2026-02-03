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
def get_hours(place: str) -> str:
    """Return hours for a place."""
    return HOURS.get(place, "Hours unavailable")

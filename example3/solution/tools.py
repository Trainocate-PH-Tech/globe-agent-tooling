from pathlib import Path
from strands import tool

@tool
def read_attractions_file(city):
    data = Path(__file__).parent / "data.json"

    if not data.exists():
        return []

@tool
def get_hours(place):
    pass

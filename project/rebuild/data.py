import json
import os
from models import Item

DATA_FILE = "collectibles.json"
DEFAULT_CATEGORIES = ["Articles", "Videos", "Books", "Other"]


def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            raw = json.load(f)
            return [Item.from_dict(d) for d in raw]
    except (json.JSONDecodeError, IOError):
        print("Warning: data file is corrupted. Starting fresh.")
        return []


def save_items(items):
    with open(DATA_FILE, "w") as f:
        json.dump([item.to_dict() for item in items], f, indent=2)


def get_all_categories(items):
    cats = list(DEFAULT_CATEGORIES)
    for item in items:
        if item.category not in cats:
            cats.append(item.category)
    return cats

from datetime import date


class Item:
    def __init__(self, name, url, category, description="", favorite=False,
                 tags=None, date_added=None):
        self.name = name
        self.url = url
        self.category = category
        self.description = description
        self.favorite = favorite
        self.tags = tags or []
        self.date_added = date_added or date.today().isoformat()

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "category": self.category,
            "description": self.description,
            "favorite": self.favorite,
            "tags": self.tags,
            "date_added": self.date_added
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            url=data["url"],
            category=data["category"],
            description=data.get("description", ""),
            favorite=data.get("favorite", False),
            tags=data.get("tags", []),
            date_added=data.get("date_added", date.today().isoformat())
        )

    def favorite_icon(self):
        return "[★]" if self.favorite else "[ ]"

    def __str__(self):
        tags_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        return f"{self.favorite_icon()} {self.name}{tags_str} — {self.url}"

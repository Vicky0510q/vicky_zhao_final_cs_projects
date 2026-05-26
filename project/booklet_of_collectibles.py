import json
import os
import requests

DATA_FILE = "collectibles.json"
DEFAULT_CATEGORIES = ["Articles", "Videos", "Books", "Other"]


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: data file is corrupted. Starting fresh.")
        return []


def save_data(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=2)


def get_all_categories(items):
    cats = list(DEFAULT_CATEGORIES)
    for item in items:
        if item["category"] not in cats:
            cats.append(item["category"])
    return cats


def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code < 400:
            return True, ""
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "request timed out"
    except requests.exceptions.ConnectionError:
        return False, "could not connect to URL"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def print_item(item, index=None, show_category=False):
    fav = "[★]" if item["favorite"] else "[ ]"
    prefix = f"{index}. " if index is not None else ""
    cat = f" — {item['category']}" if show_category else ""
    print(f"{prefix}{fav} {item['name']}{cat} — {item['url']}")


def add_item(items):
    name = input("Item name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    url = input("URL: ").strip()
    ok, reason = check_url(url)
    if not ok:
        print(f"URL check failed: {reason}. Item not saved.")
        return

    categories = get_all_categories(items)
    print("Categories:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    print(f"  {len(categories) + 1}. New category")

    choice = input("Choose a category (number): ").strip()
    try:
        choice_num = int(choice)
    except ValueError:
        print("Invalid choice.")
        return

    if choice_num == len(categories) + 1:
        new_cat = input("New category name: ").strip()
        if not new_cat:
            print("Category name cannot be empty.")
            return
        category = new_cat
    elif 1 <= choice_num <= len(categories):
        category = categories[choice_num - 1]
    else:
        print("Invalid choice.")
        return

    description = input("Description (optional, press Enter to skip): ").strip()

    item = {
        "name": name,
        "url": url,
        "category": category,
        "description": description,
        "favorite": False
    }
    items.append(item)
    save_data(items)
    print(f"Added '{name}' under {category}.")


def view_categories(items):
    categories = get_all_categories(items)
    print("Categories:")
    for i, cat in enumerate(categories, 1):
        count = sum(1 for item in items if item["category"] == cat)
        print(f"  {i}. {cat} ({count} items)")

    choice = input("Choose a category (number): ").strip()
    try:
        choice_num = int(choice)
    except ValueError:
        print("Invalid choice.")
        return

    if not (1 <= choice_num <= len(categories)):
        print("Invalid choice.")
        return

    category = categories[choice_num - 1]
    cat_items = [item for item in items if item["category"] == category]

    print(f"\n--- {category} ---")
    if not cat_items:
        print("No items in this category.")
    else:
        for i, item in enumerate(cat_items, 1):
            print_item(item, index=i)


def search_items(items):
    keyword = input("Search keyword: ").strip().lower()
    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = []
    for item in items:
        if (keyword in item["name"].lower()
                or keyword in item["category"].lower()
                or keyword in item["description"].lower()):
            results.append(item)

    if not results:
        print("No items found.")
    else:
        print(f"Found {len(results)} results:")
        for i, item in enumerate(results, 1):
            print_item(item, index=i, show_category=True)


def mark_favorite(items):
    categories = get_all_categories(items)
    print("Categories:")
    for i, cat in enumerate(categories, 1):
        count = sum(1 for item in items if item["category"] == cat)
        print(f"  {i}. {cat} ({count} items)")

    choice = input("Choose a category (number): ").strip()
    try:
        choice_num = int(choice)
    except ValueError:
        print("Invalid choice.")
        return

    if not (1 <= choice_num <= len(categories)):
        print("Invalid choice.")
        return

    category = categories[choice_num - 1]
    cat_items = [item for item in items if item["category"] == category]

    if not cat_items:
        print("No items in this category.")
        return

    print(f"\n--- {category} ---")
    for i, item in enumerate(cat_items, 1):
        print_item(item, index=i)

    item_choice = input("Pick an item number to toggle favorite: ").strip()
    try:
        item_num = int(item_choice)
    except ValueError:
        print("Invalid choice.")
        return

    if not (1 <= item_num <= len(cat_items)):
        print("Invalid choice.")
        return

    target = cat_items[item_num - 1]
    target["favorite"] = not target["favorite"]
    save_data(items)

    if target["favorite"]:
        print(f"'{target['name']}' marked as favorite.")
    else:
        print(f"'{target['name']}' unmarked as favorite.")


def delete_item(items):
    if not items:
        print("No items to delete.")
        return

    print("All items:")
    for i, item in enumerate(items, 1):
        print_item(item, index=i, show_category=True)

    choice = input("Pick an item number to delete: ").strip()
    try:
        choice_num = int(choice)
    except ValueError:
        print("Invalid choice.")
        return

    if not (1 <= choice_num <= len(items)):
        print("Invalid choice.")
        return

    target = items[choice_num - 1]
    confirm = input(f"Delete '{target['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        items.remove(target)
        save_data(items)
        print(f"'{target['name']}' deleted.")
    else:
        print("Delete cancelled.")


def top_favorites(items):
    favs = [item for item in items if item["favorite"]]
    if not favs:
        print("No favorites yet.")
        return

    print("=== Top Favorites ===")
    for i, item in enumerate(favs, 1):
        print_item(item, index=i, show_category=True)


def main():
    items = load_data()

    while True:
        print("\n=== Booklet of Collectibles ===")
        print("1. Add an item")
        print("2. View categories")
        print("3. Search items")
        print("4. Mark/unmark favorite")
        print("5. Delete an item")
        print("6. Top Favorites")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_item(items)
        elif choice == "2":
            view_categories(items)
        elif choice == "3":
            search_items(items)
        elif choice == "4":
            mark_favorite(items)
        elif choice == "5":
            delete_item(items)
        elif choice == "6":
            top_favorites(items)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    main()

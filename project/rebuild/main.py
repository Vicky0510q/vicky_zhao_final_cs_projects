from data import load_items, save_items, get_all_categories
from utils import check_url, print_item, print_categories, pick_from_list


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
    print_categories(categories, items)
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

    tags_input = input("Tags (comma-separated, or press Enter to skip): ").strip()
    tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []

    item = {
        "name": name,
        "url": url,
        "category": category,
        "description": description,
        "favorite": False,
        "tags": tags
    }

    from models import Item
    new_item = Item(**item)
    items.append(new_item)
    save_items(items)
    print(f"Added '{name}' under {category}.")


def view_categories(items):
    categories = get_all_categories(items)
    print_categories(categories, items)

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
    cat_items = [item for item in items if item.category == category]

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
        if (keyword in item.name.lower()
                or keyword in item.category.lower()
                or keyword in item.description.lower()
                or any(keyword in tag.lower() for tag in item.tags)):
            results.append(item)

    if not results:
        print("No items found.")
    else:
        print(f"Found {len(results)} results:")
        for i, item in enumerate(results, 1):
            print_item(item, index=i, show_category=True)


def edit_item(items):
    if not items:
        print("No items to edit.")
        return

    print("All items:")
    target = pick_from_list(items, "Pick an item number to edit")
    if not target:
        return

    print(f"\nEditing: {target.name}")
    print("  1. Name")
    print("  2. URL")
    print("  3. Category")
    print("  4. Description")
    print("  5. Tags")
    print("  6. Cancel")

    field = input("Which field to edit? ").strip()

    if field == "1":
        new_name = input(f"New name [{target.name}]: ").strip()
        if new_name:
            target.name = new_name
    elif field == "2":
        new_url = input(f"New URL [{target.url}]: ").strip()
        if new_url:
            ok, reason = check_url(new_url)
            if not ok:
                print(f"URL check failed: {reason}. URL not updated.")
                return
            target.url = new_url
    elif field == "3":
        categories = get_all_categories(items)
        print_categories(categories, items)
        choice = input("New category (number): ").strip()
        try:
            num = int(choice)
            if 1 <= num <= len(categories):
                target.category = categories[num - 1]
            else:
                print("Invalid choice.")
                return
        except ValueError:
            print("Invalid choice.")
            return
    elif field == "4":
        new_desc = input(f"New description [{target.description}]: ").strip()
        target.description = new_desc
    elif field == "5":
        print(f"Current tags: {', '.join(target.tags) if target.tags else '(none)'}")
        new_tags = input("New tags (comma-separated): ").strip()
        target.tags = [t.strip() for t in new_tags.split(",") if t.strip()] if new_tags else []
    elif field == "6":
        print("Edit cancelled.")
        return
    else:
        print("Invalid choice.")
        return

    save_items(items)
    print(f"'{target.name}' updated.")


def mark_favorite(items):
    categories = get_all_categories(items)
    print_categories(categories, items)

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
    cat_items = [item for item in items if item.category == category]

    if not cat_items:
        print("No items in this category.")
        return

    print(f"\n--- {category} ---")
    target = pick_from_list(cat_items, "Pick an item number to toggle favorite")
    if not target:
        return

    target.favorite = not target.favorite
    save_items(items)

    if target.favorite:
        print(f"'{target.name}' marked as favorite.")
    else:
        print(f"'{target.name}' unmarked as favorite.")


def delete_item(items):
    if not items:
        print("No items to delete.")
        return

    print("All items:")
    target = pick_from_list(items, "Pick an item number to delete")
    if not target:
        return

    confirm = input(f"Delete '{target.name}'? (y/n): ").strip().lower()
    if confirm == "y":
        items.remove(target)
        save_items(items)
        print(f"'{target.name}' deleted.")
    else:
        print("Delete cancelled.")


def top_favorites(items):
    favs = [item for item in items if item.favorite]
    if not favs:
        print("No favorites yet.")
        return

    print("=== Top Favorites ===")
    for i, item in enumerate(favs, 1):
        print_item(item, index=i, show_category=True)


def sort_items(items):
    if not items:
        print("No items to sort.")
        return

    print("Sort by:")
    print("  1. Name (A-Z)")
    print("  2. Category")
    print("  3. Favorite (favorites first)")
    print("  4. Date added (newest first)")
    print("  5. Cancel")

    choice = input("Choose sort option: ").strip()

    if choice == "1":
        items.sort(key=lambda x: x.name.lower())
        print("Sorted by name.")
    elif choice == "2":
        items.sort(key=lambda x: x.category.lower())
        print("Sorted by category.")
    elif choice == "3":
        items.sort(key=lambda x: (not x.favorite, x.name.lower()))
        print("Sorted by favorite.")
    elif choice == "4":
        items.sort(key=lambda x: x.date_added, reverse=True)
        print("Sorted by date added (newest first).")
    elif choice == "5":
        print("Sort cancelled.")
        return
    else:
        print("Invalid choice.")
        return

    save_items(items)
    print("\nSorted items:")
    for i, item in enumerate(items, 1):
        print_item(item, index=i, show_category=True)


def main():
    items = load_items()

    while True:
        print("\n=== Booklet of Collectibles ===")
        print("1. Add an item")
        print("2. View categories")
        print("3. Search items")
        print("4. Mark/unmark favorite")
        print("5. Delete an item")
        print("6. Top Favorites")
        print("7. Edit an item")
        print("8. Sort items")
        print("9. Exit")

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
            edit_item(items)
        elif choice == "8":
            sort_items(items)
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-9.")


if __name__ == "__main__":
    main()

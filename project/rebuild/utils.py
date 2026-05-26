import requests


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
    prefix = f"{index}. " if index is not None else ""
    cat = f" — {item.category}" if show_category else ""
    print(f"{prefix}{item}{cat}")


def print_categories(categories, items):
    print("Categories:")
    for i, cat in enumerate(categories, 1):
        count = sum(1 for item in items if item.category == cat)
        print(f"  {i}. {cat} ({count} items)")


def pick_from_list(items, prompt="Pick an item number"):
    for i, item in enumerate(items, 1):
        print_item(item, index=i, show_category=True)

    choice = input(f"{prompt}: ").strip()
    try:
        num = int(choice)
    except ValueError:
        print("Invalid choice.")
        return None

    if not (1 <= num <= len(items)):
        print("Invalid choice.")
        return None

    return items[num - 1]

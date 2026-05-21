# Final Project PRD (Updated)

## Project Title

Booklet of Collectibles

## One Sentence Pitch

A command-line Python program that lets users collect and categorize URLs to articles, videos, and books, so they can easily find them later by browsing categories or searching by keyword.

## Target User

People who collect online content (articles, videos, books) but lose track of where they saved them.

## Purpose

Makes it easy to organize and retrieve saved links by category and keyword search, so you never lose track of a useful resource again.

## MVP

A command-line Python program where the user can add a collectible (name + URL + category), view items by category, search by keyword, and delete items. Data is saved to a JSON file so it persists between sessions.

---

## Must-Have Features (3)

1. **Search by keyword** — case-insensitive, matches across name, category, AND description fields. Partial matches count (e.g., "space" matches "Cool Article About Space").
2. **View items grouped by category** — two-step flow: user picks a category from a numbered list, then sees all items in that category. Displays name, URL, and favorite status.
3. **Add items with name, URL, and category** — URL validation required (see API section below). If URL is unreachable or returns an error, the save is **blocked** and the user is told why.

## Nice-to-Have Features (2)

1. **Description field** — optional free-text field for each item (included in search).
2. **Favorite marking** — toggleable per item. Shown as `[★]` in list views.

## Stretch Feature (1)

1. **Top Favorites view** — a menu option that shows only items marked as favorite.

---

## Required Complexity: API Connection

When the user adds an item, the program sends an HTTP request to the provided URL using the `requests` library.

- **Timeout**: 5 seconds.
- **If the request succeeds** (any 2xx/3xx response): item is saved.
- **If the request fails** (timeout, connection error, 4xx, 5xx): save is **blocked**. User sees a message like: `"URL check failed: [reason]. Item not saved."`
- **Implementation**: wrap in a function like `check_url(url) -> tuple[bool, str]` that returns (success, reason).

## Python Skills Demonstrated (7)

- [x] Functions — modular design (menu, add, search, check_url, save/load)
- [x] Lists — list of item dicts
- [x] Dictionaries — item data structure
- [x] File reading/writing — JSON persistence
- [x] API use — HTTP request for URL validation
- [x] Loops — menu loop, iteration over items
- [x] Conditional logic — category selection, search filtering, URL check result
- [x] User input/output — all menu interactions

---

## Data Plan

### Fields per item

| Field         | Type  | Required | Notes                                |
|---------------|-------|----------|--------------------------------------|
| `name`        | str   | yes      | Display name of the item             |
| `url`         | str   | yes      | Must pass URL validation on add      |
| `category`    | str   | yes      | From default list or user-created    |
| `description` | str   | no       | Defaults to empty string `""`        |
| `favorite`    | bool  | no       | Defaults to `False`                  |

### Default categories

- Articles
- Videos
- Books
- Other

Users can create new categories during the add-item flow. Categories are not deletable or renameable (simplifies scope).

### Duplicates

Duplicate URLs are **allowed** — no check for existing URLs.

### Storage

- File: `collectibles.json` in the same directory as the script.
- Format: JSON list of dicts.
- Saved after every add, delete, or favorite toggle.
- If file is missing on startup: start with an empty list.
- If file is corrupted (invalid JSON): print an error message and start with an empty list.

---

## Menu Design

```
=== Booklet of Collectibles ===
1. Add an item
2. View categories
3. Search items
4. Mark/unmark favorite
5. Delete an item
6. Top Favorites
7. Exit
Choose an option:
```

- Menu loops until user picks 7 (Exit).
- Invalid input (non-numeric, out of range) shows an error and re-displays the menu.
- Screen does **not** clear between actions — output prints below the previous action.

---

## Detailed Flows

### 1. Add an item

1. Prompt: `"Item name: "` — user types the name (cannot be blank).
2. Prompt: `"URL: "` — user types the URL.
   - Program runs `check_url(url)`. If it fails, print `"URL check failed: [reason]. Item not saved."` and return to menu.
3. Prompt: `"Category: "` — show numbered list of existing categories + an option to create a new one.
   - If user picks an existing category, use it.
   - If user picks "New category", prompt: `"New category name: "`. Add it to the category list for future use.
4. Prompt: `"Description (optional, press Enter to skip): "` — defaults to `""`.
5. Save item to `collectibles.json`.
6. Print: `"Added '[name]' under [category]."` and return to menu.

### 2. View categories

1. Show numbered list of all categories (including user-created ones).
   ```
   1. Articles (3 items)
   2. Videos (1 item)
   3. Books (0 items)
   4. Other (2 items)
   ```
2. User picks a number.
3. Show all items in that category:
   ```
   --- Articles ---
   1. [★] Cool Article About Space — https://example.com/space
   2. [ ] Python Tips — https://example.com/python
   3. [ ] Another Article — https://example.com/another
   ```
4. Return to menu.

### 3. Search items

1. Prompt: `"Search keyword: "` — user types a keyword.
2. Case-insensitive search across name, category, and description fields.
3. Show matching items:
   ```
   Found 2 results:
   1. [★] Cool Article About Space — Science — https://example.com/space
   2. [ ] Python Tips — Articles — https://example.com/python
   ```
4. If no matches: `"No items found."`
5. Return to menu.

### 4. Mark/unmark favorite

1. Show numbered list of all categories.
2. User picks a category.
3. Show items in that category, numbered.
4. User picks an item number.
5. Toggle the `favorite` field (True → False, False → True).
6. Print: `"'[name]' marked as favorite."` or `"'[name]' unmarked as favorite."`
7. Save to JSON. Return to menu.

### 5. Delete an item

1. Show all items across all categories, numbered:
   ```
   1. [★] Cool Article About Space — Science — https://example.com/space
   2. [ ] Python Tips — Articles — https://example.com/python
   3. [ ] Another Article — Other — https://example.com/another
   ```
2. User picks a number to delete.
3. Prompt: `"Delete '[name]'? (y/n): "` — confirm before deleting.
4. If confirmed, remove from list, save to JSON, print: `"'[name]' deleted."`
5. Return to menu.

### 6. Top Favorites

1. Filter items where `favorite == True`.
2. Show them:
   ```
   === Top Favorites ===
   1. [★] Cool Article About Space — Science — https://example.com/space
   2. [★] Best Video Ever — Videos — https://example.com/video
   ```
3. If no favorites: `"No favorites yet."`
4. Return to menu.

---

## Item Data Structure

```python
{
    "name": "Cool Article About Space",
    "url": "https://example.com/space",
    "category": "Science",
    "description": "",
    "favorite": False
}
```

---

## First Tiny Step

Build the main menu loop and the add-item flow (without URL validation yet). Then add URL validation as the next step.

## Possible Risk

URL validation may be slow or blocked by some websites. Mitigation: 5-second timeout, clear error message to user.

## Project Lane

- [x] Lane 2: Personal Utility

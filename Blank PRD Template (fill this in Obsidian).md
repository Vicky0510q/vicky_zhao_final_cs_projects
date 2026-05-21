# Final Project PRD

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

## Must-Have Features (3 only)

1. Search by keyword across name, category, and description (case-insensitive)
2. View items grouped by category (two-step: pick category, then see items)
3. Add items with name, URL, and category (with URL validation on add)

## Nice-to-Have Features (1 or 2)

1. Detailed description field for each item
2. Favorite marking (shown as [★] in list view)

## Stretch Feature (1 only)

1. Top Favorites view — a menu option that shows only items marked as favorite

## Required Complexity (Difficulty Feature)

Every project must include at least ONE difficulty feature.

Pick one option and explain why:

- [ ] Option 1: File Storage (save/load user data)
- [x] Option 2: API Connection (fetch live external data)
- [ ] Option 3: Object-Oriented Design (use at least one class)
- [ ] Option 4: Data Analysis (analyze data and give useful results)
- [ ] Option 5: Visual Output (create a chart or visual display)

Which option did you choose? Why?
Option 2: API Connection. When the user adds an item, the program makes a request to the URL to check it's reachable. If it's a 404 or unreachable, the save is blocked. This catches broken links at entry time.

## Python Skills You Will Use

Check at least 4 boxes. Your project must demonstrate at least 4 of these skills:

- [x] Functions
- [x] Lists
- [x] Dictionaries
- [x] File reading or writing
- [x] API use
- [ ] Classes and objects
- [ ] Error handling
- [x] Loops
- [x] Conditional logic
- [ ] Data visualization
- [x] User input and output

## Data Plan

1. What data does my project need?
   Each item has: name (str), url (str), category (str), description (str, optional), favorite (bool, default False).
2. Where will the data come from?
   User input at runtime. URLs are validated via HTTP requests.
3. How will I store or organize the data?
   JSON file on disk. Items stored as a list of dicts, saved after every add/delete/favorite change.

## First Tiny Step

Build the main menu loop and the add-item flow (without URL validation yet).

## Possible Risk

URL validation may be slow or blocked by some websites. Mitigation: set a short timeout (e.g., 5 seconds) and warn the user if the check fails.

## Project Lane

Which lane did you choose?

- [ ] Lane 1: Data Tool
- [x] Lane 2: Personal Utility
- [ ] Lane 3: Game or Simulation
- [ ] Lane 4: Advanced Stretch (requires teacher approval)

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

Default categories: Articles, Videos, Books, Other. Users can create new categories during the add-item flow.

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

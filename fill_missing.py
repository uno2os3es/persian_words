import json
from pathlib import Path

# Files
ant_file = Path("ant.json")   # previously created JSON with word, synonym, antonym
dic_file = Path("dic.json")   # persian -> translation

# Load dic.json
with dic_file.open(encoding="utf-8") as f:
    dic = json.load(f)

# Load ant.json
with ant_file.open(encoding="utf-8") as f:
    ant_data = json.load(f)

def translate_list(lst):
    """Replace any Persian word with translation from dic.json if available"""
    return [dic.get(word, word) for word in lst]

# Fill blanks
for entry in ant_data:
    if not entry.get("synonym"):
        entry["synonym"] = translate_list([entry["word"]])
    if not entry.get("antonym"):
        entry["antonym"] = translate_list([entry["word"]])

# Save back
with ant_file.open("w", encoding="utf-8") as f:
    json.dump(ant_data, f, ensure_ascii=False, indent=2)

print(f"Filled missing synonyms/antonyms in {ant_file}")
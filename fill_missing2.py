import json
from pathlib import Path

# Files
ant_file = Path("ant.json")
dic_file = Path("dic.json")

# Load dictionary
with dic_file.open(encoding="utf-8") as f:
    dic = json.load(f)

# Load ant.json
with ant_file.open(encoding="utf-8") as f:
    ant_data = json.load(f)

# Example antonym mapping (fill with more words as needed)
ANTONYM_MAP = {
    "آباد": "خراب",
    "خراب": "آباد",
    "درصد": "کسر",
    "سالم": "بیمار",
    "زیاد": "کم",
    "کوچک": "بزرگ"
}

# Fill missing antonyms
for entry in ant_data:
    if not entry.get("antonym"):
        word = entry["word"]
        antonym = ANTONYM_MAP.get(word)
        if antonym:
            entry["antonym"] = [antonym]
        else:
            entry["antonym"] = []

# Save back
with ant_file.open("w", encoding="utf-8") as f:
    json.dump(ant_data, f, ensure_ascii=False, indent=2)

print(f"Filled real antonyms for {ant_file}")
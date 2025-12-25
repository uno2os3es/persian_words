import json
import sys
from pathlib import Path
import re

# --- character normalization ---
TRANS = str.maketrans({
    "ي": "ی",
    "ك": "ک",
    "ة": "ه",
    "ؤ": "و",
    "إ": "ا",
    "أ": "ا",
    "ٱ": "ا",
    "ئ": "ی",
    "‌": "",   # ZWNJ
})

def normalize(text: str) -> str:
    return text.translate(TRANS)

def split_senses(text: str):
    """
    Returns {sense_number: text}
    """
    parts = re.split(r"\b(\d+)\b", text)
    senses = {}
    current = None

    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part.isdigit():
            current = int(part)
            senses[current] = ""
        elif current is not None:
            senses[current] += " " + part

    return senses

def parse_items(text: str):
    text = normalize(text)
    text = text.replace("،", ",")
    return [x.strip() for x in text.split(",") if x.strip()]

# --- main ---
if len(sys.argv) != 3:
    print("Usage: python dict_to_json_sense.py <input.txt> <output.json>")
    sys.exit(1)

inp = Path(sys.argv[1])
out = Path(sys.argv[2])

records = []

for line in inp.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or ":" not in line:
        continue

    word, rest = line.split(":", 1)
    word = normalize(word.strip())

    syn_part, ant_part = rest, ""
    if "&" in rest:
        syn_part, ant_part = rest.split("&", 1)

    syn_senses = split_senses(syn_part)
    ant_senses = split_senses(ant_part)

    all_senses = sorted(set(syn_senses) | set(ant_senses))

    for s in all_senses:
        records.append({
            "word": word,
            "sense": s,
            "synonym": parse_items(syn_senses.get(s, "")),
            "antonym": parse_items(ant_senses.get(s, ""))
        })

out.write_text(
    json.dumps(records, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Converted {len(records)} sense entries → {out}")
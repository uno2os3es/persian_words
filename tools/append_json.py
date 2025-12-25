#!/usr/bin/env python3
import json
from pathlib import Path

file_a = Path('a.txt')
file_b = Path('b.txt')
json_file = Path('dic.json')

# Load existing dictionary if exists
if json_file.exists():
    with json_file.open('r', encoding='utf-8') as jf:
        translation_dict = json.load(jf)
else:
    translation_dict = {}

# Read new lines
with file_a.open('r',
                 encoding='utf-8') as fa, file_b.open('r',
                                                      encoding='utf-8') as fb:
    for k, v in zip(fa, fb):
        k = k.strip()
        v = v.strip()
        translation_dict.setdefault(k, v)  # only add if key doesn't exist

# Sort dictionary by Persian words
sorted_dict = dict(sorted(translation_dict.items(), key=lambda item: item[0]))

# Save updated dictionary
with json_file.open('w', encoding='utf-8') as jf:
    json.dump(sorted_dict, jf, ensure_ascii=False, indent=2)

print(f'Updated {json_file}. Total unique entries: {len(sorted_dict)}')

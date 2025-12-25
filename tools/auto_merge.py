#!/usr/bin/env python3
import json
from pathlib import Path

json_file = Path('dic.json')
current_dir = Path('.')  # current directory

# Load existing dictionary if exists
if json_file.exists():
    with json_file.open('r', encoding='utf-8') as jf:
        translation_dict = json.load(jf)
else:
    translation_dict = {}

# Find all Persian txt files (ignore files ending with _eng.txt)
persian_files = [
    f for f in current_dir.glob('*.txt') if not f.name.endswith('_eng.txt')
]

for pf in persian_files:
    eng_file = pf.with_name(f'{pf.stem}_eng.txt')
    if not eng_file.exists():
        print(
            f'Warning: translation file {eng_file.name} not found. Skipping {pf.name}'
        )
        continue

    with pf.open('r',
                 encoding='utf-8') as fa, eng_file.open('r',
                                                        encoding='utf-8') as fb:
        for k, v in zip(fa, fb):
            k = k.strip()
            v = v.strip()
            if k and v:  # skip empty lines
                translation_dict.setdefault(k,
                                            v)  # only add if key doesn't exist

# Sort dictionary by Persian words
sorted_dict = dict(sorted(translation_dict.items(), key=lambda item: item[0]))

# Save updated dictionary
with json_file.open('w', encoding='utf-8') as jf:
    json.dump(sorted_dict, jf, ensure_ascii=False, indent=2)

print(f'Updated {json_file}. Total unique entries: {len(sorted_dict)}')

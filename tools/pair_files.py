#!/usr/bin/env python3
import json
from pathlib import Path

# Paths to input and output files
file_a = Path('colors.txt')
file_b = Path('colors_eng.txt')
output_file = Path('dic.json')

# Read lines from both files
with file_a.open('r',
                 encoding='utf-8') as fa, file_b.open('r',
                                                      encoding='utf-8') as fb:
    lines_a = [line.strip() for line in fa]
    lines_b = [line.strip() for line in fb]

# Ensure both files have the same number of lines
if len(lines_a) != len(lines_b):
    print('Warning: The number of lines in a.txt and b.txt do not match.')

# Create dictionary
translation_dict = {k: v for k, v in zip(lines_a, lines_b)}

# Save to JSON
with output_file.open('w', encoding='utf-8') as out:
    json.dump(translation_dict, out, ensure_ascii=False, indent=2)

print(f'Saved {len(translation_dict)} entries to {output_file}')

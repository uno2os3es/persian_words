#!/data/data/com.termux/files/usr/bin/python
import json
import sys

with open('dic.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if not isinstance(data, dict):
    raise ValueError('JSON must be an object (key-value pairs)')

# Rebuild dict to ensure uniqueness
unique = {}
for k, v in data.items():
    unique[k] = v

wunik = []

# Write back in-place
with open('words.txt', 'r', encoding='utf-8') as fw:
    lines = fw.readlines()
    for line in lines:
        cleaned = line.strip('\n').lstrip().rstrip()
        if not cleaned in unique:
            wunik.append(line)

with open('words.txt', 'w', encoding='utf-8') as fo:
    fo.write(''.join(wunik))
print('done')

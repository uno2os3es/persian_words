def tabs_to_spaces(text: str, spaces: int = 1) -> str:
    return text.replace('\t', ' ' * spaces)


cleaned = ''
with open('dic.json', 'r') as f:
    data = f.read()
    cleaned = tabs_to_spaces(data, 1)

with open('dic.json', 'w') as fo:
    fo.write(cleaned)

print('done')

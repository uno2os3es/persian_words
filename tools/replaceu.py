#!/usr/bin/env python3
import sys
import re
from pathlib import Path

_unicode_re = re.compile(r'\\u([0-9a-fA-F]{4})')


def decode_unicode_escapes(text: str) -> str:
    return _unicode_re.sub(lambda m: chr(int(m.group(1), 16)), text)


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <filename>')
        sys.exit(1)

    fname = Path(sys.argv[1])

    if not fname.is_file():
        print(f'Error: file not found: {fname}')
        sys.exit(1)

    data = fname.read_text(encoding='utf-8')
    decoded = decode_unicode_escapes(data)

    fname.write_text(decoded, encoding='utf-8')
    print(f'Unicode escapes decoded successfully: {fname}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import sys
from pathlib import Path


def decode_unicode_escapes(text: str) -> str:
    # Decode sequences like \uXXXX into real Unicode characters
    return text.encode('utf-8').decode('unicode_escape')


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

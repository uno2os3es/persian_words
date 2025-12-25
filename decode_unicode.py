import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python decode_unicode_escapes.py <json_file>")
    sys.exit(1)

path = Path(sys.argv[1])

text = path.read_text(encoding="utf-8")

# Decode \uXXXX sequences into real Unicode characters
decoded = text.encode("utf-8").decode("unicode_escape")

path.write_text(decoded, encoding="utf-8")

print(f"Unicode escapes decoded in-place: {path}")
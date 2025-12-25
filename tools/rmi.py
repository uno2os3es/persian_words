#!/data/data/com.termux/files/usr/bin/python
import unicodedata
import sys

# Define a set of known invisible/formatting characters
INVISIBLE_CHARS = {
    '\u200b',  # ZERO WIDTH SPACE
    '\u200c',  # ZERO WIDTH NON-JOINER
    '\u200d',  # ZERO WIDTH JOINER
    '\u00a0',  # NO-BREAK SPACE
    '\u00ad',  # SOFT HYPHEN
    '\ufeff',  # ZERO WIDTH NO-BREAK SPACE (BOM)
    '\u202a',  # LEFT-TO-RIGHT EMBEDDING
    '\u202b',  # RIGHT-TO-LEFT EMBEDDING
    '\u202c',  # POP DIRECTIONAL FORMATTING
    '\u202d',  # LEFT-TO-RIGHT OVERRIDE
    '\u202e',  # RIGHT-TO-LEFT OVERRIDE
}


def clean_text(text: str) -> str:
    """Remove invisible and formatting characters from text."""
    return ''.join(
        c for c in text
        if c == '\n' or (c not in INVISIBLE_CHARS and
                         unicodedata.category(c) not in ('Cc', 'Cf')))


def main():
    # Read file
    with open(sys.argv[1], encoding='utf-8') as f:
        text = f.read()

    # Clean text
    cleaned = clean_text(text)

    # Report how many characters were removed
    removed = len(text) - len(cleaned)
    if removed:
        print(f'{removed} invisible characters removed')
    else:
        print('No invisible characters found')

    # Overwrite file with cleaned text
    with open(sys.argv[1], 'w', encoding='utf-8') as f:
        f.write(cleaned)

    print('done')


if __name__ == '__main__':
    main()

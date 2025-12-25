import json
import pathlib
import re


def clean_persian_text(text):
    # This keeps only Persian letters, standard spaces, and numbers.
    # It removes invisible control characters, ZWNJ, and 'black dots'.
    # Range: \u0600-\u06FF (Persian/Arabic)
    return ''.join(re.findall(r'[\u0600-\u06FF\s]', text)).strip()


def convert_to_clean_json(input_file, output_file) -> None:
    # Pattern to match Persian part and English part
    pattern = re.compile(
        r'([\u0600-\u06FF\s\W]+?)\s*(?:<->|<-->|\s{2,})\s*([a-zA-Z\s]+)')

    dictionary_data = {}

    try:
        with pathlib.Path(input_file).open(encoding='utf-8') as f:
            for line in f:
                matches = pattern.findall(line)
                for fa_word, en_word in matches:
                    # 1. Clean the Persian word of invisible characters
                    clean_fa = clean_persian_text(fa_word)
                    # 2. Clean the English translation
                    clean_en = en_word.strip()

                    if clean_fa and clean_en:
                        dictionary_data[clean_fa] = clean_en

        # Sort and Save
        sorted_dict = dict(sorted(dictionary_data.items()))

        with pathlib.Path(output_file).open('w', encoding='utf-8') as f_out:
            json.dump(sorted_dict, f_out, ensure_ascii=False, indent=4)

        print(
            f'Success! Cleaned and saved {len(sorted_dict)} entries to {output_file}'
        )

    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    convert_to_clean_json('words.txt', 'dic.json')

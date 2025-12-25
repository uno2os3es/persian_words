import pathlib
import re


def extract_and_trim_persian(input_file, output_file) -> None:
    # Pattern to find the first Persian character in a line
    persian_start_pattern = re.compile(r'[\u0600-\u06FF]')

    try:
        with pathlib.Path(input_file).open('r', encoding='utf-8') as f_in:
            with pathlib.Path(output_file).open('w', encoding='utf-8') as f_out:
                for line in f_in:
                    match = persian_start_pattern.search(line)
                    if match:
                        # Extract from the first Persian character to the end of the line
                        trimmed_line = line[match.start():]
                        f_out.write(trimmed_line)

        print(f'Done! Cleaned words saved to {output_file}')

    except FileNotFoundError:
        print("Error: '20.txt' not found.")
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    extract_and_trim_persian('20.txt', 'words.txt')

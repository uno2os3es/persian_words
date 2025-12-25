import pathlib
import re


def extract_persian_lines(input_file, output_file) -> None:
    # This regex matches any character in the Arabic/Persian Unicode block
    persian_pattern = re.compile(r'[\u0600-\u06FF]')

    try:
        with pathlib.Path(input_file).open('r', encoding='utf-8') as f_in:
            with pathlib.Path(output_file).open('w', encoding='utf-8') as f_out:
                for line in f_in:
                    # Check if the line contains at least one Persian character
                    if persian_pattern.search(line):
                        f_out.write(line)

        print(f'Extraction complete. Persian lines saved to {output_file}')

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    extract_persian_lines('20.txt', 'words.txt')

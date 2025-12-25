def last_occurrence_line(filename, char):
    last_line = -1
    with open(filename, encoding='utf-8') as f:
        for i, line in enumerate(f, start=1):
            if char in line:
                last_line = i
    return last_line


# Example usage:
print(last_occurrence_line('words.txt', '",'))

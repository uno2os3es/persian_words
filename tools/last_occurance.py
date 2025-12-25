def last_occurrence(filename, char):
    with open(filename, encoding='utf-8') as f:
        text = f.read()
    pos = text.rfind(char)  # returns -1 if not found
    return pos


# Example usage:
print(last_occurrence('word.txt', 'پ'))  # finds last occurrence of 'پ'

with open('test.json', 'r') as f:
    str1 = f.read()
    for ch in str(str1):
        print(f'{ch}=={ord(ch)}')

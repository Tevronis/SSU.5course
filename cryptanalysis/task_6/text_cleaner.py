def del_not_alf(text, alf):
    text = text.lower()
    result = ''
    for i in range(len(text)):
        if text[i] in alf:
            result += text[i]
    return result


textname = input('Enter filename: ')
outfile = input('Out filename: ')
alph = open('alphabet.txt').read()
with open(textname) as f:
    result = del_not_alf(f.read(), alph)

with open(outfile, 'w') as f:
    f.write(result)

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
    t = f.read()
    result = del_not_alf(t, alph)

with open(outfile, 'w') as f:
    f.write(result)

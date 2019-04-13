import mono


def get_cryptotext():
    mod2 = int(input('1 - сгенерировать ключ\n2 - зашифровать\n> '))
    if mod2 == 1:
        open('key.txt', 'w')
        length = int(input('длина ключа: '))
        key = mono.gen_key(length)
        for i in range(len(key)):
            open('key.txt', 'a').write(str(key[i]) + ' ')
    if mod2 == 2:
        key = list(map(int, open('key.txt').read().strip().split(' ')))
        fout = open('crypt.txt', 'w', encoding='utf-8')
        name = input('name: ')
        with open(name + '.txt', 'r', encoding='utf-8') as fin:
            text = fin.read(len(key))
            while text:
                text = text.lower()
                # print(text)
                result = mono.encryption(key, text)
                # print(result)
                fout.write(result)
                text = fin.read(len(key))
        fout.close()


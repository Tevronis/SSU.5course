import simpson
import vigenere


def encrypt():
    modv = int(input('1 - зашифровать\n2 - дешифровать\n> '))
    if modv == 1:
        name = input('файл: ')
        with open(name + '.txt', 'r') as fin:
            text = fin.read()
        alf = open('alphabet.txt', 'r').read().strip()
        key = open('key.txt', 'r').read().strip()
        open('key_len.txt', 'w').write(str(len(key)))
        text = vigenere.del_not_alf(text, alf)
        crypt = vigenere.vigenere_encryption(text, key, alf)
        open('crypt.txt', 'w').write(crypt)

    if modv == 2:
        with open('crypt.txt', 'r') as fin:
            text = fin.read()
        key = open('key.txt').read().strip()
        alf = open('alphabet.txt', 'r').read().strip()
        decrypt = vigenere.vigenere_decryption(text, key, alf)
        open('decrypt.txt', 'w').write(str(decrypt))


def simpson_mode():
    with open('crypt.txt', 'r') as fin:
        text = fin.read()
    l = int(input('длина ключа: '))
    with open('ot_alf.txt', 'r') as fina:
        alf_ot = fina.read()
    alf = open('alphabet.txt', 'r').read().strip()
    deltas = simpson.get_deltas(l, text, alf, alf_ot)
    keys = simpson.get_keys(deltas, alf)
    with open('answers.txt', 'w') as fout2:
        for item in keys:
            fout2.write(item + '\n')
            fout2.write(vigenere.vigenere_decryption(text, item, alf) + '\n\n\n')


def main():
    mod = int(input('0 - шифр Виженера\n'
                    '1 - метод Симпсона\n> '))
    if mod == 0:
        encrypt()

    if mod == 1:
        simpson_mode()


if __name__ == '__main__':
    main()


import matrix
import vigenere
import keys_finding


def encryption():
    modv = int(input('1 - зашифровать\n2 - дешифровать\n> '))
    if modv == 1:
        name = input('файл: ')
        with open(name + '.txt', 'r') as fin:
            text = fin.read()
        alf = open('alphabet.txt', 'r').read().strip()
        key = open('key.txt', 'r').read().strip()
        text = vigenere.del_not_alf(text, alf)
        crypt = vigenere.vigenere_encryption(text, key, alf)
        open('crypt.txt', 'w').write(crypt)
        print('Сохранен файл crypt.txt')

    if modv == 2:
        with open('crypt.txt', 'r') as fin:
            text = fin.read()
        key = open('key.txt').read().strip()
        alf = open('alphabet.txt', 'r').read().strip()
        decrypt = vigenere.vigenere_decryption(text, key, alf)
        open('decrypt.txt', 'w').write(str(decrypt))
        print('Сохранен файл decrypt.txt')


def create_matrix():
    name = input('файл открытого текста: \n> ')
    with open(name + '.txt', 'r') as fin:
        text = fin.read()
    alf = open('alphabet.txt', 'r').read().strip()
    mx = matrix.get_reference_matrix(text, alf)
    with open('reference_matrix.txt', 'w') as fout:
        for i in range(len(mx)):
            for j in range(len(mx)):
                fout.write('{:.7f}'.format(mx[i][j]))
                fout.write(' ')
            fout.write('\n')
    print('Сохранен файл reference_matrix.txt')


def calculate_key():
    d = int(input('длина ключа: \n> '))
    alf = open('alphabet.txt', 'r').read().strip()
    with open('crypt.txt', 'r') as fin:
        crypt = fin.read()

    mat = []
    with open('reference_matrix.txt', 'r') as fin_m:
        for line in fin_m:
            mat.append([float(item) for item in line.split()])

    key = keys_finding.finding(d, alf, crypt, mat)
    print('найден ключ: ', key)
    with open('probable_key.txt', 'w') as fout:
        fout.write(key)
    print('Сохранен файл probable_key.txt')


def main():
    mod = int(input('0 - шифр Виженера\n'
                    '1 - создание эталонной матрицы биграм\n'
                    '2 - вычисление ключа\n> '))
    if mod == 0:
        encryption()

    if mod == 1:
        create_matrix()

    if mod == 2:
        calculate_key()


if __name__ == '__main__':
    main()


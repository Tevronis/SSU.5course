# coding=utf-8
import gen_tables
import vigenere
import key_finding
from utils import read_txt


def vigenere_mod():
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
        print('сохранен файл: crypt.txt')

    if modv == 2:
        with open('crypt.txt', 'r') as fin:
            text = fin.read()
        key = open('key.txt').read().strip()
        alf = open('alphabet.txt', 'r').read().strip()
        decrypt = vigenere.vigenere_decryption(text, key, alf)
        open('decrypt.txt', 'w').write(str(decrypt))
        print('сохранен файл: decrypt.txt')


def counter():
    mod1 = int(input('1 - вычисление таблицы частот открытых сообщений\n'
                     '2 - вычисление ключа атакой по частотному анализу\n> '))
    if mod1 == 1:
        name = input('файл открытого текста: ')
        text = read_txt(name)
        alf = open('alphabet.txt', 'r').read().strip()

        table = gen_tables.open_table(text, alf)

        with open('ot_table.txt', 'w') as fout:
            for k, v in table:
                fout.write('{} {:.7f}\n'.format(k, v))
        ans = gen_tables.gen_ot_alf(table)
        open('ot_alf.txt', 'w').write(ans)
        print('сохранен файл: ot_alf.txt')
        print('сохранен файл: ot_table.txt')

    if mod1 == 2:
        alf = open('alphabet.txt', 'r').read().strip()
        l = int(input('длина ключа: '))
        k = int(input('введите количество символов максимальной точности: '))
        text = read_txt('crypt')
        alf_ot = read_txt('ot_alf')

        keys = key_finding.freq(text, l, alf_ot, alf, k)

        with open('fr_keys.txt', 'w') as fout1:
            for item in keys:
                fout1.write(item + '\n')
        with open('frequency_answers.txt', 'w') as fout2:
            for item in keys:
                fout2.write(item + '\n')
                fout2.write(vigenere.vigenere_decryption(text, item, alf) + '\n\n\n')
        print('сохранен файл: fr_keys.txt')
        print('сохранен файл: frequency_answers.txt')


def word_attack():
    mod2 = int(input('1 - вычисление таблицы наиболее частых слов в ОТ\n'
                     '2 - вычисление ключа атакой по вероятному слову\n> '))
    if mod2 == 1:
        name = input('файл открытого текста: ')
        with open(name + '.txt', 'r') as fin:
            text = fin.read()
        alf = open('alphabet.txt', 'r').read().strip()
        table = gen_tables.ot_dict(text, alf)
        with open('ot_table_words.txt', 'w') as fout:
            for k, v in table:
                fout.write('{} {:.7f}\n'.format(k, v))
        print('сохранен файл: ot_table_words.txt')

    if mod2 == 2:
        alf = open('alphabet.txt', 'r').read().strip()
        word = input('слово: ')
        with open('crypt.txt', 'r') as fin:
            text = fin.read()
        l = int(input('длина ключа: '))

        keys = key_finding.keys_by_word(text, word, l, alf)

        with open('probable_answers.txt', 'w') as fout:
            for item in keys:
                fout.write(item + '\n')
                fout.write(vigenere.vigenere_decryption_with(text, item, alf) + '\n\n')
        print('сохранен файл: probable_answers.txt')


def main():
    mod = int(input('0 - шифр Виженера\n'
                    '1 - атака по частотному анализу\n'
                    '2 - атака по вероятному слову\n> '))
    if mod == 0:
        vigenere_mod()

    if mod == 1:
        counter()

    if mod == 2:
        word_attack()


if __name__ == '__main__':
    main()

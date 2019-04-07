# -*- coding: utf-8 -*-
import json
from pprint import pprint

from kostill import mod100
from text_modification import del_punctuations, explore_text, get_forbidden_bigrams
from gen_table import text_division, make_table
from gen_forest import modify_table, make_forest
from brute import make_keys, modify_keys, decrypt_it


def forbidden_bigamy():
    name = input('файл текста:\n> ')

    with open(name + '.txt', 'r', encoding='utf-8') as fin:
        text = fin.read()

    text = del_punctuations(text)
    alf, bigrams = explore_text(text)
    strr = ''
    for item in alf:
        strr += item
    with open('alf.txt', 'w', encoding='utf-8') as fout:
        fout.write(strr)

    fb = get_forbidden_bigrams(alf, bigrams)
    with open('forbidden.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fb))


def generate_tables():
    name = input('файл шифротекста: ')
    with open(name + '.txt', 'r', encoding='utf-8') as fin:
        text = fin.read()
    l = int(input('длина периода: '))
    fb = []
    with open('forbidden.txt', 'r', encoding='utf-8') as fin_forb:
        for item in fin_forb:
            fb.append(item[:-1])
    blocks = text_division(text, l)
    table = make_table(blocks, fb, l)
    pprint(table)
    with open('table.txt', 'w', encoding='utf-8') as fout:
        for i in range(l):
            fout.write(str(table[0][i] + ' '))
        for i in range(1, l):
            fout.write(str('\n'))
            for j in range(l):
                fout.write(str(table[i][j]) + ' ')
        fout.write(str('\n'))


def create_forest():
    table = []
    with open('table.txt', 'r', encoding='utf-8') as fin_t:
        for item in fin_t:
            tmp = ''
            for i in range(0, len(item), 2):
                tmp += item[i]
            table.append(tmp[:-1])
    table = modify_table(table)
    make_forest(table)


def brute_keys():
    l = int(input('длина ключа: '))
    with open('forest.json', 'r') as fin:
        forest = json.load(fin)
    name = input('файл шифротекста: ')
    keys = make_keys(forest, l)
    print('ветки: ' + str(keys))
    keys = modify_keys(keys)
    print('ключи: ' + str(keys))
    decrypt_it(name, keys)


def main():
    mod = int(input('100 - шифрование\n1 - вычисление запретных биграмм\n2 - построение вспомогательной таблицы\n'
                    '3 - построение ориентированного леса\n4 - перебор ключей\n'))
    if mod == 100:
        mod100()
    if mod == 0:
        name = input('файл текста: ')

        with open(name + '.txt', 'r', encoding='utf-8') as fin:
            text = fin.read()

        # text = del_punctuations(text)
        text = text.lower()
        open(name + '.txt', 'w', encoding='utf-8').write(text)

    if mod == 1:
        forbidden_bigamy()

    if mod == 2:
        generate_tables()

    if mod == 3:
        create_forest()

    if mod == 4:
        brute_keys()


if __name__ == '__main__':
    main()

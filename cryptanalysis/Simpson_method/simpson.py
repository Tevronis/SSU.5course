import itertools
from copy import copy
from pprint import pprint

import collections


def average_overlap_index(a, b, alf):
    if len(a) != len(b):
        for i in range(len(a)-len(b)):
            b += ' '

    N = len(a)
    I = 0
    count_a = collections.Counter()
    count_b = collections.Counter()
    for i in range(len(a)):
        count_a[a[i]] += 1
        count_b[b[i]] += 1
    for i in range(len(alf)):
        I += (count_a[alf[i]]/N)*(count_b[alf[i]]/N)
    return I


def get_blocks_y(text, l):
    mas = ['' for j in range(l)]
    for i in range(len(text)):
        mas[i % l] += text[i]
    return mas


def analysis(block, fr_ot, alf):
    table = collections.Counter()
    for item in block:
        table[item] += 1
    for item in table:
        table[item] = table[item] / len(block)
    table = sorted(table.items(), key=lambda x: -x[1])
    fr_block = ''
    for item in table:
        fr_block += item[0]

    table2 = collections.Counter()
    for i in range(len(fr_block)):
        # print(len(fr_block))
        # print(len(fr_ot))
        a = (alf.index(fr_block[i]) - alf.index(fr_ot[i])) % len(alf)
        table2[a] += 1
    for item in table2:
        table2[item] = table2[item] / len(alf)
    table2 = sorted(table2.items(), key=lambda x: -x[1])
    mas_range = []
    for item in table2:
        mas_range.append(item[0])

    mas = []
    # print(mas_range)
    k = int(input('введите k:\n> '))
    for i in range(min(k, len(mas_range))):
        mas.append(mas_range[i])

    return mas


def get_deltas(l, text, alf, alf_ot):
    deltas = [[] for j in range(l)]
    blocks = get_blocks_y(text, l)
    for i in range(1, l):
        inds = []
        for j in range(len(alf)):
            del_Y = ''
            for item in blocks[i]:
                del_Y += alf[(alf.index(item) - j) % len(alf)]
            inds.append(average_overlap_index(blocks[0], del_Y, alf))
        # print(inds)
        # print('\n')
        around = 1
        min_value = max([round(item, around) for item in inds])
        for j in range(len(inds)):
            if round(inds[j], around) == min_value:
                # print(inds[j])
                deltas[i].append(j)
    deltas[0] = analysis(blocks[0], alf_ot, alf)
    return deltas


# def gen_all_keys(mas):
#     pprint(mas)
#     result = []
#     for item in itertools.product(*mas):
#         tmp = ''
#         for i in item:
#             tmp += i
#         result.append(tmp)
#
#     return result


def gen_all_keys(mas):
    result = []
    path = []

    def rec(deep, pos):
        if len(path) == len(mas):
            result.append(''.join(path))
            return

        for item in mas[deep][pos]:
            path.append(item)
            rec(deep + 1, pos)
            path.pop()

    for i in range(len(mas[0])):
        rec(0, i)
    # pprint(result)
    return result


def get_keys(deltas, alf):
    options = [[] for j in range(len(deltas))]
    for item in deltas[0]:
        options[0].append(alf[item])

    for i in range(1, len(deltas)):
        options[i] = [[] for _ in range(len(deltas[0]))]
        for item in deltas[i]:
            for idx, item2 in enumerate(deltas[0]):
                options[i][idx % len(deltas[0])].append(alf[(item+item2) % len(alf)])
    print('Таблица:\n')
    pprint(options)
    res = gen_all_keys(options)
    print('Список вероятных ключей:', res)
    return res









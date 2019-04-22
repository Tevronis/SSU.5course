from pprint import pprint
import itertools
import collections


def analysis(block, fr_ot, alf, k):
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
    for i in range(k):
        mas.append(alf[int(mas_range[i])])

    return mas


def gen_all_keys(mas):
    pprint(mas)
    result = []

    for item in itertools.product(*mas):
        result.append(''.join(item))

    return result


def freq(text, l, alf_ot, alf, k):
    mas = ['' for j in range(l)]
    for i in range(len(text)):
        mas[i % l] += text[i]
    result = []
    for item in mas:
        result.append(analysis(item, alf_ot, alf, k))
    ans = gen_all_keys(result)
    return ans


def shift(word):
    new_word = word[1:] + word[0]
    return new_word


def make_keys_new(text, alf, word, l):
    keys = set()
    for i in range(len(text) - l):
        key = ''
        for j in range(l):
            if word[j] not in alf:
                key += '*'
            else:
                # print(text[i+j] + ' ' + str(alf.index(text[i+j])))
                # print(word[j] + ' ' + str(alf.index(word[j])))
                # print(alf[(alf.index(text[i+j]) - alf.index(word[j])) % len(alf)] + ' ' + str((alf.index(text[i+j]) - alf.index(word[j])) % len(alf)))
                # print('\n')
                key += alf[(alf.index(text[i + j]) - alf.index(word[j])) % len(alf)]
        keys.add(key)
        for ii in range(l):
            key = shift(key)
            keys.add(key)
    return keys


def keys_by_word(text, word, l, alf):
    if len(word) < l:
        for i in range(l - len(word)):
            word += '*'
    keys = make_keys_new(text, alf, word, l)

    return keys

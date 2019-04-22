import collections
from copy import copy


def shift_keys(table_ot, table_crypt, alf):
    keys = []
    for (a, b) in list(zip(table_ot, table_crypt)):
        keys.append((alf.index(b[0])-alf.index(a[0])) % len(alf))
    result = collections.Counter()
    for item in keys:
        result[item] += 1
    for item in result:
        result[item] = result[item] / len(keys)
    result = sorted(result.items(), key=lambda x: -x[1])
    return result


def blocks_of_size(table_crypt, around):
    for index, item in enumerate(table_crypt):
        table_crypt[index][1] = round(item[1], around)
        print(table_crypt[index][1])

    block_count = []
    tmp = 0
    i = table_crypt[0][1]

    for ind in range(len(table_crypt)):
        if table_crypt[ind][1] == i:
            tmp += 1
        else:
            block_count.append(tmp)
            tmp = 1
            i = table_crypt[ind][1]
    # [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 4, 1, 2, 1, 2, 3]
    # [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 4, 1, 2, 1, 2, 3]
    # [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 4, 1, 2, 1, 2, 3]
    print(block_count)
    if tmp != 0:
        block_count.append(tmp)
    return block_count


def make_mas_sub(block, alf_ot, alf_crypt):
    result = []

    def rec(table, answer, deep, l):
        if len(answer) == l:
            result.append(copy(answer))
            return

        for item in table[deep][1]:
            if item not in answer:
                answer.append(item)
                rec(table, answer, deep + 1, l)
                answer.pop()
    k = 0
    mas = []
    values = []
    for item in block:
        for i in range(item):
            for j in range(item):
                values.append(alf_crypt[k+j])
            mas.append((alf_ot[k+i], values))
            values = []
        k += item
    rec(mas, [], 0, k)

    return result


def sub_keys(mas, alf, alf_ot):
    keys = []
    for item in mas:
        tmp = ''
        for i in alf:
            tmp += item[alf_ot.index(i)]
        keys.append(tmp)

    return keys

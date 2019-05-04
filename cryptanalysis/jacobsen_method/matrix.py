import collections


def del_not_alf(text, alf):
    new_text = ''
    for item in text:
        if item in alf:
            new_text += item
    return new_text


def get_reference_matrix(text, alf):
    text = del_not_alf(text, alf)

    mat = [[0 for j in range(len(alf))] for i in range(len(alf))]
    table = collections.Counter()
    for i in range(len(text)-1):
        table[text[i]+text[i+1]] += 1
    bigrams_sum = sum(table.values())
    for item in table:
        table[item] = table[item] / bigrams_sum

    for i in range(len(alf)):
        for j in range(len(alf)):
            if str(alf[i] + alf[j]) in table:
                mat[i][j] = table[alf[i] + alf[j]]
            else:
                mat[i][j] = 0

    return mat

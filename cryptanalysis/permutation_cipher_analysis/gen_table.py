from pprint import pprint


def text_division(text, l):
    blocks = []
    for i in range(0, len(text), l):
        blocks.append(text[i:i + l])
    blocks.pop()

    return blocks


def make_table(blocks, fb, l):
    table = [[' ' for y in range(l)] for x in range(l)]
    for i in range(l):
        for j in range(l):
            if i == j:
                table[i][j] = 'x'
            # else:
            #     table[i][j] = ' '
    # pprint(table)
    for i in range(l):
        for j in range(l):
            for item in blocks:
                bi = '{}{}'.format(item[j], item[i])
                if bi in fb:
                    # print(bi)
                    table[j][i] = 'x'
                    break
    return table

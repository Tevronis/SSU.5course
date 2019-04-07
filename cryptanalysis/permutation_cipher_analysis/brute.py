from copy import copy


def make_keys(forest, l):
    result = []
    tmp = []

    def rec(forest_):
        for k, v in forest_.items():
            tmp.append(k)
            if not v:
                if len(tmp) == l:
                    result.append(copy(list(map(int, tmp))))
            for item_dict in v:
                rec(item_dict)
            tmp.pop()
    rec(forest)
    return result


def modify_keys(keys):
    result = []
    for item in keys:
        tmp = []
        for i in range(len(item)):
            tmp.append(item.index(i))
        result.append(tmp)
    return result


def decryption(key, text):
    result = ''
    for i in range(len(key)):
        for j in range(len(key)):
            if key[j] == i:
                result += text[j]
                break
    return result


def decrypt_it(name, s):
    fout = open('answers.txt', 'w', encoding='utf-8')
    for i in range(len(s)):
        key = s[i]
        fout.write(str(key) + '\n')
        with open(name + '.txt', 'r', encoding='utf-8') as fin:
            text = fin.read(len(key))
            while text:
                result = decryption(key, text)
                fout.write(result)
                text = fin.read(len(key))
            fout.write('\n\n\n')
    fout.close()

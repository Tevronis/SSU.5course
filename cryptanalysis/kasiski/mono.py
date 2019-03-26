import random


def permutation(length):
    mas = [item for item in range(length)]

    used = [False]*len(mas)
    tmp = 0
    used[0] = True
    while not all(used):
        ran = random.randint(0, len(mas)-1)
        if used[ran]:
            continue
        mas[tmp], mas[ran] = mas[ran], mas[tmp]
        used[ran] = True
        tmp = ran

    return mas


def is_mono(mas):
    used = [False] * len(mas)
    used[mas[0]] = True
    result = [mas[0]]
    while len(result) != len(mas):
        used[mas[result[-1]]] = True
        result.append(mas[result[-1]])
    if all(used):
        return True
    return False


def gen_key(length):
    mas = permutation(length)

    while not is_mono(mas):
        mas = permutation(length)

    return mas


def encryption(key, text):
    result = ''
    options = open('alph.txt', 'r').read().strip()
    while len(key) != len(text):
        a = random.randint(0, len(options)-1)
        tmp = options[a]
        text += tmp

    for i in range(len(key)):
        result += text[key[i]]

    return result


def decryption(key, text):
    result = ''
    for i in range(len(key)):
        for j in range(len(key)):
            if key[j] == i:
                result += text[j]
                break
    return result

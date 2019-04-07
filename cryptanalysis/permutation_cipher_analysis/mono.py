import random


def permutation(length):
    mas = []
    for i in range(0, length):
        mas.append(i)
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
    used = [False]*len(mas)
    used[mas[0]] = True
    result = [mas[0]]
    while len(result) != len(mas):
        used[mas[result[len(result)-1]]] = True
        result.append(mas[result[len(result)-1]])
    if all(used):
        return True
    return False


def gen_key(length):
    # mas = permutation(length)
    # ran = random.randint(0, len(mas) - 1)
    # result = [mas[ran]]
    # mas = [3, 0, 4, 5, 1, 2]
    # result = [mas[0]]
    # while len(result) != len(mas):
    #     result.append(mas[result[len(result)-1]])
    # return result
    mas = permutation(length)
    while is_mono(mas) is False:
        mas = permutation(length)
    return mas


def encryption(key, text):
    options = 'абвгдеёжзийклмнопрстуфхцч'
    while len(key) != len(text):
        a = random.randint(0, len(options)-1)
        tmp = options[a]
        text += tmp
    result = ''
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


if __name__=='__main__':
    a = set()
    for i in range(100):
        a.add(tuple(permutation(5)))
    print('\n'.join(map(str, sorted(a))))

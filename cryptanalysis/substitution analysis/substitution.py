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
    mas = permutation(length)
    while is_mono(mas) is False:
        mas = permutation(length)
    return mas


def make_substitution(alf):
    l = len(alf)
    key = gen_key(l)
    ans = ''
    for item in key:
        ans += alf[item]
    return ans


def make_shift(l):
    shift = random.randint(1, l-1)
    return shift


def encoding_shift(text, alf, key):
    text = text.lower()
    ans = ''
    for item in text:
        # if str(ord(item)) == '160':
        #     item = ' '
        if item in alf:
            for i in range(len(alf)):
                if item == alf[i]:
                    ans += alf[(i+key) % len(alf)]
                    break
    return ans


def decoding_shift(text, alf, key):
    ans = ''
    for item in text:
        for i in range(len(alf)):
            if item == alf[i]:
                ans += alf[(i-key) % len(alf)]
                break
    return ans


def encoding_sub(text, alf, key):
    text = text.lower()
    # print(key)
    # print(alf)
    ans = ''
    for item in text:
        if str(ord(item)) == '160':
            item = ' '
        if item in alf:
            # print(' fdfds "' + str(ord(item)))
            ans += key[alf.index(item)]
    return ans


def decoding_sub(text, alf, key):
    text = text[:1000]
    ans = ''
    for item in text:
        if item not in key:
            ans += ' '
        else:
            ans += alf[key.index(item)]
    return ans



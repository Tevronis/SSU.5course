import random


def cut_text(text, size):
    if len(text) < size:
        return -1
    else:
        return text[:size]


def gen_text(alf, size):
    text = ''
    while len(text) != size:
        text += alf[random.randint(0, len(alf)-1)]
    return text


def del_not_alf(text, alf):
    text = text.lower()
    text2 = ''
    for i in range(len(text)):
        if text[i] in alf:
            text2 += text[i]
    return text2

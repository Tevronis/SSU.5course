
def del_punctuations(text):
    str = open('del.txt', 'r', encoding='utf-8').read().strip()
    charr = set()
    for i in str:
        charr.add(i)
    charr.add('\ufeff')
    charr.add('\xa0')
    charr.add('\xee')
    charr.add('\x97')
    charr.add('\xcb')
    text = text.lower()
    text2 = ''
    for i in range(len(text)):
        if text[i] not in charr:
            text2 += text[i]
        else:
            text2 += ' '
    # open('text_new.txt', 'w').write(text2)
    return text2


def explore_text(text):
    alf = set()
    bigrams = set()
    for i in range(len(text)-1):
        alf.add(text[i])
        bigrams.add(text[i] + text[i+1])
    alf.add(text[len(text)-1])
    return alf, bigrams


def get_forbidden_bigrams(alf, bigrams):
    fb = set()
    all = {x + y for x in alf for y in alf}
    for item in all:
        if item not in bigrams:
            fb.add(item)
    return fb





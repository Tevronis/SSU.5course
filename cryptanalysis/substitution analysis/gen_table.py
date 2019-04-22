import collections


def open_table(text, alf):
    result = collections.Counter()
    text = text.lower()
    for item in text:
        if str(ord(item)) == '160':
            item = ' '
        if item in alf:
            result[item] += 1
    res_len = sum(result.values())
    for item in result:
        result[item] = result[item] / res_len
    result = sorted(result.items(), key=lambda x: -x[1])
    return result


def crypt_table(text, alf):
    result = collections.Counter()
    for item in text:
        result[item] += 1
    for item in result:
        result[item] = result[item] / len(text)
    for item in alf:
        if item not in text:
            result[item] = 0
    result = sorted(result.items(), key=lambda x: -x[1])
    return result





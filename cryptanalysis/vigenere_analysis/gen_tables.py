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


def gen_ot_alf(table_ot):
    return ''.join([item[0] for item in table_ot])


def ot_dict(text, alf):
    # symbs = ' !\'()*,-.'
    result = collections.Counter()
    text = text.lower()
    new_text = ''
    for i in range(len(text)):
        if text[i] not in alf:
            new_text += ' '
        else:
            new_text += text[i]
    text = new_text
    tmp = ''
    for i in range(1, len(text)):
        if text[i] in alf and text[i] != ' ' and text[i-1] == ' ':
            tmp += text[i]
            i += 1
            while text[i] in alf and text[i] != ' ':
                tmp += text[i]
                i += 1
        if tmp != '':
            result[tmp] += 1
        tmp = ''
    for item in result:
        result[item] = result[item] / len(text)
    result = sorted(result.items(), key=lambda x: -x[1])
    # pprint(result)
    return result



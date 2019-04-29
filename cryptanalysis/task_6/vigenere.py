
def del_not_alf(text, alf):
    text = text.lower()
    result = ''
    for i in range(len(text)):
        if text[i] in alf:
            result += text[i]
    return result


def vigenere_encryption(text, key, alf):
    ans = ''
    for i in range(len(text)):
        idx = (alf.index(text[i]) + alf.index(key[i % len(key)])) % len(alf)
        ans += alf[idx]
    return ans


def vigenere_decryption(text, key, alf):
    ans = ''
    for i in range(len(text)):
        idx = (alf.index(text[i]) - alf.index(key[i % len(key)]) + len(alf)) % len(alf)
        ans += alf[idx]
    return ans


def vigenere_decryption_with(text, key, alf):
    ans = ''
    for i in range(len(text)):
        if key[i % len(key)] not in alf:
            ans += '*'
        else:
            idx = (alf.index(text[i]) - alf.index(key[i % len(key)]) + len(alf)) % len(alf)
            ans += alf[idx]
    return ans

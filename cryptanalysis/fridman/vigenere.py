
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


def shift(text, l):
    # ans = ''
    # for i in range(len(text)-l):
    #     ans += text[(i+l) % len(text)]
    return text[l:]

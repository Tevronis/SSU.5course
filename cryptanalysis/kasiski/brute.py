from math import factorial

import mono


def brute_force(l):
    n = factorial(l-1)
    s = set()
    while len(s) != n:
        t = tuple(mono.gen_key(l))
        s.add(t)
    return sorted(s)


def decrypt_it(s):
    fout = open('answers.txt', 'w')
    for i in range(len(s)):
        key = s[i]
        fout.write(str(key) + '\n')
        with open("crypt.txt", 'r') as fin:
            text = fin.read(len(key))
            while text:
                result = mono.decryption(key, text)
                fout.write(result)
                text = fin.read(len(key))
            fout.write('\n\n\n')
    fout.close()



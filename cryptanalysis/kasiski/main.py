import brute
import metod_kasiski
import mono


def permutation_cipher():
    cmd = int(input('1 - зашифровать\n'
                    '2 - расшифровать\n'
                    '>> '))
    if cmd == 1:
        length = int(input('длина ключа: '))

        key = mono.gen_key(length)

        open('key.txt', 'w').write(' '.join(map(str, key)))

        with open("text.txt", 'r') as fin, open('crypt.txt', 'w') as fout:
            text = fin.read(len(key))
            while text:
                result = mono.encryption(key, text)
                fout.write(result)
                text = fin.read(len(key))

        with open('len_key.txt', 'w') as f:
            f.write(str(len(key)))
    if cmd == 2:
        key = list(map(int, open('key.txt').read().strip().split(' ')))
        fout = open('decrypt.txt', 'w')
        with open("crypt.txt", 'r') as fin:
            text = fin.read(len(key))
            while text:
                result = mono.decryption(key, text)
                fout.write(result)
                text = fin.read(len(key))
        fout.close()


def main():
    mod = int(input('1 - шифр простой перестановки \n'
                    '2 - тест Казиски по вычислению ключа\n'
                    '3 - перебор ключей\n'
                    '>> '))
    if mod == 1:
        permutation_cipher()

    if mod == 2:
        n = int(input('максимальная длина подстроки: '))
        for i in range(3, n + 1):
            print(metod_kasiski.get_substrings(i))

    if mod == 3:
        n = int(open('len_key.txt').read().strip())
        brute.decrypt_it(brute.brute_force(n))


if __name__ == '__main__':
    main()

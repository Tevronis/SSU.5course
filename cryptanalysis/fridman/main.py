import index
import modify_text
import vigenere


def main():
    mod = int(input('1 - подсчет индекса совпадений  \n2 - шифр Виженера'
                    '\n'))
    if mod == 1:
        mod_rand = int(input('1 - генерация случайных последовательностей'
                             '\n2 - использование готовых текстов\n'
                             '3 - готовые тексты со сдвигом\n'))
        mod_alf = int(input('1 - английский алфавит\n'
                            '2 - русский алфавит\n'))
        if mod_alf == 1:
            with open('english.txt', 'r') as fin:
                alf = fin.read()
        else:
            with open('russian.txt', 'r') as fin:
                alf = fin.read()

        if mod_rand == 1:
            l = int(input('введите длину текста: '))
            a = modify_text.gen_text(alf, l)
            with open('rand_a.txt', 'w') as finra:
                finra.write(a)
            b = modify_text.gen_text(alf, l)
            with open('rand_b.txt', 'w') as finrb:
                finrb.write(b)
            print('индекс совпадения: ' +
                  str(round(index.overlap_index(a, b), 5) * 100))

            # if mod2 == 2:
            print('средний индекс совпадения: ' +
                  str(round(index.average_overlap_index(a, b, alf), 5) * 100))

        if mod_rand == 3:
            name_a = input('файл 1: ')
            for i in range(1, 15+1):
                with open(name_a + '.txt', 'r') as fin_a:
                    a = fin_a.read()

                with open(name_a + '+' + str(i) + '.txt', 'r') as fin_b:
                    b = fin_b.read()
                a = modify_text.del_not_alf(a, alf)
                b = modify_text.del_not_alf(b, alf)

                if len(a) > len(b):
                    l = len(b)
                else:
                    l = len(a)

                if len(a) != len(b):
                    if modify_text.cut_text(a, l) != -1:
                        a = modify_text.cut_text(a, l)

                    if modify_text.cut_text(b, l) != -1:
                        b = modify_text.cut_text(b, l)

                # print(len(a))
                # print(len(b))

                print('индекс совпадения ' + name_a + ' и ' + name_a + '+' + str(i) + ': '
                      + str(round(index.overlap_index(a, b), 5) * 100))

        if mod_rand == 2:
            # l = int(input('введите длину текста: '))
            name_a = input('файл 1: ')
            name_b = input('файл 2: ')
            with open(name_a + '.txt', 'r') as fin_a:
                a = fin_a.read()

            with open(name_b + '.txt', 'r') as fin_b:
                b = fin_b.read()

            a = modify_text.del_not_alf(a, alf)
            b = modify_text.del_not_alf(b, alf)
            # может быть сделать длину равную длине меньшего текста?

            if len(a) > len(b):
                l = len(b)
            else:
                l = len(a)

            if len(a) != len(b):
                if modify_text.cut_text(a, l) != -1:
                    a = modify_text.cut_text(a, l)
                else:
                    print('длина первого текста не соответствует требованию')
                    exit()
                if modify_text.cut_text(b, l) != -1:
                    b = modify_text.cut_text(b, l)
                else:
                    print('длина второго текста не соответствует требованию')
                    exit()
                # with open(name_a + '_remade.txt', 'w') as fouta:
                #     fouta.write(str(a))
                # with open(name_b + '_remade.txt', 'w') as foutb:
                #     foutb.write(str(b))
            print(len(a))
            print(len(b))

            # mod2 = int(input('1 - индекс совпадения\n'
            #                  '2 - средний индекс совпадения\n3'))
            #
            # if mod2 == 1:
            print('индекс совпадения: ' +
                  str(round(index.overlap_index(a, b), 5) * 100))

            # if mod2 == 2:
            print('средний индекс совпадения: ' +
                  str(index.average_overlap_index(a, b, alf) * 100))

    if mod == 2:
        mod_alf = int(input('1 - английский алфавит\n'
                            '2 - русский алфавит\n'))
        if mod_alf == 1:
            with open('english.txt', 'r') as fin:
                alf = fin.read()
        else:
            with open('russian.txt', 'r') as fin:
                alf = fin.read()

        mod_vigenere = int(input('1 - зашифровать\n2 - дешифровать\n'
                                 '3 - сдвинуть текст\n4 - сдвинуть в интервале\n'))

        if mod_vigenere == 1:
            name = input('введите название файла: ')
            with open(name + '.txt', 'r') as fin:
                text = fin.read()
            key = open('key.txt').read().strip()
            # key = input('ключ: ').strip()
            # open('key.txt', 'w').write(str(key))
            text = modify_text.del_not_alf(text, alf)

            crypt = vigenere.vigenere_encryption(text, key, alf)
            open(name + 'cr.txt', 'w').write(str(crypt))

        if mod_vigenere == 2:
            name = input('введите название файла: ')
            text = open(name + '.txt', 'r').read().strip()
            key = open('key.txt').read().strip()
            decrypt = vigenere.vigenere_decryption(text, key, alf)
            open('decrypt.txt', 'w').write(str(decrypt))

        if mod_vigenere == 3:
            name = input('введите название файла: ')
            with open(name + '.txt', 'r') as fin:
                text = fin.read()
            # l = int(open('l_shift.txt', 'r').read().strip())
            l = int(input('введите сдвиг l: '))
            text = vigenere.shift(text, l)
            open(name + '+' + str(l) + '.txt', 'w').write(str(text))

        if mod_vigenere == 4:
            name = input('введите название файла: ')
            with open(name + '.txt', 'r') as fin:
                text = fin.read()
            # l = int(open('l_shift.txt', 'r').read().strip())
            l1 = int(input('введите минимальный сдвиг l min: '))
            l2 = int(input('введите максимальный сдвиг l max: '))
            for i in range(l1, l2+1):
                ans = vigenere.shift(text, i)
                open(name + '+' + str(i) + '.txt', 'w').write(str(ans))


if __name__ == '__main__':
    main()

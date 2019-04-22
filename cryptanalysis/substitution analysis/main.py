import gen_table
import isotone_mapping
import substitution


def keygen():
    alf = open('alphabet.txt', 'r').read().strip()
    key = substitution.make_substitution(alf)
    print('alphabet:', alf)
    print('     key:', key)
    with open('key_substitution.txt', 'w') as fout:
        fout.write(alf + '\n')
        fout.write(key)
    open('key_sub.txt', 'w').write(str(key))
    print('\nсохранен файл: key_substitution.txt')
    
    
def encryption():
    mod_encoding = int(input('1 - сдвиг\n2 - перестановка\n> '))
    if mod_encoding == 1:
        alf = open('alphabet.txt', 'r').read().strip()
        key = int(open('key_shift.txt', 'r').read().strip())
        name = input('файл открытого текста: ')
        with open(name + '.txt', 'r') as fin:
            text = fin.read()
        text = substitution.encoding_shift(text, alf, key)
        with open('crypt.txt', 'w') as fout:
            fout.write(text)
        print('\nсохранен файл: crypt.txt')

    if mod_encoding == 2:
        alf = open('alphabet.txt', 'r').read().strip()
        key = open('key_sub.txt', 'r').read()
        name = input('файл открытого текста: ')
        with open(name + '.txt', 'r') as fin:
            text = fin.read()
        text = substitution.encoding_sub(text, alf, key)
        with open('crypt.txt', 'w') as fout:
            fout.write(text)
        print('\nсохранен файл: crypt.txt')


def create_table_freq_ot():
    name = input('файл открытого текста: ')
    with open(name + '.txt', 'r') as fin:
        text = fin.read()
    alf = open('alphabet.txt', 'r').read().strip()
    table = gen_table.open_table(text, alf)
    with open('ot_table.txt', 'w') as fout:
        for k, v in table:
            fout.write('{} {:.7f}\n'.format(k, v))
    print('сохранен файл: ot_table.txt')
    
    
def create_table_freq_crypt():
    with open('crypt.txt', 'r') as fin:
        text = fin.read()
    alf = open('alphabet.txt', 'r').read().strip()
    table = gen_table.crypt_table(text, alf)
    with open('crypt_table.txt', 'w') as fout:
        for k, v in table:
            fout.write('{} {:.7f}\n'.format(k, v))
    print('сохранен файл: crypt_table.txt')


def create_isoton_list():
    table_ot = []
    with open('ot_table.txt', 'r') as fin_ot:
        for item in fin_ot:
            table_ot.append([item[0], float(item[2:])])
    table_crypt = []
    with open('crypt_table.txt', 'r') as fin_cr:
        for item in fin_cr:
            table_crypt.append([item[0], float(item[2:])])
    alf = open('alphabet.txt', 'r').read().strip()

    mod2 = int(input('1 - сдвиг\n2 - перестановка\n> '))
    if mod2 == 1:
        keys = isotone_mapping.shift_keys(table_ot, table_crypt, alf)
        for item in keys:
            print('сдвиг ' + str(item[0]) + ' с частотой ' + str(item[1]))
        open('ans_shift_keys.txt', 'w')
        for item in keys:
            open('ans_shift_keys.txt', 'a').write(str(item[0]) + ' ' + str(item[1]) + '\n')
        print('сохранен файл: ans_shift_keys.txt')

    if mod2 == 2:
        alf_ot = ''
        for item in table_ot:
            alf_ot += item[0]

        alf_crypt = ''
        for item in table_crypt:
            alf_crypt += item[0]

        around = int(input('округлить до (знаков после запятой): '))
        blocks = isotone_mapping.blocks_of_size(table_crypt, around)
        result = isotone_mapping.make_mas_sub(blocks, alf_ot, alf_crypt)

        keys = isotone_mapping.sub_keys(result, alf, alf_ot)
        print('количество ключей: ' + str(len(keys)))
        with open('ans_sub_keys.txt', 'w') as fout:
            for item in keys:
                fout.write(item + '\n')
        print('сохранен файл: ans_sub_keys.txt')


def verify_key_list():
    with open('crypt.txt', 'r') as fin:
        text = fin.read()
    alf = open('alphabet.txt', 'r').read().strip()
    mod = int(input('1 - сдвиг\n2 - перестановка\n> '))

    if mod == 1:
        keys = []
        with open('ans_shift_keys.txt', 'r') as fin:
            for line in fin:
                keys.append(int(line.split()[0]))

        open('ans_shift.txt', 'w')
        with open('ans_shift.txt', 'a') as fout:
            for item in keys:
                fout.write(str(item) + '\n')
                fout.write(substitution.decoding_shift(text, alf, item))
                fout.write('\n\n\n')
        print('сохранен файл: ans_shift.txt')

    if mod == 2:
        keys = []
        with open('ans_sub_keys.txt', 'r') as fin:
            for line in fin:
                line = line[:-1]
                keys.append(line)
        open('ans_sub.txt', 'w')
        with open('ans_sub.txt', 'a') as fout:
            for item in keys:
                fout.write(item + '\n')
                fout.write(substitution.decoding_sub(text, alf, item))
                fout.write('\n\n\n\n')
        print('сохранен файл: ans_sub.txt')


def main():
    mod = int(input('1 - генерация ключа перестановки\n'
                    '2 - шифрование\n'
                    '3 - создание таблицы частот символов открытых сообщений\n'
                    '4 - создание таблицы частот символов в криптограмме\n'
                    '5 - создание списка изотонных отображений\n'
                    '6 - проверка списка ключей на криптограмме\n> '))
    if mod == 1:
        keygen()

    if mod == 2:
        encryption()

    if mod == 22:  # дешифрование по сдвигу
        alf = open('alphabet.txt', 'r').read().strip()
        key = int(open('key_shift.txt', 'r').read().strip())
        with open('crypt.txt', 'r') as fin:
            text = fin.read()
        text = substitution.decoding_shift(text, alf, key)
        with open('decrypt.txt', 'w') as fout:
            fout.write(text)

    if mod == 33:  # дешифрование по перестановке
        alf = open('alphabet.txt', 'r').read().strip()
        key = open('key_sub.txt', 'r').read().strip()
        with open('crypt.txt', 'r') as fin:
            text = fin.read()
        text = substitution.decoding_sub(text, alf, key)
        with open('decrypt.txt', 'w') as fout:
            fout.write(text)

    if mod == 3:
        create_table_freq_ot()

    if mod == 4:
        create_table_freq_crypt()

    if mod == 5:
        create_isoton_list()

    if mod == 6:
        verify_key_list()


if __name__ == '__main__':
    main()

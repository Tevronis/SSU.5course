import os
import sys
import argparse
import hashlib
import pefile
from utils import disable_file_system_redirection

MODE_TEST = False
MODE_SIGNATURE = 1
MODE_HASH = 2

SIGNATURE = '00 00 00 61 74 2e 70 64 62 00 00'
HASH = 'e5c69016d2322f7aa19b02e67194d72a'

sys.stdout = open('log.txt', 'w')

mm = []
for item in SIGNATURE.split():
    mm.append(int(item, 16))
SIGNATURE = bytes(mm)
print('SIGNATURE const: ', SIGNATURE)


def analyze_signature(code):
    if code is None:
        return False
    if SIGNATURE in code:
        print('SIGNATURE was found!')
        return True
    return False


def analyze_hash(code):
    if code is None:
        return False
    hash_md5 = hashlib.md5(code)
    if hash_md5.hexdigest() == HASH:
        print('Hash of two files is equal!')
        return True
    return False


def checkup(file, mode):
    try:
        pe = pefile.PE(name=file, fast_load=True)
    except pefile.PEFormatError:
        return False
    except PermissionError:
        print('Permission error to file: {}'.format(file))
        return False
    except Exception:
        return False

    result = False

    """test code"""
    if MODE_TEST:
        print(file)
        print("Entry point: ", hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))

        for section in pe.sections:
            print(section.name, hex(section.VirtualAddress), hex(section.Misc_VirtualSize), section.SizeOfRawData,
                  hex(section.PointerToRawData),
                  hex(section.Characteristics))
        s_code = pe.sections[0].get_data()
        print('size of code: ', len(s_code))
    """\test code"""
    if pe.is_dll():
        return result
    code_section = None
    for section in pe.sections:
        if hex(section.Characteristics) == '0x60000020':  # если секция явялется секцией кода
            code_section = section.get_data()
            break

    if mode == MODE_SIGNATURE:
        with open(file, 'rb') as f:
            result = analyze_signature(f.read())
    elif mode == MODE_HASH:
        result = analyze_hash(code_section)
    else:
        raise ValueError('Параметр mode некорректный!')

    pe.close()
    return result


def analyze_dir_tree(path, mode):
    if os.path.isfile(path):
        if checkup(path, mode):
            print('File was found!', path)
            return False #True

    try:
        if os.path.isdir(path):
            for file in os.listdir(path):
                if analyze_dir_tree(path + '\\' + file, mode):
                    return True
    except PermissionError:
        print('Permission error to dir: {}'.format(path))
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=int, default=2)
    parser.add_argument('--dir', type=str)
    args = parser.parse_args(sys.argv[1:])

    with disable_file_system_redirection():
        analyze_dir_tree(args.dir, args.mode)


if __name__ == '__main__':
    main()

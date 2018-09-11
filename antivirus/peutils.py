"""
    Tool for intersect sequence bytes in PE files
    By Mike Ents
"""

import pefile
import collections

TEMPLATE_LENGTH = 12  # Length of bytes sequence


def sig_filter(bts: list):
    cnt = collections.Counter()
    for item in bts:
        cnt[item] += 1
        if cnt[item] + 1 >= len(bts):
            return False

    pair = 0
    start = [item for item in bts if item != 0][0]
    start = bts.index(start)
    for idx in range(start, len(bts)):
        if idx + 1 < len(bts) and bts[idx] != 0 and bts[idx + 1] == 0:
            pair += 1
    if pair > len(bts) // 3:
        return False
    return True


def hex_present(item):
    return str(hex(item))[2:]


def main():
    files = input('Please enter files splited by space: ').split()

    open_files = []
    section_code_positions = []
    section_code_sizes = []
    for file in files:
        f = open(file, 'rb').read()
        open_files.append(f)
        try:
            pe = pefile.PE(file, fast_load=True)
        except Exception:
            raise Exception('File {} do not loaded!'.format(file))
        section_code_positions.append(pe.sections[0].PointerToRawData)
        section_code_sizes.append(pe.sections[0].SizeOfRawData)

    start_file = open_files[0]
    first_file_pos = section_code_positions[0]
    out = []
    while first_file_pos + TEMPLATE_LENGTH <= len(start_file):
        temp = start_file[first_file_pos: first_file_pos + TEMPLATE_LENGTH]
        positions = []
        for file, s_find_pos, s_find_size in zip(open_files[1:], section_code_positions[1:], section_code_sizes[1:]):
            pos = file.find(temp, s_find_pos, s_find_pos + s_find_size)
            positions.append(pos)
            if pos <= 0:  # Если шаблон не найден хоть в одном файле, то завершаем иттерацию
                break
        else:
            smt_signature = []
            while first_file_pos < len(start_file):
                for idx, file in enumerate(open_files[1:]):
                    if not (positions[idx] < len(file) and start_file[first_file_pos] == file[positions[idx]]):
                        break
                else:
                    smt_signature.append(start_file[first_file_pos])
                    for idx in range(len(positions)):
                        positions[idx] += 1
                    first_file_pos += 1
                    continue
                break
            if smt_signature:
                out.append(smt_signature)
            continue
        first_file_pos += 1
    out = filter(sig_filter, out)
    print('Potential signatures:')
    for num, item in enumerate(out):
        print(str(num) + ') ' + ' '.join(map(hex_present, item)))


if __name__ == '__main__':
    main()

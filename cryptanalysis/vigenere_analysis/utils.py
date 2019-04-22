
def read_txt(filename):
    with open(filename + '.txt', 'r') as fin:
        result = fin.read()
    return result

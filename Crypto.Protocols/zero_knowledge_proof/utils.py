import json


def read_param(file, param):
    with open(file) as f:
        ff = json.load(f)
    return ff[param]


def save_param(file, paramname, param):
    try:
        with open(file, 'r') as f:
            it = json.load(f)
    except:
        it = {}
    it[paramname] = param
    with open(file, 'w') as f:
        json.dump(it, f, indent=True)

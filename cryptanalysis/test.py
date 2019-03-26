# -*- coding: utf-8 -*-
import json


def f():
    def dfs(u, tree_):
        for v in range(len(table[u])):
            if not used[v] and table[u][v] == 1:
                used[v] = 1
                tree_.append({v: []})
                dfs(v, tree_[-1][v])
                used[v] = 0

    table = [[0, 0, 0, 0, 1],
             [0, 0, 0, 1, 0],
             [0, 0, 0, 1, 0],
             [1, 0, 1, 0, 0],
             [0, 0, 1, 0, 0]]

    max_value = 0
    roots = []
    for j in range(len(table)):
        cnt = 0
        for i in range(len(table)):
            if table[i][j] == 0:
                cnt += 1
        if cnt > max_value:
            max_value = cnt
            roots = []
        if cnt == max_value:
            roots.append(j)
    print('Roots of trees: ', roots)
    tree = {}
    for root in roots:
        print('Current root: ', root)
        used = [0 for i in range(len(table))]
        tree[root] = []

        dfs(root, tree[root])

        with open('{}_tree.json'.format(root), 'w') as fout:
            json.dump(tree, fout, indent=2)


# 1 3 0 4 2
# 1 3 2

def rec(d):
    for k, v in d.items():
        if v:
            print(k, ': ', v)
        for item_dict in v:
            rec(item_dict)


if __name__ == '__main__':
    f()
    with open('1_tree.json', 'r') as fin:
        trees = json.load(fin)
    rec(trees)

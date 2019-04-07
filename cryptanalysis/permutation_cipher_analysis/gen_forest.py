import json


def modify_table(table):
    l = len(table[0])
    ans = [[0 for y in range(l)] for x in range(l)]
    for i in range(l):
        for j in range(l):
            if table[i][j] == ' ':
                ans[i][j] = 1
    # print(ans)
    return ans


def rec(d):
    for k, v in d.items():
        if v:
            print(k, ': ', v)
        for item_dict in v:
            rec(item_dict)


def make_forest(table):
    def dfs(u, tree_):
        for v in range(len(table[u])):
            if not used[v] and table[u][v] == 1:
                used[v] = 1
                tree_.append({v: []})
                dfs(v, tree_[-1][v])
                used[v] = 0
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
    forest = {}
    for root in roots:
        used = [0 for i in range(len(table))]
        forest[root] = []
        used[root] = 1
        dfs(root, forest[root])

        with open('forest.json', 'w') as fout:
            json.dump(forest, fout, indent=2)
    # rec(forest)



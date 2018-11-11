import random
import sys
import graph
import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.isomorphism as iso

# создает изоморфный граф, причем цикл там правильный будет
def create_iso_graph(g):
    iso = {}

    degree = len(g.edges)

    values = []
    for i in range(len(g.edges)):
        values.append(i)

    items = list(range(len(values)))
    # print(items)
    random.shuffle(items)
    # print(items)
    items = iter(items)
    for i in range(degree):
        #next = random.randint(0, len(values) - 1)
        iso.update({i: values[next(items)]})

    _edges = []
    for i in range(degree):
        _edges.append([])

    for i in range(degree):
        for j in range(len(g.edges[i])):
            _edges[iso[i]].append(iso[g.edges[i][j]])

    _cycle = [0 for i in range(len(g.cycle))]
    for i in range(len(g.cycle)):
        _cycle[i] = iso[g.cycle[i]]

    return graph.Graph(_edges, _cycle)


def Generate_List_all_edges(degree):
    # список всех возможных ребер
    all_edges = []
    for i in range(degree):
        for j in range(i + 1, degree):
            all_edges.append([i, j])

    return all_edges


def generate_graph(degree):
    # список всех возможных ребер
    all_edges = Generate_List_all_edges(degree)

    cycle = []

    g = []

    for i in range(degree):
        g.append([])

        # вершины для создания цикла
    points = []
    for i in range(1, degree):
        points.append(i)

    prev = 0
    cycle.append(0)
    for i in range(degree - 1):
        next = random.randint(0, len(points) - 1)

        # добавление в граф
        g[points[next]].append(prev)
        g[prev].append(points[next])

        cycle.append(points[next])
        all_edges.remove([min(prev, points[next]), max(prev, points[next])])

        prev = points[next]

        points.pop(next)

    g[prev].append(0)
    g[0].append(prev)
    cycle.append(0)

    all_edges.remove([0, prev])

    # с этого момента в g уже есть Гамильтонов цикл
    # макс.число ребер в графе n(n - 1) / 2

    max_degree = (degree * (degree - 1)) // 2 - degree

    cnt_add_points = random.randint(0, max_degree)

    # добавление рандомного числа ребер в граф с уже имеющимся циклом
    for i in range(cnt_add_points):
        next = random.randint(0, len(all_edges) - 1)

        g[all_edges[next][0]].append(all_edges[next][1])
        g[all_edges[next][1]].append(all_edges[next][0])

        all_edges.pop(next)

    return g, cycle


def draw_graph(edges):
    G = nx.Graph()
    for v in range(len(edges)):
        for ne in edges[v]:
            G.add_edge(v, ne)
    nx.draw_circular(G, with_labels=True)
    plt.show()


def get_matrix(edges, n):
    M = [[0 for i in range(n)] for i in range(n)]
    for idx, edge in enumerate(edges):
        for item in edge:
            M[idx][item] = 1
    return M


def get_networkx_graph(matrix):
    G = nx.DiGraph()
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            try:
                if matrix[i][j]:
                    G.add_edge(i, j)
            except:
                r = 3
    return G


def read_matrixs(dig):
    result = []
    with open('new.txt') as f:
        try:
            while True:
                M = []
                for i in range(dig):
                    M.append(list(map(int, f.readline().split())))
                f.readline()
                if M == [[], [],[],[],[]]:
                    break
                result.append(M)
        except:
            pass
    print(len(result))
    return result


def print_matrix(M):
    for line in M:
        print(' '.join(list(map(str, line))))


def main(args):
    matrixs = read_matrixs(5)
    iso = 0
    niso = 0
    nmatr = []
    for M1 in matrixs:
        f = False
        for M2 in matrixs:
            if M1 != M2:
                G = get_networkx_graph(M1)
                #iso_graph = create_iso_graph(g)
                H = get_networkx_graph(M2)
                if nx.is_isomorphic(G, H):
                    f = True
                    iso += 1
                    print_matrix(M1)
                    print()
                    print_matrix(M2)
                    return
                else:
                    niso += 1
        if f:
            nmatr.append(M1)
    print(len(nmatr))
    print(iso//2, niso//2)


if __name__ == '__main__':
    main(sys.argv)

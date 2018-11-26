# coding=utf-8
import argparse
import random
import sys

import matplotlib.pyplot as plt
import networkx as nx

import utils


class Graph:
    def __init__(self, edges, cycle):
        self.edges = edges
        self.cycle = cycle


def create_iso_graph(g):
    iso = {}

    degree = len(g.edges)

    values = []
    for i in range(len(g.edges)):
        values.append(i)

    items = list(range(len(values)))

    random.shuffle(items)

    items = iter(items)
    for i in range(degree):
        iso.update({i: values[next(items)]})

    _edges = []
    for i in range(degree):
        _edges.append([])

    for i in range(degree):
        for j in range(len(g.edges[i])):
            _edges[iso[i]].append(iso[g.edges[i][j]])

    _cycle = [0 for _ in range(len(g.cycle))]
    for i in range(len(g.cycle)):
        _cycle[i] = iso[g.cycle[i]]
    print(iso.items())
    return Graph(_edges, _cycle), iso


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
        next_edge = random.randint(0, len(points) - 1)

        # добавление в граф
        g[points[next_edge]].append(prev)
        g[prev].append(points[next_edge])

        cycle.append(points[next_edge])
        all_edges.remove([min(prev, points[next_edge]), max(prev, points[next_edge])])

        prev = points[next_edge]

        points.pop(next_edge)

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
        next_edge = random.randint(0, len(all_edges) - 1)

        g[all_edges[next_edge][0]].append(all_edges[next_edge][1])
        g[all_edges[next_edge][1]].append(all_edges[next_edge][0])

        all_edges.pop(next_edge)

    return g, cycle


def draw_graph(edges):
    G = nx.Graph()
    for v in range(len(edges)):
        for ne in edges[v]:
            G.add_edge(v, ne)
    nx.draw_circular(G, with_labels=True)
    plt.show()


def get_matrix(edges, n):
    M = [[0 for _ in range(n)] for i in range(n)]
    for idx, edge in enumerate(edges):
        for item in edge:
            M[idx][item] = 1
    return M


def get_networkx_graph(edges):
    G = nx.Graph()
    for v in range(len(edges)):
        for ne in edges[v]:
            G.add_edge(v, ne)
    return G


def check_iso(G, H, iso):
    HH = [[] for _ in range(len(G))]
    for u, neighbour_v in enumerate(G):
        for v in neighbour_v:
            HH[iso[str(u)]].append(iso[str(v)])
    print(H)
    print(HH)
    return H == HH


def check_gam_cycle(H, cycle):
    n = len(H)
    if len(set(cycle)) != n or cycle[0] != cycle[-1]:
        return False
    used = [0 for _ in range(n)]
    available = [v for v in cycle]
    for v in cycle:
        if v in available:
            used[v] = 1
            available = H[v]
        else:
            return False
    if sum(used) == n:
        return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=1)
    parser.add_argument('-b', type=int)
    parser.add_argument('--draw', action='store_true')
    parser = parser.parse_args()

    if parser.m == 1:  # Пегги
        graph_size = utils.read_param('graph_size', 'size')
        edges, cycle = generate_graph(graph_size)
        utils.save_param('G_graph.param', 'edges', edges)
        utils.save_param('Peggy/G_cycle.param', 'cycle', cycle)
        if parser.draw:
            draw_graph(edges)
    elif parser.m == 2:  # Пегги. генерация изоморфного графа
        edges = utils.read_param('G_graph.param', 'edges')
        cycle = utils.read_param('Peggy/G_cycle.param', 'cycle')
        g = Graph(edges, cycle)
        iso_graph, iso = create_iso_graph(g)
        utils.save_param('H_graph.param', 'edges', iso_graph.edges)
        utils.save_param('Peggy/H_cycle.param', 'cycle', iso_graph.cycle)
        utils.save_param('Peggy/H_iso.param', 'iso', iso)
        if parser.draw:
            draw_graph(iso_graph.edges)
    elif parser.m == 3:  # Виктор
        b = random.randint(0, 1)
        if parser.b:
            b = parser.b
        utils.save_param('b.param', 'b', b)
    elif parser.m == 4:  # Пегги исполняет просьбу исходя из b
        b = utils.read_param('b.param', 'b')
        if b == 0:
            iso = utils.read_param('Peggy/H_iso.param', 'iso')
            utils.save_param('iso_GH.param', 'iso', iso)
        elif b == 1:
            cycle = utils.read_param('Peggy/H_cycle.param', 'cycle')
            utils.save_param('cycle_in_H.param', 'cycle', cycle)
    elif parser.m == 5:  # Виктор проверяет то что предоставила Пегги
        b = utils.read_param('b.param', 'b')
        if b == 0:
            iso = utils.read_param('iso_GH.param', 'iso')
            G = utils.read_param('G_graph.param', 'edges')
            H = utils.read_param('H_graph.param', 'edges')
            result = check_iso(G, H, iso)
            utils.save_param('result.txt', 'check iso', result)
        elif b == 1:
            cycle = utils.read_param('cycle_in_H.param', 'cycle')
            H = utils.read_param('H_graph.param', 'edges')
            result = check_gam_cycle(H, cycle)
            utils.save_param('result.txt', 'check cycle', result)


if __name__ == '__main__':
    main()

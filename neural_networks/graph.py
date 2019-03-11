# -*- coding: utf-8 -*-
import argparse
import functools
import math
import sys
from operator import mul, add

import collections
import json
import re


def log(text, _exit=False):
    with open('log.log', 'a') as f:
        f.write(text + '\n')
    if _exit:
        exit(-1)


class Graph:
    def __init__(self):
        self.graph = None
        self.backward_view = collections.defaultdict(list)
        self.forward_view = collections.defaultdict(list)
        self.vertexes = set()

    def read_from_json(self, filename):
        with open(filename) as f:
            g = json.load(f)
        self.backward_view = g
        for k, v in self.backward_view.items():
            for item in v:
                if k not in self.forward_view[item[1]]:
                    self.vertexes.add(k)
                    self.vertexes.add(item[1])
                    self.forward_view[item[1]].append([item[0], k])

    def read_graph(self, file_graph):
        with open(file_graph) as f:
            line = f.read()
        r = re.findall('(\(.*?\))', line)
        if not r:
            log("Некорретный формат входных данных: (..), (..)", True)
        for item in r:
            if not re.match('\([\w\d]+, ?[\w\d]+, ?[\d]+\)', item):
                log("Некорретный формат входных данных: (\w\d, \w\d, \d)", True)
        ans = []
        for item in r:
            ans.append([it.strip('() ') for it in item.split(',')])  # (a1, b1, 1)
        self.graph = ans
        for item in self.graph:
            if int(item[2]) in self.backward_view[item[1]]:
                log("Третий параметр ребра должен быть уникален для каждого второго параметра", True)
            self.backward_view[item[1]].append([int(item[2]), item[0]])

        for k, v in self.backward_view.items():
            for item in v:
                if k not in self.forward_view[item[1]]:
                    self.vertexes.add(k)
                    self.vertexes.add(item[1])
                    self.forward_view[item[1]].append([item[0], k])

        return self.graph

    def to_json(self, file_json):
        to_json = collections.defaultdict(list)
        for k, v in self.backward_view.items():
            to_json[k] = list(sorted(v, key=lambda x: x[0]))
        with open(file_json, 'w') as f:
            json.dump(to_json, f, indent=2)

    def exist_cycle(self, ver):
        used = {v: 0 for v in self.vertexes}

        def rec(u):
            used[u] = 1
            if u in self.forward_view.keys():
                for v in self.forward_view[u]:
                    if used[v[1]] == 1:
                        log('Обнаружен цикл с ребром {} {}'.format(u, v), True)
                        raise Exception('Обнаружен цикл с ребром {} {}'.format(u, v))
                    if used[v[1]] == 0:
                        rec(v[1])
            used[u] = 2

        rec(ver)

    def create_function(self, exception=True, replace=None):
        def rec(u):
            if u not in self.backward_view.keys():
                if replace:
                    return replace[u]
                return u
            if replace:
                res = replace[u] + '('
            else:
                res = u + '('
            for v in self.backward_view[u]:
                if replace:
                    res += rec(v[1]) + ','
                else:
                    res += rec(v[1]) + ','
            if res[-1] == ',':
                res = res[:-1]
            return res + ')'

        v = [k for k in self.backward_view.keys() if k not in self.forward_view.keys()]
        v2 = [k for k in self.forward_view.keys() if k not in self.backward_view.keys()]
        # print(self.backward_view.keys(), self.forward_view.keys())
        if len(v) > 1:
            log('Ошибка: сток не единственный, построить функцию не удастся', True)
        if len(v) == 0 and exception:
            log('Обнаружен цикл', True)
        for item in v2:
            self.exist_cycle(item)
        result = rec(v[0])
        return result


def calculate_value(graph, operations):
    to_replace = collections.defaultdict(list)
    for k, sink in graph.backward_view.items():
        for item in sink:
            to_replace[operations[k]].append([item[0], operations[item[1]]])

    def compute(op, values):
        if op.isdigit():
            if len(values):
                raise Exception('число не принимает параметров!')
            return int(op)
        if op == 'exp':
            if len(values) != 1:
                raise Exception('exp принимает один параметр!')
            return math.e ** values[0]
        if op == '*':
            if not len(values):
                raise Exception('* принимает ненулевое количество элементов!')
            return functools.reduce(mul, values)
        if op == '+':
            if not len(values):
                raise Exception('+ принимает ненулевое количество элементов!')
            return functools.reduce(add, values)

    def rec(u):
        res = []
        for v in graph.backward_view[u]:
            res.append(rec(v[1]))
        return compute(operations[u], res)

    sink = [k for k in graph.backward_view.keys() if k not in graph.forward_view.keys()]
    # source = [k for k in graph.forward_view.keys() if k not in graph.backward_view.keys()]
    # print(graph.backward_view.keys(), graph.forward_view.keys())
    result = rec(sink[0])
    print(result)

    with open("temp.json", 'w') as f:
        json.dump(to_replace, f, indent=2)


if __name__ == '__main__':
    m = None
    if len(sys.argv) > 2 and sys.argv[1] == '-m':
        m = int(sys.argv[2])

    g = Graph()
    graph_edge = 'test1.txt'
    if m == 1:
        g.read_graph(graph_edge)
        g.to_json('graph.json')
    if m == 2:
        g.read_graph(graph_edge)
        # g.read_from_json('graph.json')
        fun = g.create_function()
        print(fun)
        open('function', 'w').write(fun)
    if m == 3:
        g.read_graph(graph_edge)
        g.to_json('graph.json')
        # g.read_from_json('graph.json')
        with open('operations.json', 'r') as f:
            operations = json.load(f)
        fun = g.create_function(replace=operations)
        print(fun)
        calculate_value(g, operations)

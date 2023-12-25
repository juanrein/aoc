import os
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt

def parse_input(exclude = []):
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    g = defaultdict(set)

    for line in lines:
        firstlast = line.split(": ")
        first = firstlast[0]
        rest = firstlast[1].split(" ")
        for c in rest:
            if (first, c) not in exclude and (c, first) not in exclude:
                g[c].add(first)
                g[first].add(c)

    graph = nx.Graph()
    for k,v in g.items():
        graph.add_node(k)
        for c in v:
            graph.add_edge(k, c)

    return graph


def plot_graph():
    g = parse_input()

    subax1 = plt.subplots()
    nx.draw(g, with_labels=True)

    plt.show()


g = parse_input([("ttv", "ztc"), ("rpd", "bnv"), ("vfh", "bdj")])

def bfs(g: nx.Graph, start):
    Q = deque()
    visited = set()
    Q.appendleft(start)
    while len(Q) > 0:
        v = Q.pop()
        for c in g.neighbors(v):
            if c not in visited:
                visited.add(c)
                Q.appendleft(c)

    return visited

values = set()
for k in g.nodes:
    component = bfs(g, k)
    values.add(len(component))

print(values)

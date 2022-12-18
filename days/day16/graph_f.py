import math

def makeGraph(data):
    graph = {}
    for name, rate, connections in data:
        graph[name] = {
            "name": name,
            "rate": rate,
            "connections": connections
        }
    return graph

def dijkstra(graph: dict, start: str):
    dist = {}
    prev = {}
    Q = []
    for v in graph.keys():
        dist[v] = math.inf
        prev[v] = None
        Q.append(v)
    dist[start] = 0
    while len(Q) > 0:
        u = min(Q, key=lambda x: dist[x])
        Q.remove(u)
        for v in filter(lambda x: x in Q, graph[u]["connections"]):
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    return dist, prev


def shortestPaths(graph):
    paths = {}
    for start in graph.keys():
        dist, prev = dijkstra(graph, start)
        paths[start] = {"dist": dist, "prev": prev}

    return paths

def expandPaths(paths: dict):
    ex = {k: {} for k in paths.keys()}
    for k in paths.keys():
        for k2 in paths.keys():
            cur = k2
            path = []
            while cur is not None:
                path.append(cur)
                cur = paths[k]["prev"][cur]
            ex[k][k2] = path

    return ex

def makeWGraph(graph):
    paths = shortestPaths(graph)
    expanded = expandPaths(paths)
    clearedPaths = {k:{"c": []} for k in expanded}
    def areDirectlyConnected(k1, k2):
        between = 0
        for c in expanded[k1][k2]:
            if (graph[c]["rate"] != 0 or c == "AA") and c != k1 and c != k2:
                between += 1
        return between <= 0

    for k1 in expanded:
        if graph[k1]["rate"] == 0 and k1 != "AA":
            continue
        for k2 in expanded[k1]:
            if k1 == k2:
                continue
            if graph[k2]["rate"] == 0 and k2 != "AA":
                continue
            clearedPaths[k1][k2] = len(expanded[k1][k2])-1
            if areDirectlyConnected(k1,k2):
                clearedPaths[k1]["c"].append(k2)

    return clearedPaths

    
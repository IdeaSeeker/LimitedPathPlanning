import config
config.configure_imports()

from collections import defaultdict
import heapq

from Map import Map
from Node import Node
from data_parser import *
from utils import heuristic


def a_star(_map: Map, start: Node, finish: Node, return_visited = False):
    visited = set()

    start = start.coordinates()
    finish = finish.coordinates()

    graph = defaultdict(list)
    for i in range(_map._height):
        for j in range(_map._width):
            if not _map.is_free(i, j):
                continue
            for s in _map.get_neighbors(_map._cells[i][j]):
                graph[(i, j)].append((s.i, s.j))

    dist = defaultdict(lambda: -1)
    dist[start] = 0
    heap = [(dist[start] + heuristic(Node(*start), Node(*finish)), start)]
    while len(heap) > 0:
        _, v = heapq.heappop(heap)
        visited.add(v)
        if v == finish:
            break
        for u in graph[v]:
            if dist[u] == -1 or dist[v] + 1 < dist[u]:
                dist[u] = dist[v] + 1
                heapq.heappush(heap, (dist[u] + heuristic(Node(*u), Node(*finish)), u))

    if return_visited:
        return dist[finish], list(visited)
    else:
        return dist[finish]

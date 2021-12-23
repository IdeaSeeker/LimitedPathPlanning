from typing import List
from Map import Map
from Node import Node
from Change import Change
from OpenList import OpenList
from utils import *


class LPAStar:
    def __init__(self, map: Map, start: Node, finish: Node):
        self._map = map

        self._start = start
        self._finish = finish
        self._change_index = 0
        self._path = [self._start]

        self._map.init_nodes()

        self._finish.g = self._finish.rhs = inf
        self._map.update_node(self._start)

        self._start.g = self._start.rhs = 0
        self._map.update_node(self._start)

        self._open = OpenList()
        self._open.insert(self.calculate_key(self._start), self._start)

        self.compute_shortest_path()


    def calcutale_rhs(self, s):
        if s == self._start:
            return 0
        neighbors = self._map.get_neighbors(s)
        if len(neighbors) > 0:
            rhs = min(
                adj_node.g + compute_cost(adj_node, s)
                for adj_node in neighbors
            )
        else:
            rhs = inf
        return min(rhs, inf)


    def calculate_key(self, s):
        corrected_g = min(s.g, s.rhs)
        return ( corrected_g + heuristic(self._finish, s), corrected_g )


    def update_vertex(self, s):
        if s != self._start:
            s.rhs = self.calcutale_rhs(s)
            self._map.update_node(s)
        if s in self._open:
            self._open.remove(s)
        if s.g != s.rhs:
            self._open.insert(self.calculate_key(s), s)


    def compute_shortest_path(self):
        visited = []
        while not self._open.is_empty() and (
            self._open.get_min_value() < self.calculate_key(self._finish) or \
            self._finish.rhs != self._finish.g
        ):
            u, _ = self._open.pop_min_value()
            visited.append(u)
            if u.g > u.rhs:
                u.g = u.rhs
                for s in self._map.get_neighbors(u):
                    self.update_vertex(s)
            else:
                u.g = inf
                for s in self._map.get_neighbors(u) + [u]:
                    self.update_vertex(s)
            self._map.update_node(u)
        return visited


    def print_path(self):
        self._map.print_path(self._path)


    def greedy_path(self):
        current = self._map[self._finish]
        if current.g == inf:
            return None
        path = [current]
        while current != self._start and current.g < inf:
            current = min(self._map.get_neighbors(current), key=lambda node: node.g)
            path.append(current)
        return list(reversed(path))


    def apply_changes(self, changes: List[Change]):
        for change in changes:
            self._map.apply_change(change)
            i, j = change.coordinates
            new_node = self._map[Node(i, j)]
            if new_node is not None:
                self.update_vertex(new_node)
            else:
                for adj_ij in self._map.get_neighbors(Node(i, j), free_required = False):
                    self.update_vertex(adj_ij)

            for s in list(self._open._data.keys()):
                if s in self._open:
                    self._open.remove(s)
                self._open.insert(self.calculate_key(s), s)

        visited = self.compute_shortest_path()
        return visited
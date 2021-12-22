from typing import List
from Map import Map
from Node import Node
from Change import Change
from OpenList import OpenList
from utils import *


class LPAStar:

    def __init__(self, map: Map, start: Node, finish: Node, changes: List[List[Change]]):
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
        self._open[self._start] = self.calculate_key(self._start)

        self._changes = changes


    def calcutale_rhs(self, s):
        if s == self._start:
            return 0
        rhs = min(
            adj_node.g + compute_cost(adj_node, s)
            for adj_node in self._map.get_neighbors(s)
        )
        return min(rhs, inf)


    def calculate_key(self, s):
        corrected_g = min(s.g, s.rhs)
        return ( corrected_g + heuristic(self._finish, s), corrected_g )


    def update_vertex(self, s):
        if s != self._start:
            s.rhs = self.calcutale_rhs(s)
            self._map.update_node(s)
        if s in self._open:
            self._open.pop(s)
        if s.g != s.rhs:
            self._open[s] = self.calculate_key(s)


    def compute_shortest_path(self):
        while not self._open.is_empty() and (
            self._open.get_min_value() < self.calculate_key(self._finish) or \
            self._finish.rhs != self._finish.g
        ):
            u, _ = self._open.pop()
            if u.g > u.rhs:
                u.g = u.rhs
                for s in self._map.get_neighbors(u):
                    self.update_vertex(s)
            else:
                u.g = inf
                for s in self._map.get_neighbors(u) + [u]:
                    self.update_vertex(s)
            self._map.update_node(u)


    def print_path(self):
        self._map.print_path(self._path)


    def greedy_path(self):
        current = self._map[self._finish]
        path = [current]
        while current != self._start and current.g < inf:
            current = min(self._map.get_neighbors(current), key=lambda node: node.g)
            path.append(current)
        return list(reversed(path))


    def run(self):
        self.compute_shortest_path()
        self.print_path(self.greedy_path())
        for change_set in self._changes:
            for change in change_set:
                self._map.apply_change(change)
                i, j = change.coordinates
                new_node = self._map[Node(i, j)]
                if new_node is not None:
                    self.update_vertex(new_node)
                else:
                    for adj_ij in self._map.get_neighbors(Node(i, j), free_required = False):
                        self.update_vertex(adj_ij)

                for s in self._open._data:
                    self._open._data[s] = self.calculate_key(s)

            self.compute_shortest_path()
            self._map.print_path(self.greedy_path())


if __name__ == "__main__":
    _map = Map()
    _map.read_from_string(3, 3,
'''
...
#..
#..
''')
    _start = Node(0, 0)
    _finish = Node(2, 2)
    _changes = [
        [Change(1, 1, 1, True)],
        [Change(1, 1, 2, True),
        Change(10, 1, 0, False),
        Change(10, 2, 0, False)]
    ]

    d_star = LPAStar(_map, _start, _finish, _changes)
    d_star.run()
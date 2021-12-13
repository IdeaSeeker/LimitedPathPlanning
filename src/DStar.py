from Map import Map
from Node import Node
from Change import Change
from OpenList import OpenList
from utils import *


class DStar:

    def __init__(self, map: Map, start: Node, finish: Node, changes: list[Change]):
        self._map = map
        self._start = start
        self._finish = finish
        self._change_index = 0
        self._changes = changes
        self._path = [self._start]

        self._map.init_nodes()

        self._start.g = self._start.rhs = inf
        self._map.update_node(self._start)

        self._finish.g = self._finish.rhs = 0
        self._map.update_node(self._finish)

        self._open = OpenList()
        self._open[self._finish] = self.calculate_key(self._finish)


    def calcutale_rhs(self, s):
        if s == self._finish:
            return 0
        rhs = min(
            adj_node.g + compute_cost(adj_node, s)
            for adj_node in self._map.get_neighbors(s)
        )
        return min(rhs, inf)


    def calculate_key(self, s):
        corrected_g = min(s.g, s.rhs)
        return ( corrected_g + heuristic(self._start, s), corrected_g )


    def update_vertex(self, s):
        if s != self._finish:
            s.rhs = self.calcutale_rhs(s)
            self._map.update_node(s)
        if s in self._open:
            self._open.pop(s)
        if s.g != s.rhs:
            self._open[s] = self.calculate_key(s)


    def compute_shortest_path(self):
        while not self._open.is_empty() and (
            self._open.get_min_value() < self.calculate_key(self._start) or \
            self._start.rhs != self._start.g
        ):
            u, _ = self._open.pop()
            if u.g >= u.rhs:
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


    def run(self):
        current_time = 0

        self.compute_shortest_path()
        while self._start != self._finish:
            if self._start.g == inf:
                print('No available path yet')
                continue

            best_node = best_cost = None
            for next_node in self._map.get_neighbors(self._start):
                next_cost = compute_cost(self._start, next_node) + next_node.g
                if best_cost is None or next_cost < best_cost:
                    best_cost = next_cost
                    best_node = next_node

            self._start = best_node
            self._map.update_node(self._start)
            self._path.append(self._start)

            is_changed = False
            while self._change_index < len(self._changes) and self._changes[self._change_index]._time == current_time:
                current_change = self._changes[self._change_index]

                if current_change.coordinates() == self._start.coordinates():
                    print(f'Invalid time( = {current_time}) for obstacle #{self._change_index}')
                    break

                self._map.apply_change(current_change)

                i, j = current_change.coordinates()
                new_node = self._map[Node(i, j)]
                if not new_node is None:
                    self.update_vertex(new_node)
                else:
                    for adj_ij in self._map.get_neighbors(Node(i, j)):
                        self.update_vertex(adj_ij)

                for s in self._open._data:
                    self._open._data[s] = self.calculate_key(s)

                is_changed = True
                self._change_index += 1

            if is_changed:
                self.compute_shortest_path()

            current_time += 1

        return self._path


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
    Change(0, 1, 1, True),
    Change(1, 1, 2, True),
    Change(10, 1, 2, False),
]

d_star = DStar(_map, _start, _finish, _changes)
d_star.run()
d_star.print_path()
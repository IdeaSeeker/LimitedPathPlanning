from Map import Map
from Node import Node
from Change import Change
from OpenList import OpenList
from utils import *


class DStarLite:
    def __init__(self, map: Map, start: Node, finish: Node, vision_distance=1):
        self._full_map = map
        self._current_map = Map()
        self._current_map.read_from_string(
            self._full_map._width,
            self._full_map._height,
            '\n'.join([
                '.' * self._full_map._width
                for _ in range(self._full_map._height)
            ])
        )

        self._K_m = 0

        self._start = start
        self._last_start = start
        self._finish = finish
        self._change_index = 0
        self._path = [self._start]
        self._paths = []

        self._current_map.init_nodes()

        self._start.g = self._start.rhs = inf
        self._current_map.update_node(self._start)

        self._finish.g = self._finish.rhs = 0
        self._current_map.update_node(self._finish)

        self._open = OpenList()
        self._open.insert(self.calculate_key(self._finish), self._finish)

        self.vision_distance = vision_distance


    def calcutale_rhs(self, s):
        if s == self._finish:
            return 0
        neighbors = self._current_map.get_neighbors(s)
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
        return ( corrected_g + heuristic(self._start, s) + self._K_m, corrected_g )


    def update_vertex(self, s):
        if s != self._finish:
            s.rhs = self.calcutale_rhs(s)
            self._current_map.update_node(s)
        if s in self._open:
            self._open.remove(s)
        if s.g != s.rhs:
            self._open.insert(self.calculate_key(s), s)


    def compute_shortest_path(self):
        while not self._open.is_empty() and (
            self._open.get_min_value() < self.calculate_key(self._start) or \
            self._start.rhs != self._start.g
        ):
            K_old = self._open.get_min_value()
            u, _ = self._open.pop_min_value()
            if self._current_map._cells[u.i][u.j] is None:
                continue
            if K_old < self.calculate_key(u):
                self._open.insert(self.calculate_key(u), u)
            elif u.g > u.rhs:
                u.g = u.rhs
                for s in self._current_map.get_neighbors(u):
                    self.update_vertex(s)
            else:
                u.g = inf
                for s in self._current_map.get_neighbors(u) + [u]:
                    self.update_vertex(s)
            self._current_map.update_node(u)
        self._paths.append(self.greedy_path())


    def print_path(self):
        self._current_map.print_path(self._path)


    def greedy_path(self):
        current = self._full_map[self._start]
        path = [current]
        while current != self._finish and current.g < inf:
            current = min(self._current_map.get_neighbors(current), key=lambda node: node.g)
            path.append(current)
        return list(reversed(path))


    def update_map(self):
        first_time = True

        for di in range(-self.vision_distance, self.vision_distance + 1):
            for dj in range(-self.vision_distance, self.vision_distance + 1):
                if di == dj and di == 0:
                    continue
                i, j = self._start.i + di, self._start.j + dj
                if not self._full_map.is_on_grid(i, j):
                    continue

                full_node_obst = self._full_map._cells[i][j] is None
                current_node_obst = self._current_map._cells[i][j] is None
                if current_node_obst and not full_node_obst or not current_node_obst and full_node_obst:
                    if first_time:
                        first_time = False
                        self._K_m += heuristic(self._last_start, self._start)
                        self._last_start = self._start

                    current_change = Change(0, i, j, full_node_obst)
                    self._current_map.apply_change(current_change)

                    i, j = current_change.coordinates
                    new_node = self._current_map[Node(i, j)]
                    if not new_node is None:
                        self.update_vertex(new_node)
                    else:
                        for adj_ij in self._current_map.get_neighbors(Node(i, j), free_required = False):
                            self.update_vertex(adj_ij)

                    # for s in self._open._data:
                    #     self._open._data[s] = self.calculate_key(s)

        self.compute_shortest_path()


    def collect_open_stats(self):
        return self._open.add_count, self._open.get_count, self._open.pop_count


    def run(self):
        current_time = 0

        self.update_map()
        self.compute_shortest_path()
        while self._start != self._finish:
            current_time += 1
            if self._start.g == inf:
                print('No available path yet')
                continue

            best_node = best_cost = None
            for next_node in self._current_map.get_neighbors(self._start):
                next_cost = compute_cost(self._start, next_node) + next_node.g
                if best_cost is None or next_cost < best_cost:
                    best_cost = next_cost
                    best_node = next_node

            self._start = best_node
            self._current_map.update_node(self._start)
            self._path.append(self._start)

            self.update_map()

        return self._path

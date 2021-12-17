from Node import Node
from Change import Change
from utils import *


class Map:

    def __init__(self, width = 0, height = 0, grid_cells = []):
        self._width = width
        self._height = height
        self._cells = grid_cells


    def __getitem__(self, node):
        return self._cells[node.i][node.j]


    def __setitem__(self, node, value):
        self._cells[node.i][node.j] = value


    def __str__(self):
        result = []
        for i in range(self._width):
            for j in range(self._height):
                if self._cells[i][j] is None:
                    result.append('#')
                else:
                    result.append('.')
            result.append('\n')
        return ''.join(result)


    def update_node(self, node):
        self[node] = node


    def print(self, verbose = False):
        if verbose:
            for i in range(self._width):
                for j in range(self._height):
                    print(self._cells[i][j], end = ' ')
                print()
        else:
            print(str(self))


    def print_path(self, path: list[Node]):
        result = str(self).split('\n')
        result = list(map(list, result))
        for node in path:
            if result[node.i][node.j] == '#':
                result[node.i][node.j] = '@'
            else:
                result[node.i][node.j] = 'O'
        for line in result:
            print(''.join(line))


    def read_from_string(self, width, height, cell_str):
        # '.' - for free cells, any other - for obstacles
        self._width = width
        self._height = height
        self._cells = [
            [
                None  # for obstacles
                for _ in range(width)
            ]
            for _ in range(height)
        ]

        i = 0
        for line in cell_str.split('\n'):
            if len(line) == 0:
                continue
            j = 0
            for cell in line:
                if cell == '.':  # Node() for free cells
                    self._cells[i][j] = Node(i, j)
                j += 1
            i += 1


    def init_nodes(self):
        for i in range(self._width):
            for j in range(self._height):
                if not self._cells[i][j] is None:
                    self._cells[i][j].g   = inf
                    self._cells[i][j].rhs = inf


    def apply_change(self, change: Change):
        i, j = change.coordinates()
        if change._is_obst:
            self._cells[i][j] = None
        else:
            self._cells[i][j] = Node(i, j, g = inf, rhs = inf)


    def is_on_grid(self, i, j):
        return (0 <= j < self._width) and (0 <= i < self._height)


    def is_free(self, i, j):
        return self.is_on_grid(i, j) and not self._cells[i][j] is None


    def get_neighbors(self, node, free_required = True, diagonal_allowed = False):
        i, j = node.coordinates()

        if free_required and not self.is_free(i, j):
            return []

        neighbors = [
            self._cells[i + di][j + dj]
            for di, dj in [(0, -1), (-1, 0), (1, 0), (0, 1)]
            if self.is_free(i + di, j + dj)
        ]

        if diagonal_allowed:
            neighbors += [
                self._cells[i + di][j + dj]
                for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                if self.is_free(i + di, j + dj) and self.is_free(i + di, j) and self.is_free(i, j + dj)
            ]

        return neighbors


    def get_size(self):
        return (self._height, self._width)

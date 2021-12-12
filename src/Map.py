from src import Node


class Map:

    def __init__(self, width = 0, height = 0, grid_cells = []):
        self._width = width
        self._height = height
        self._cells = grid_cells


    def read_from_string(self, cell_str, width, height):
        # '.' - for free cells, any other - for obstacles
        self._width = width
        self._height = height
        self._cells = [
            [0 for _ in range(width)]
            for _ in range(height)
        ]

        i = 0
        for line in cell_str.split('\n'):
            if len(line) == 0:
                continue
            j = 0
            for cell in line:
                self._cells[i][j] = int(cell != '.')  # 0 for free cells
                j += 1
            i += 1


    def init_nodes(self):
        for i in range(self._width):
            for j in range(self._height):
                self._cells[i][j] = Node(i, j, g = 10 ** 9)


    def is_on_grid(self, i, j):
        return (0 <= j < self._width) and (0 <= i < self._height)


    def is_free(self, i, j):
        return self.is_on_grid(i, j) and self._cells[i][j] == 0


    def get_neighbors(self, i, j, diagonal_allowed = False):
        if not self.is_free(i, j):
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

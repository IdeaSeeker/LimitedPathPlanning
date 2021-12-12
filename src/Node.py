class Node:

    def __init__(self, i, j, g = 0, h = 0, F = None, parent = None):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        if F is None:
            self.F = self.g + h
        else:
            self.F = F
        self.parent = parent


    def __str__(self):
        return f'Node({self.i}, {self.j}: {self.g} + {self.h} = {self.F})'


    def __repr__(self):
        return str(self)


    def coordinates(self):
        return (self.i, self.j)


    def __eq__(self, other):
        return self.coordinates() == other.coordinates()


    def __hash__(self):
        return hash(self.coordinates())


    def __lt__(self, other):
        return self.F < other.F or (self.F == other.F and self.h < other.h)

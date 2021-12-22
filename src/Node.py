class Node:

    def __init__(self, i, j, g = 0, rhs = 0):
        self.i = i
        self.j = j
        self.g = g
        self.rhs = rhs
        # self.h = h
        # if F is None:
        #     self.F = self.g + h
        # else:
        #     self.F = F
        # self.parent = parent


    def __str__(self):
        return f'Node({self.i}, {self.j}: g = {self.g}, rhs = {self.rhs})'


    def __repr__(self):
        return str(self)


    def coordinates(self):
        return (self.i, self.j)


    def __eq__(self, other):
        return self.coordinates() == other.coordinates()


    def __hash__(self):
        return hash(self.coordinates())


    def __lt__(self, other):
        return self.g < other.g

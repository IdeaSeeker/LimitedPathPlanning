inf = 10 ** 9

uldr = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def compute_cost(s, t):
    return ( abs(s.i - t.i) ** 2 + abs(s.j - t.j) ** 2 ) ** 0.5


def heuristic(s, t):
    return abs(s.i - t.i) + abs(s.j - t.j)

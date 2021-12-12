def compute_cost(i1, j1, i2, j2):
    # (i1, j1) -> (i2, j2)
    return ( abs(i1 - i2) + abs(j1 - j2) ) ** 0.5

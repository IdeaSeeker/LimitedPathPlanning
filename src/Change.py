class Change:

    def __init__(self, time: int, i: int, j: int, is_obst: bool):
        self._time = time
        self._i = i
        self._j = j
        self._is_obst = is_obst

    @property
    def coordinates(self):
        return self._i, self._j
